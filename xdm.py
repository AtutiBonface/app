import os, asyncio,aiohttp, ssl, certifi, time, threading, re
from asyncio import Queue 
from settings import Settings
import aiofiles, database

class TaskManager():
    


    def __init__(self, parent) -> None:
            self.CHUNK_SIZE = 256 * 1024  # 1 MB
           
            self.PROGRESS_UPDATE_INTERVAL = 1024 * 1024         
                
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            self.name = ''
            self.links_and_filenames = Queue()## link and filename is appended
            self.ui_files = []
            self.parent = parent
            self.max_concurrent_downloads = 5  # Set the maximum number of concurrent downloads
            self.semaphore = asyncio.Semaphore(self.max_concurrent_downloads)

            self.ui_callback = parent
            self.condition = asyncio.Condition() ## used to check if queue is not empty and when file is added to a queue queue has value

            self.paused_downloads = {}
            self.is_paused = False

            self.loop = asyncio.new_event_loop()## creating a new loop
            self.download_thread = threading.Thread(target=self.download_task_manager, daemon=True)
            # starting a different thread to run downloads
            self.download_thread.start()

            self.is_downloading = False
    async def append_file_details_to_storage(self, filename, path, address, date):
        if not path:
            path = Settings(self.parent.content_container).xengine_download_path_global## the path stored in config file
        await asyncio.to_thread(self.parent.add_download_to_list ,filename, address, path, date)
        await asyncio.to_thread(database.add_data,filename,address, '---', '---', 'waiting...', date, path)

        
    async def update_file_details_on_storage_during_download(self, filename, address,size, downloaded, status, speed, date):
        file_details = []
        await asyncio.to_thread(self.parent.update_download, filename, status, size,downloaded, date, speed)
        await asyncio.to_thread(database.update_data, filename, address,size, downloaded, status, date)
        
        
         
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
                if not filename in self.paused_downloads:## filename in paused downloads has path with it but if it does not exist it creates name together with path selected
                    filename = self.validate_filename(filename, path)
                    name_with_no_path = os.path.basename(filename)
                    await self.append_file_details_to_storage(name_with_no_path, path, link, time.strftime(r'%Y-%m-%d'))
                   
                file = (link, filename, path)
                
                tasks.append(asyncio.create_task(self.start_task(file)))
                self.links_and_filenames.task_done()

            if tasks:
                await asyncio.gather(*tasks)
                tasks.clear()

            if self.links_and_filenames.empty():
                self.is_downloading = False

    async def start_task(self, file): 
        async with self.semaphore:
            link, filename ,path= file
            self.timeout = aiohttp.ClientTimeout(total=None)
            self.ssl_context = ssl.create_default_context(cafile=certifi.where())
            self.connector = aiohttp.TCPConnector(ssl=self.ssl_context, limit=None)
            async with aiohttp.ClientSession(connector=self.connector, headers=self.headers,timeout=self.timeout) as session:
                downloaded_chunk = self.paused_downloads.get(filename, {}).get('downloaded', 0)
                size = 0
                speed =0
               
                try:
                    async with session.get(link, headers={'Range': f'bytes={downloaded_chunk}-'}) as resp:
                        if resp.status in (200, 206):
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

                if downloaded_chunk % self.PROGRESS_UPDATE_INTERVAL == 0 or downloaded_chunk == size:

                    await self._update_progress(filename, link, size, downloaded_chunk, start_time)

               
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
                
                        
        
