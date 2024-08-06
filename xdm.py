import os, asyncio,aiohttp, ssl, certifi, time, threading, re
from asyncio import Queue 
from settings import Settings
import aiofiles, database
from pathlib import Path
import shutil
from urllib.parse import urlparse, urlunparse

class TaskManager():
    def get_base_url(self, url):
        parsed_url = urlparse(url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '/', '', '', ''))
        return base_url
    


    def __init__(self, parent) -> None:
            # Initialize configuration settings

            self.CHUNK_SIZE = 256 * 1024  # 256 kb

            self.SEGMENT_SIZE = 10 * 1024 * 1024  # 10 MB segments
           
            self.PROGRESS_UPDATE_INTERVAL = 1024 * 1024 

            self.lock = asyncio.Lock()  

            self.retry_attempts = 3

            self.concurrency_delay = 0.8

            self.size_downloaded_dict = {}    

                
            self.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'identity;q=1, *;q=0',
                'Connection': 'keep-alive',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
                }
            
            self.name = ''
            self.links_and_filenames = Queue() # Queue for managing download tasks
            self.ui_files = []
            self.parent = parent
            self.max_concurrent_downloads = 5  # Set the maximum number of concurrent downloads
            self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)

            self.ui_callback = parent
            self.condition = asyncio.Condition() # Condition to notify when the queue is not empty

            self.paused_downloads = {} # Dictionary to keep track of paused downloads
            self.is_paused = False

            self.loop = asyncio.new_event_loop()## creating a new loop
            self.download_thread = threading.Thread(target=self.download_task_manager, daemon=True)
            # starting a different thread to run downloads
            self.download_thread.start()

            self.is_downloading = False
    async def append_file_details_to_storage(self, filename, path, address, date):
        # Append file details to storage
        if not path:
            path = Settings(self.parent.content_container).xengine_download_path_global## the path stored in config file
        await asyncio.to_thread(self.parent.add_download_to_list ,filename, address, path, date)
        await asyncio.to_thread(database.add_data,filename,address, '---', '---', 'waiting...', date, path)

        
    async def update_file_details_on_storage_during_download(self, filename, address,size, downloaded, status, speed, date):
        # Update file details in storage during download
        await asyncio.to_thread(self.parent.update_download, filename, status, size,downloaded, date, speed)
        await asyncio.to_thread(database.update_data, filename, address,size, downloaded, status, date)
        
        
         
    def download_task_manager(self):
        # Manage the download tasks using asyncio
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.download_tasks())
        

    # converts speed to mbs, kbs, bytes
    def returnSpeed(self, speed):
        # Convert speed to human-readable format

        if speed > 1:
           speed = round(speed, 2)
           return f'{speed} mb/s'
        elif speed > 0:
            speed = int(speed * 1000)
            return f'{speed} kbs/s'
        else: 
            speed = int(speed * 1000)
            return f'{speed} bytes/s'
    async def addQueue(self, file):  
        # Add a file to the download queue
     
        self.links_and_filenames.put_nowait(file)
        # adds to queue,              
            
        async with self.condition:
            await self.condition.notify_all()



        # sends a notification that a queue was added
        

    ## this adds index to file name if file exists
    def validate_filename(self, filename, selected_path):
        path = Settings(self.parent.content_container).xengine_download_path_global## the path stored in config file
        if selected_path:
            path = selected_path
        try:
            os.makedirs(path, exist_ok=True)## making directory if it does exist
        except Exception as e:
            pass
        file_path = os.path.join(path, filename)
        index = 1
        name, extension = os.path.splitext(filename)

        name_with_no_path = f'{name}{extension}'

        new_name = file_path

        while True:

            if os.path.exists(new_name):
            
                new_name = os.path.join(path, f'{name}_{index}{extension}')
                index += 1
                continue

            if database.check_filename_existance(new_name):
                new_name = os.path.join(path, f'{name}_{index}{extension}')
                index += 1               

                continue

            break


        return new_name
    async def download_tasks(self):
        # Handle the download tasks
        self.is_downloading = True
       
        while True:
            # waits for self.links and filename queue to have link if it there are links it continues 
            # otherwise it keeps waiting this prevents while True not to run forever as it consumes alot cpu
            async with self.condition:
                await self.condition.wait()
               

            while not self.links_and_filenames.empty():
                file = await self.links_and_filenames.get()
                link, filename, path = file
                if not filename in self.paused_downloads:## filename in paused downloads has path with it but if it does not exist it creates name together with path selected
                    filename = self.validate_filename(filename, path)
                    name_with_no_path = os.path.basename(filename)
                    await self.append_file_details_to_storage(name_with_no_path, path, link, time.strftime(r'%Y-%m-%d'))
                   
                file = (link, filename, path)
                
                asyncio.create_task(self.start_task(file))

                self.links_and_filenames.task_done()


            if self.links_and_filenames.empty():
                self.is_downloading = False

    async def start_task(self, file):     
    
        link, filename ,path= file
        self.timeout = aiohttp.ClientTimeout(total=None)
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context, limit=None)
        async with aiohttp.ClientSession(connector=self.connector, headers=self.headers,timeout=self.timeout) as session:
            downloaded_chunk = self.paused_downloads.get(filename, {}).get('downloaded', 0)
            size = 0
            speed =0
            
            try:
                async with session.get(link) as resp:
                    if resp.status in (200, 206):
                        size = int(resp.headers['Content-Length'])

                        range_supported = 'Accept-Ranges' in resp.headers
                        
                        
                        if size > self.SEGMENT_SIZE * 3 and range_supported:
                            
                            num_segments = (size + self.SEGMENT_SIZE - 1) // self.SEGMENT_SIZE

                            tasks = []
                            for i in range(num_segments):
                                start = i * self.SEGMENT_SIZE
                                end = start + self.SEGMENT_SIZE - 1 if i < num_segments - 1 else size - 1
                                tasks.append(self.fetch_segment(session, link, start, end, filename, i, size))

                                await asyncio.sleep(self.concurrency_delay)

                            await asyncio.gather(*tasks)
                            await self.combine_segments(filename,link,size, num_segments)

                            async with self.lock:
                                if filename in self.size_downloaded_dict:
                                    del self.size_downloaded_dict[filename]
                            
                        else:
                            await self._handle_download(resp, filename, link, downloaded_chunk)
                        
                    else:
                        
                        await self.update_file_details_on_storage_during_download(
                filename,link, size, downloaded_chunk, 'failed!',speed, time.strftime('%Y-%m-%d'))
                        
            except aiohttp.ClientError as e: 
                
                await self.update_file_details_on_storage_during_download(
                filename,link, size, downloaded_chunk, 'failed!', speed,time.strftime('%Y-%m-%d')
                )
            except Exception as e:
                print("Error is", e)

    async def _handle_segments_downloads_ui(self,filename, link, total_size):
        async with self.lock:
            if filename in self.size_downloaded_dict:
                total_downloaded, start_time = self.size_downloaded_dict[filename]
                unit_time = time.time() - start_time
                if total_downloaded > 0 and unit_time > 1:
                    down_in_mbs = total_downloaded / (1024 * 1024)
                    speed = down_in_mbs / unit_time
                    new_speed = round(speed, 3)
                    speed_str = self.returnSpeed(new_speed)
                    percentage = round((total_downloaded / total_size) * 100, 0)

                    await self.update_file_details_on_storage_during_download(
                        filename, link, total_size, total_downloaded, f'{percentage}%', speed_str, time.strftime(r'%Y-%m-%d')
                    )

    async def fetch_segment(self, session, url, start, end, filename, segment_num, original_filesize):
        referer = self.get_base_url(url)
        headers = self.headers.copy()
        headers['Range'] = f'bytes={start}-{end}'
        headers['Referer'] = referer
        
            
       
        max_retries = 5
        retry_delay = 1
        segment_downloaded = 0
        for attempt in range(max_retries):
            try:
                print(f"Requesting segment {segment_num} with range {headers['Range']}")
                async with session.get(url, headers=headers) as response:
                    print(f"Segment {segment_num}: Status {response.status}")
                    if response.status in (200, 206):  # Partial Content

                        basename = os.path.basename(filename)
                        tem_folder = f"{Path().home()}/.blackjuice/temp/.{basename}"
                        try:
                            os.makedirs(tem_folder, exist_ok=True)
                        except Exception as e:
                            print(e)

                        segment_filename = f'{tem_folder}/part{segment_num}'
                    
                        async with aiofiles.open(segment_filename, 'wb') as f:
                            async for chunk in response.content.iter_chunked(self.CHUNK_SIZE):
                                await f.write(chunk)

                                chunk_size = len(chunk)
                                segment_downloaded += chunk_size

                                async with self.lock:
                                    if filename in self.size_downloaded_dict:
                                        self.size_downloaded_dict[filename][0] += len(chunk)
                                    else:
                                        self.size_downloaded_dict[filename] = [len(chunk), time.time()]

                                await self._handle_segments_downloads_ui(filename, url, original_filesize)
                        break

                    elif response.status == 416:  # Requested Range Not Satisfiable
                            print(f"Segment {segment_num}: Requested range not satisfiable {start}-{end}")

                            return
                    else:
                        print(f"Failed to fetch segment {segment_num}, attempt {max_retries}, status: {response.status}")
                        await asyncio.sleep(retry_delay)  # Wait a bit before retrying

                       
                        retry_delay = min(retry_delay * 2, 60)
                        
            except aiohttp.ClientError as e:
                print(f"Network error fetching segment {segment_num}, attempt {attempt + 1}: {e}")

        print(f"Segment {segment_num} failed after {self.retry_attempts} attempts")

    async def combine_segments(self, filename,link,size, num_segments):
        basename = os.path.basename(filename)
        tem_folder = f"{Path().home()}/.blackjuice/temp/.{basename}"
        
        with open(filename, 'wb') as final_file:
            for i in range(num_segments):
                segment_filename = f'{tem_folder}/part{i}'
                async with aiofiles.open(segment_filename, 'rb') as segment_file:
                    while True:
                        chunk = await segment_file.read(self.CHUNK_SIZE)
                        if not chunk:
                            break
                        final_file.write(chunk)
                try:
                    shutil.rmtree(tem_folder)
                except Exception as e:
                    print('Error of deleting folder is ', e)

        await self.update_file_details_on_storage_during_download(
            filename, link, size, size, 'completed.', 0, time.strftime(r'%Y-%m-%d'))
    
                    

    async def _handle_download(self, resp,filename, link, initial_chuck=0):
       
        downloaded_chunk = initial_chuck

        size = int(resp.headers.get('Content-Length', 0)) + initial_chuck
        mode = 'ab' if initial_chuck > 0 else 'wb'

        

     
        async with aiofiles.open(filename, mode) as f:
            start_time = time.time()
            speed = 0
            async for chunk in resp.content.iter_chunked(self.CHUNK_SIZE):
                if filename in self.paused_downloads and self.paused_downloads[filename]['resume'] == False:
                    self.paused_downloads[filename] = {
                        'downloaded': downloaded_chunk,
                        'size': size,
                        'link': link
                    }
                    await self.update_file_details_on_storage_during_download(
                        filename, link, size, downloaded_chunk, 'paused.',speed, time.strftime(r'%Y-%m-%d')
                    )
        
                    return
                await f.write(chunk)

                

                downloaded_chunk += len(chunk)

                

                await self._update_progress(filename, link, size, downloaded_chunk, start_time)

               
                

            if filename in self.paused_downloads:
                del self.paused_downloads[filename]

            await self.update_file_details_on_storage_during_download(
                filename, link, size, size, 'completed.',speed, time.strftime(r'%Y-%m-%d')
            )
        
            

    async def pause_downloads_fn(self, filename, size, link ,downloaded):
        self.paused_downloads[filename] = {
                        'downloaded': downloaded,
                        'size': size,
                        'link': link,
                        'resume': False
                    }
       
        await self.update_all_active_downloads('paused.')

    async def resume_downloads_fn(self, name, address, downloaded):

        self.paused_downloads[name] = {
            'downloaded': downloaded,
            'size': '---',
            'link': address,
            'resume': True
        }
        
        for filename, info in self.paused_downloads.items():
            if name == filename:                          
                await self.addQueue((info['link'], filename, None))
            
        await self.update_all_active_downloads('resuming...')      
        async with self.condition:
            self.condition.notify_all()




    async def update_all_active_downloads(self, status):
        speed = 0
        for filename, info in self.paused_downloads.items():
            await self.update_file_details_on_storage_during_download(
                filename, info['link'], info['size'], info['downloaded'], status,speed, time.strftime(r'%Y-%m-%d')
            )

    async def _update_progress(self,filename, link, size, downloaded_chunk, start_time):
        unit_time = time.time() - start_time

        if downloaded_chunk > 0 and unit_time > 1:  # Ensure some time has passed and some data is downloaded
            down_in_mbs = downloaded_chunk / (1024 * 1024)
            speed = down_in_mbs / unit_time
            new_speed = round(speed, 3)
            speed_str = self.returnSpeed(new_speed)
            percentage = round((downloaded_chunk / size) * 100, 0)
           
            
            await self.update_file_details_on_storage_during_download(
                filename, link, size, downloaded_chunk, f'{percentage}%', speed_str, time.strftime(r'%Y-%m-%d')
            )
        else:
           
            print("Calculating speed...")
                
                        
        
