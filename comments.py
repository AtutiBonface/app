import os
import asyncio
import aiohttp
import ssl
import certifi
import time
import threading
from asyncio import Queue
from settings import Settings
import aiofiles
import database

class TaskManager:
    def __init__(self, parent) -> None:
        # Initialize configuration settings
        self.CHUNK_SIZE = 256 * 1024  # 256 KB
        self.PROGRESS_UPDATE_INTERVAL = 1024 * 1024  # 1 MB
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        self.links_and_filenames = Queue()  # Queue for managing download tasks
        self.parent = parent
        self.max_concurrent_downloads = 5  # Maximum number of concurrent downloads
        self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)
        self.condition = asyncio.Condition()  # Condition to notify when the queue is not empty
        self.paused_downloads = {}  # Dictionary to keep track of paused downloads
        self.loop = asyncio.new_event_loop()
        self.download_thread = threading.Thread(target=self.download_task_manager, daemon=True)
        self.download_thread.start()
        self.is_downloading = False

    async def append_file_details_to_storage(self, filename, path, address, date):
        # Append file details to storage
        if not path:
            path = Settings(self.parent.content_container).xengine_download_path_global  # Path stored in config file
        await asyncio.to_thread(self.parent.add_download_to_list, filename, address, path, date)
        await asyncio.to_thread(database.add_data, filename, address, '---', '---', 'waiting...', date, path)

    async def update_file_details_on_storage_during_download(self, filename, address, size, downloaded, status, speed, date):
        # Update file details in storage during download
        await asyncio.to_thread(self.parent.update_download, filename, status, size, downloaded, date, speed)
        await asyncio.to_thread(database.update_data, filename, address, size, downloaded, status, date)

    def download_task_manager(self):
        # Manage the download tasks using asyncio
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.download_tasks())

    def returnSpeed(self, speed):
        # Convert speed to human-readable format
        if speed > 1:
            return f'{round(speed, 2)} mb/s'
        elif speed > 0:
            return f'{int(speed * 1000)} kbs/s'
        else:
            return f'{int(speed * 1000)} bytes/s'

    async def addQueue(self, file):
        # Add a file to the download queue
        await self.links_and_filenames.put(file)
        async with self.condition:
            self.condition.notify_all()

    def validate_filename(self, filename, selected_path):
        # Validate and ensure the filename is unique
        path = Settings(self.parent.content_container).xengine_download_path_global  # Path stored in config file
        if selected_path:
            path = selected_path
        os.makedirs(path, exist_ok=True)  # Make directory if it doesn't exist
        file_path = os.path.join(path, filename)
        index = 1
        name, extension = os.path.splitext(filename)

        while os.path.exists(file_path) or database.check_filename_existance(file_path):
            file_path = os.path.join(path, f'{name}_{index}{extension}')
            index += 1

        return file_path

    async def download_tasks(self):
        # Handle the download tasks
        self.is_downloading = True
        while True:
            async with self.condition:
                await self.condition.wait()

            while not self.links_and_filenames.empty():
                file = await self.links_and_filenames.get()
                link, filename, path = file
                if filename not in self.paused_downloads:
                    filename = self.validate_filename(filename, path)
                    await self.append_file_details_to_storage(os.path.basename(filename), path, link, time.strftime('%Y-%m-%d'))
                asyncio.create_task(self.start_task((link, filename, path)))
                self.links_and_filenames.task_done()

            self.is_downloading = False

    async def start_task(self, file):
        # Start a download task
        async with self.semaphore:
            link, filename, path = file
            timeout = aiohttp.ClientTimeout(total=None)
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_context, limit=None)
            async with aiohttp.ClientSession(connector=connector, headers=self.headers, timeout=timeout) as session:
                downloaded_chunk = self.paused_downloads.get(filename, {}).get('downloaded', 0)
                try:
                    async with session.get(link, headers={'Range': f'bytes={downloaded_chunk}-'}) as resp:
                        if resp.status in (200, 206):
                            await self._handle_download(resp, filename, link, downloaded_chunk)
                        else:
                            await self.update_file_details_on_storage_during_download(filename, link, 0, downloaded_chunk, 'failed!', 0, time.strftime('%Y-%m-%d'))
                except aiohttp.ClientError as e:
                    # Handle aiohttp client errors
                    await self.update_file_details_on_storage_during_download(filename, link, 0, downloaded_chunk, 'failed!', 0, time.strftime('%Y-%m-%d'))
                    print(f"Client error occurred: {e}")
                except Exception as e:
                    # Handle other exceptions
                    await self.update_file_details_on_storage_during_download(filename, link, 0, downloaded_chunk, 'failed!', 0, time.strftime('%Y-%m-%d'))
                    print(f"Unexpected error occurred: {e}")

    async def _handle_download(self, resp, filename, link, initial_chunk=0):
        # Handle the download process
        downloaded_chunk = initial_chunk
        size = int(resp.headers.get('Content-Length', 0)) + initial_chunk
        mode = 'ab' if initial_chunk > 0 else 'wb'

        async with aiofiles.open(filename, mode) as f:
            start_time = time.time()
            async for chunk in resp.content.iter_chunked(self.CHUNK_SIZE):
                if filename in self.paused_downloads and not self.paused_downloads[filename]['resume']:
                    self.paused_downloads[filename] = {'downloaded': downloaded_chunk, 'size': size, 'link': link}
                    await self.update_file_details_on_storage_during_download(filename, link, size, downloaded_chunk, 'paused.', 0, time.strftime('%Y-%m-%d'))
                    return

                await f.write(chunk)
                downloaded_chunk += len(chunk)
                if downloaded_chunk % self.PROGRESS_UPDATE_INTERVAL == 0 or downloaded_chunk == size:
                    await self._update_progress(filename, link, size, downloaded_chunk, start_time)

            if filename in self.paused_downloads:
                del self.paused_downloads[filename]

            await self.update_file_details_on_storage_during_download(filename, link, size, size, 'completed.', 0, time.strftime('%Y-%m-%d'))

    async def pause_downloads_fn(self, filename, size, link, downloaded):
        # Pause the download for a specific file
        self.paused_downloads[filename] = {'downloaded': downloaded, 'size': size, 'link': link, 'resume': False}
        await self.update_all_active_downloads('paused.')

    async def resume_downloads_fn(self, name, address, downloaded):
        # Resume the download for a specific file
        self.paused_downloads[name] = {'downloaded': downloaded, 'size': '---', 'link': address, 'resume': True}
        for filename, info in self.paused_downloads.items():
            if name == filename:
                await self.addQueue((info['link'], filename, None))
        await self.update_all_active_downloads('resuming...')
        async with self.condition:
            self.condition.notify_all()

    async def update_all_active_downloads(self, status):
        # Update the status of all active downloads
        speed = 0
        for filename, info in self.paused_downloads.items():
            await self.update_file_details_on_storage_during_download(filename, info['link'], info['size'], info['downloaded'], status, speed, time.strftime('%Y-%m-%d'))

    async def _update_progress(self, filename, link, size, downloaded_chunk, start_time):
        # Update the download progress
        unit_time = time.time() - start_time
        if downloaded_chunk > 0 and unit_time > 1:  # Ensure some time has passed and some data is downloaded
            down_in_mbs = downloaded_chunk / (1024 * 1024)
            speed = down_in_mbs / unit_time
            speed_str = self.returnSpeed(speed)
            percentage = round((downloaded_chunk / size) * 100, 0)
            await self.update_file_details_on_storage_during_download(filename, link, size, downloaded_chunk, f'{percentage}%', speed_str, time.strftime('%Y-%m-%d'))
        else:
            print("Calculating speed...")

