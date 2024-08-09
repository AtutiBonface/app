import os, asyncio,aiohttp, ssl, certifi, time, threading, re
from asyncio import Queue 
from settings import Settings
import aiofiles, database
from pathlib import Path
import shutil, m3u8
from app_utils import OtherMethods
from urllib.parse import urlparse, urlunparse, urljoin



class Config:
    CHUNK_SIZE = 256 * 1024  # 256 kb
    SEGMENT_SIZE = 10 * 1024 * 1024  # 10 MB segments
    PROGRESS_UPDATE_INTERVAL = 1024 * 1024
    MAX_CONCURRENT_DOWNLOADS = 5
    RETRY_ATTEMPTS = 3
    CONCURRENCY_DELAY = 0.1


