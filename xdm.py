import os, asyncio,aiohttp, ssl, certifi, time, threading, re
from asyncio import Queue 
from settings import Settings
import aiofiles, database

class TaskManager():
    def __init__(self, parent) -> None:
            
           
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            self.name = ''
            self.links_and_filenames = Queue()## link and filename is appended
            self.ui_files = []
            self.parent = parent
            self.max_concurrent_downloads = 5  # Set the maximum number of concurrent downloads
            self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)

            self.ui_callback = parent
            self.condition = asyncio.Condition() ## used to check if queue is not empty and when file is added to a queue queue has value

            
            self.loop = asyncio.new_event_loop()## creating a new loop
            self.download_thread = threading.Thread(target=self.download_task_manager, daemon=True)
            # starting a different thread to run downloads
            self.download_thread.start()

            self.is_downloading = False
    def append_file_details_to_storage(self, filename, path, address, date):
        if not path:
            path = Settings(self.parent.content_container).xengine_download_path_global## the path stored in config file
        self.parent.add_download_to_list(filename, address, path, date)
        database.add_data(filename,address, '---', '---', 'waiting...', date, path)

        
    def update_file_details_on_storage_during_download(self, filename, address,size, downloaded, status, date):
        file_details = []
        self.parent.update_download(filename, status, size, date)
        database.update_data(filename, address,size, downloaded, status, date)
        
        
         
    def download_task_manager(self):
        # where threads starts and asyncio couritine is started
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.download_tasks())
        

    # converts speed to mbs, kbs, bytes
    def returnSpeed(self, speed):
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
            os.makedirs(path)## making directory if it does exist
        except Exception as e:
            pass
        file_path = f'{path}/{filename}'
        index = 1
        name, extension = os.path.splitext(filename)

        new_name = file_path

        while os.path.exists(new_name):
            new_name = f'{path}/{name}_{index}{extension}'
            index += 1

        return new_name
    async def download_tasks(self):
        self.is_downloading = True
        tasks = []
        while True:
            # waits for self.links and filename queue to have link if it there are links it continues 
            # otherwise it keeps waiting this prevents while True not to run forever as it consumes alot cpu
            async with self.condition:
                await self.condition.wait()
               

            while not self.links_and_filenames.empty():
                file = await self.links_and_filenames.get()
                link, filename, path = file
                filename = self.validate_filename(filename, path)
                file = (link, filename, path)
                name_with_no_path = os.path.basename(filename)
                self.append_file_details_to_storage(name_with_no_path, path, link, time.strftime(r'%Y-%m-%d'))
                tasks.append(self.start_task(file))
                self.links_and_filenames.task_done()

            if tasks:
                await asyncio.gather(*tasks)

            if self.links_and_filenames.empty():
                self.is_downloading = False

    async def start_task(self, file): 
        async with self.semaphore:
            link, filename ,path= file
            self.timeout = aiohttp.ClientTimeout(total=None)
            self.ssl_context = ssl.create_default_context(cafile=certifi.where())
            self.connector = aiohttp.TCPConnector(ssl=self.ssl_context)
            async with aiohttp.ClientSession(connector=self.connector, headers=self.headers,timeout=self.timeout) as session:
                downloaded_chunk = 0
                speed = 0
                size = 0
                percentage = 0
                file_type = 'Video' 
                try:
                    async with session.get(link) as resp:
                        if resp.status == 200:
                            async with aiofiles.open(filename, 'wb') as f:
                                start_time = time.time()
                                file_size = resp.headers.get('Content-Length', None)
                                cont_type = resp.headers.get('Content-Type', None)

                                

                                if file_size:
                                    size = int(file_size)
                                    
                                else:
                                    if resp.headers.get('Transfer-Encoding') == 'chunked':
                                        file_size = 'unknown'
                                    else:
                                        file_size = None
                                
                                async for chunk in resp.content.iter_chunked(16*1024):
                                    await f.write(chunk)
                                    unit_time = time.time() - start_time 
                                    if not unit_time == 0:
                                        downloaded_chunk += len(chunk)
                                        down_in_mbs = int(downloaded_chunk / (1024*1024))
                                        speed = down_in_mbs / unit_time
                                        new_speed = round(speed, 3)
                                        speed = self.returnSpeed(new_speed)
                                        percentage = round((downloaded_chunk/size) * 100,0)
                                        self.update_file_details_on_storage_during_download(
                                        filename,link,size, downloaded_chunk, f'{percentage}%', time.strftime(r'%Y-%m-%d'))
                                        

                                
                                self.update_file_details_on_storage_during_download(
                                filename, link,size, size, 'completed.', time.strftime(r'%Y-%m-%d'))
                                

                except Exception as e:
                    print(e)
                    
                    self.update_file_details_on_storage_during_download(
                    filename,link, size, downloaded_chunk, 'failed!', time.strftime('%Y-%m-%d')
                    )
                
                        
        
