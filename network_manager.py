import os, asyncio,aiohttp, ssl, certifi, time, threading, re
from asyncio import Queue 
from settings import Settings
import aiofiles, database
from pathlib import Path
import shutil, m3u8
from app_utils import OtherMethods
from urllib.parse import urlparse, urlunparse, urljoin

class NetworkManager:
    def __init__(self, config):
        self.config = config
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'identity;q=1, *;q=0',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

       
        self.ssl_context = ssl.create_default_context(cafile=certifi.where())
        self.connector = aiohttp.TCPConnector(ssl=self.ssl_context, limit=None)

    async def create_session(self):
        return aiohttp.ClientSession(connector=self.connector, headers=self.headers, timeout=aiohttp.ClientTimeout(total=None))


    async def fetch_segment(self, session, url, start, end, total_segments, filename, segment_id, original_filesize):
        pass

    async def download_m3u8_segment(self, session, url, filename, seg_no, headers, original_filesize):
        pass