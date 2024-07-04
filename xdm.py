import os, asyncio,aiohttp, ssl, certifi, time, threading
from asyncio import Queue


class TaskManager():
    def __init__(self, parent) -> None:
            
           
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            self.name = ''
            self.links_and_filenames = Queue()
            self.ui_files = []

            self.ui_callback = parent.update_ui

            self.loop = asyncio.new_event_loop()
            self.download_thread = threading.Thread(target=self.download_task_manager, daemon=True)
            self.download_thread.start()

            self.is_downloading = False
    def download_task_manager(self):
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
        

    ## this adds index to file name if file exists
    def validate_filename(self, filename):
        index = 1
        name, extension = os.path.splitext(filename)

        new_name = filename

        while os.path.exists(new_name):
            new_name = f'{name}_{index}{extension}'
            index += 1

        return new_name
    async def download_tasks(self):
        while True:
            self.is_downloading = True
            file = await self.links_and_filenames.get()
            await self.start_task(file)
            self.links_and_filenames.task_done()  
            if self.links_and_filenames.empty():
                self.is_downloading = False

    async def start_task(self, file): 
        link, filename = file
        self.timeout = aiohttp.ClientTimeout(total=None)
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        async with aiohttp.ClientSession(connector=self.connector, headers=self.headers,timeout=self.timeout) as session:
            filename = self.validate_filename(filename)      
            async with session.get(link) as resp:
                if resp.status == 200:
                    with open(filename, 'wb') as f:
                        
                        downloaded_chuck = 0
                        start_time = time.time()
                        speed = 0
                        size = 10
                        complete = 50
                        file_type = 'Video'
            
                        async for chunk in resp.content.iter_chunked(8*1024):
                            f.write(chunk)
                            unit_time = time.time() - start_time 
                            if not unit_time == 0:
                                downloaded_chuck += len(chunk)
                                down_in_mbs = int(downloaded_chuck / (1024*1024))
                                speed = down_in_mbs / unit_time
                                new_speed = round(speed, 3)
                                speed = self.returnSpeed(new_speed)
                                self.ui_callback(filename, size, complete, speed, file_type)

                        new_speed = 0
                        print("Finished !")
                        

                    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    async def main(self, file):
        self.is_downloading = True
        self.files = []
        await self.links_and_filenames.put(file) 
               
        for i in range(self.links_and_filenames.qsize()):
            item = await self.links_and_filenames.get()
            self.links_and_filenames.task_done()
        self.files.append(item)
       
            
        self.timeout = aiohttp.ClientTimeout(total=None)
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context)
        async with aiohttp.ClientSession(connector=self.connector, headers=self.headers,timeout=self.timeout) as session:
            tasks = []
            for file in self.files:
                link, filename = file
                
                tasks.append(self.startDownloading(session, link, filename))

            results = await asyncio.gather(*tasks)

            
            
            

    async def startDownloading(self, session, link, filename):
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context) 
        filename = self.validate_filename(filename)      
        async with session.get(link) as resp:
            if resp.status == 200:
                with open(filename, 'wb') as f:
                    
                    downloaded_chuck = 0

                    start_time = time.time()

                    speed = 0
                    size = 10

                    complete = 50
                    file_type = 'Video'
        
                    async for chunk in resp.content.iter_chunked(8*1024):
                        
                        f.write(chunk)
                        
                        unit_time = time.time() - start_time 
                        if not unit_time == 0:
                            downloaded_chuck += len(chunk)

                            down_in_mbs = int(downloaded_chuck / (1024*1024))

                            speed = down_in_mbs / unit_time

                            new_speed = round(speed, 3)
                            

                            speed = self.returnSpeed(new_speed)
                            
                            self.ui_callback(filename, size, complete, speed, file_type)
                    new_speed = 0
                    print("Finished !")
                        

                    

