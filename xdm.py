import os, asyncio,aiohttp, ssl, certifi, time
from asyncio import Queue
from downloading_page import DownloadingPage

class TaskManager():
    def __init__(self) -> None:
            
           
            self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            self.name = ''
            self.links_and_filenames = Queue()
            self.ui_files = []

            self.is_downloading = False

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
    def addQueue(self, file):
        self.links_and_filenames.put_nowait(file)
        print("Data is added")
        
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
                            
                            print(filename, size, complete, speed, file_type)
                    new_speed = 0
                    print("Finished !")
                        

                    

