import os, asyncio, aiohttp, ssl, certifi, time
import aiofiles, m3u8
from pathlib import Path
from app_utils import OtherMethods
from urllib.parse import urlparse, urlunparse, urljoin

class NetworkManager:
    def __init__(self, config, task_manager):
        self.config = config
        self.other_methods = OtherMethods()
        self.task_manager = task_manager
        
        # Default headers to mimic a browser's behavior
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'identity;q=1, *;q=0',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }
        
        # SSL context to use certifi's certificates
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context, limit=None)

    async def create_session(self, connector):
        # Create an aiohttp session with a custom connector and headers
        return aiohttp.ClientSession(connector=connector, headers=self.headers, timeout=aiohttp.ClientTimeout(total=None))
    
    async def fetch_m3u8_segment_size(self, session, url):
        # Fetch the size of a single m3u8 segment by checking the Content-Length header
        async with session.get(url) as response:
            if response.status == 200 and 'Content-Length' in response.headers:
                return int(response.headers['Content-Length'])
            else:
                return 0  # Return 0 if the size is not available

    async def get_total_size_of_m3u8(self, session, m3u8_url, baseurl):
        # Download and parse the m3u8 playlist
        async with session.get(m3u8_url) as response:
            m3u8_content = await response.text()
            playlist = m3u8.loads(m3u8_content)

        # Extract segment URLs and create a list of tasks to fetch segment sizes concurrently
        segment_urls = [urljoin(baseurl, segment.uri) for segment in playlist.segments]
        tasks = [self.fetch_m3u8_segment_size(session, segment_url) for segment_url in segment_urls]
        segment_sizes = await asyncio.gather(*tasks)

        return sum(segment_sizes)  # Return the total size of all segments
    
    async def get_filename_from_m3u8_content(self, session, f_path, url, filename):
        # Determine the final filename based on the m3u8 content's MIME type
        name, _ = os.path.splitext(filename)

        async with session.get(url) as response:
            if response.status == 200 and 'Content-Type' in response.headers:
                return self.task_manager.return_filename_with_extension(f_path, name, response.headers.get('Content-Type', ''))
            else:
                return self.task_manager.return_filename_with_extension(f_path, name,  '')

    async def fetch_segment(self, session, url, start, end, total_segments, filename, segment_id, original_filesize):
        # Download a single segment of the m3u8 file, with retry logic
        
        # List of user agents to rotate between requests
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0'
        ]
                
        max_retries = 5  # Maximum number of retries
        retry_delay = 1  # Initial delay between retries
        segment_downloaded = 0
        success = False  # Flag to check if the download was successful
        
        # Create temporary folder for storing segments
        basename = os.path.basename(filename)
        tem_folder = f"{Path().home()}/.blackjuice/temp/.{basename}"
        try:
            os.makedirs(tem_folder, exist_ok=True)
        except Exception as e:
            print(e)

        # Save the segment to a temporary file
        segment_filename = f'{tem_folder}/part{segment_id}'


        if os.path.exists(segment_filename):
            segment_downloaded = os.path.getsize(segment_filename)
            start += segment_downloaded

        for attempt in range(max_retries):
            try:
                # Set headers for the request, including referer and user agent
                referer = self.other_methods.get_base_url(url)
                headers = self.headers.copy()
                headers['Referer'] = referer 
                headers['User-Agent'] = user_agents[attempt % len(user_agents)] 

                # Set range header for partial content
                if segment_id + 1 == total_segments:  # Checks if it is the last segment 
                    headers['Range'] = f'bytes={start}-'
                else:
                    headers['Range'] = f'bytes={start}-{end}'

                if segment_downloaded > 0 and os.path.exists(segment_filename):
                    start += segment_downloaded

                # Send the request to fetch the segment
                async with session.get(url, headers=headers) as response:
                    if response.status in (200, 206):  # Partial Content

                        
                        mode = 'ab' if segment_downloaded > 0 else 'wb'
                        async with aiofiles.open(segment_filename, mode) as f:
                            async for chunk in response.content.iter_chunked(self.config.CHUNK_SIZE):
                                await f.write(chunk)

                                # Update the downloaded size
                                chunk_size = len(chunk)
                                segment_downloaded += chunk_size


                                # Lock and update UI for download progress
                                async with self.task_manager.lock:
                                    if filename in self.task_manager.size_downloaded_dict:
                                        self.task_manager.size_downloaded_dict[filename][0] += len(chunk)
                                    else:
                                        self.task_manager.size_downloaded_dict[filename] = [len(chunk), time.time()]

                                await self.task_manager._handle_segments_downloads_ui(filename, url, original_filesize)

                        success = True  # Mark download as successful
                        break
                    elif response.status == 416:
                        print(f"Segment {segment_id} already fully downloaded")
                        success = True
                        break
                    else:
                        print(f"Unexpected status {response.status} for segment {segment_id}")
                        await asyncio.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, 256)

            except aiohttp.ClientError as e:
                print('Error 1', e)
                # Handle aiohttp client errors and retry
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 256)

            except Exception as e:
                print('Error 2', e)
                # Handle other exceptions and retry
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 256)

        if not success:
            print(f"Segment {segment_id} failed after {max_retries} attempts")

    async def download_m3u8_segment(self, session, url, filename, seg_no, headers, original_filesize):
        # Download a single m3u8 segment with retry logic
        max_retries = 5  # Maximum number of retries
        retry_delay = 1  # Initial delay between retries
        segment_downloaded = 0
        success = False  # Flag to check if the download was successful
        
        basename = os.path.basename(filename)
        tem_folder = f"{Path().home()}/.blackjuice/temp/.{basename}"
        try:
            os.makedirs(tem_folder, exist_ok=True)
        except Exception as e:
            print(e)

        segment_filename = f'{tem_folder}/part{seg_no}'

        if os.path.exists(segment_filename):
            segment_downloaded = os.path.getsize(segment_filename)

        # Save the segment to a temporary file

        for attempt in range(max_retries): 
            try:
                if segment_downloaded > 0:
                    headers['Range'] = f'bytes={segment_downloaded}-'
                else:
                    headers.pop('Range', None)  # Remove Range header for full download

                # Send the request to fetch the segment
                async with session.get(url, headers=headers) as resp:
                    if resp.status in (206, 200):
                        mode = 'ab' if segment_downloaded > 0 else 'wb'
                        async with aiofiles.open(segment_filename, mode) as file:
                            async for chunk in resp.content.iter_chunked(self.config.CHUNK_SIZE):
                                await file.write(chunk)

                                # Update the downloaded size
                                chunk_size = len(chunk)
                                segment_downloaded += chunk_size
                                # Lock and update UI for download progress
                                async with self.task_manager.lock:
                                    if filename in self.task_manager.size_downloaded_dict:
                                        self.task_manager.size_downloaded_dict[filename][0] += len(chunk)
                                    else:
                                        self.task_manager.size_downloaded_dict[filename] = [len(chunk), time.time()]

                                await self.task_manager.progress_manager._handle_segments_downloads_ui(filename, url, original_filesize)

                        success = True  # Mark download as successful
                        break
                    elif resp.status == 416:
                        print(f"Segment {seg_no} already fully downloaded")
                        success = True
                        break
                    else:
                        print(f"Unexpected status {resp.status} for segment {seg_no}")
                        await asyncio.sleep(retry_delay)
                        retry_delay = min(retry_delay * 2, 256)

            except aiohttp.ContentTypeError as e:
                
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 256)

            except ConnectionResetError as e:
                print(f"ConnectionResetError in segment {seg_no}: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 256)

            except aiohttp.ClientError as e:
                print(f"ClientError in segment {seg_no}: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 256)

            except Exception as e:
                print(f"Error in segment {seg_no}: {e}")
                await asyncio.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 256)

        if not success:
            print(f"Segment {seg_no} failed after {max_retries} attempts")
