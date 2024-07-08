import os, asyncio,aiohttp, ssl, certifi, time, threading, re
from asyncio import Queue
from settings import Settings

class TaskManager():
    def __init__(self, parent) -> None:
            
           
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            self.name = ''
            self.links_and_filenames = Queue()## link and filename is appended
            self.ui_files = []
            self.parent = parent

            self.ui_callback = parent.update_ui
            self.condition = asyncio.Condition() ## used to check if queue is not empty and when file is added to a queue queue has value

            
            self.loop = asyncio.new_event_loop()## creating a new loop
            self.download_thread = threading.Thread(target=self.download_task_manager, daemon=True)
            # starting a different thread to run downloads
            self.download_thread.start()

            self.is_downloading = False
    def append_file_details_to_storage(self, filename, path, address, date):
        if not path:
            path = Settings(self.parent.content_container).xengine_download_path_global## the path stored in config file

        file_details = [
            "\n",
            "<file> \n",
            f"filename: {filename}\n",
            "size:  ---\n",
            "downloaded: ---\n",
            "status: waiting...\n",
            f"date-modified: {date}\n",
            f"address: {address} \n",
            f"path: {path} \n" ,
            "</file>\n",
            "\n",
        ]

        with open('downloading_tasks.txt', 'a') as f:
            for line in file_details:
                f.write(line)

        print('Added!')

    def update_file_details_on_storage_during_download(self, filename, size, downloaded, status, date):
        file_details = []
        
        with open('downloading_tasks.txt', 'r') as f:
            entry = {}
            for line in f.readlines():
                line.strip()
                if line.startswith('<file>'):
                    entry = {}
                elif line.startswith('</file>'):
                    file_details.append(entry)
                else:
                    match = re.findall(r'\s*(\S+):\s*(.+)', line)
                    if match:
                        key, value = match[0]
                       
                        entry[key.strip()] = value.strip()

        split_name = os.path.basename(filename)
        
        with open('downloading_tasks.txt', 'w') as f:
            for entry in file_details:
                if entry.get('filename') == split_name:
                    entry['size'] = size if size != 0 else entry.get('size', '---')
                    entry['downloaded'] = downloaded
                    entry['status'] = status
                    entry['date-modified'] = date

                    

                f.write("<file>\n")
                for key, value in entry.items():
                    f.write(f"{key}: {value}\n")
                f.write("</file>\n")
                f.write("\n")

         
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
                await self.condition.wait_for(lambda : not self.links_and_filenames.empty())
               

            while not self.links_and_filenames.empty():
 
                file = await self.links_and_filenames.get()
                ## using asyncio.create-task is to be done to create new process
                ## and appending
                link, filename ,path= file  ##(adress , filename, path if chosen by default it checks for path set)

                filename = self.validate_filename(filename, path) 
                file = (link, filename, path)  ## assigning file newly updated values
                name_with_no_path = os.path.basename(filename)
                self.append_file_details_to_storage(name_with_no_path, path, link, time.strftime(r'%Y-%m-%d'))
                tasks.append(asyncio.create_task(self.start_task(file)))
                self.links_and_filenames.task_done()  
            if self.links_and_filenames.empty():
                self.is_downloading = False

            if tasks:
                asyncio.gather(*tasks)

    async def start_task(self, file): 
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
                        with open(filename, 'wb') as f:
                            start_time = time.time()
                            file_size = resp.headers.get('Content-Length', None)

                            if file_size:
                                size = int(file_size)
                                
                            else:
                                if resp.headers.get('Transfer-Encoding') == 'chunked':
                                    file_size = 'unknown'
                                else:
                                    file_size = None
                            
                            async for chunk in resp.content.iter_chunked(16*1024):
                                f.write(chunk)
                                unit_time = time.time() - start_time 
                                if not unit_time == 0:
                                    downloaded_chunk += len(chunk)
                                    down_in_mbs = int(downloaded_chunk / (1024*1024))
                                    speed = down_in_mbs / unit_time
                                    new_speed = round(speed, 3)
                                    speed = self.returnSpeed(new_speed)
                                    percentage = round((downloaded_chunk/size) * 100,0)
                                    self.update_file_details_on_storage_during_download(
                                    filename, size, downloaded_chunk, 'downloading', time.strftime(r'%Y-%m-%d')
                                )

                            new_speed = 0
                            self.update_file_details_on_storage_during_download(
                            filename, size, size, 'completed', time.strftime(r'%Y-%m-%d')
                        )
            except Exception as e:
                print(e)
                self.update_file_details_on_storage_during_download(
                filename, size, downloaded_chunk, 'failed', time.strftime('%Y-%m-%d')
                )
                        
        
