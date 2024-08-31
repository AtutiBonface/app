from PIL import Image
from customtkinter import CTkImage, CTkFont
import customtkinter as ctk
from pathlib import Path
import os, sys, logging
from urllib.parse import urljoin, urlparse, urlunparse 

class Images():
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    def __init__(self):


        
        self.homeImg = CTkImage(Image.open(self.resource_path('images/home.png')), size=(25,25))
        self.settingsImg = CTkImage(Image.open(self.resource_path('images/settings.png')),  size=(25,25))
        self.downloadImg = CTkImage(Image.open(self.resource_path('images/download.png')),  size=(25,25))
        self.aboutImg = CTkImage(Image.open(self.resource_path('images/about.png')),  size=(25,25))
        self.folderImg = CTkImage(Image.open(self.resource_path('images/folder.png')),  size=(20,20))
        self.close = CTkImage(Image.open(self.resource_path('images/close.png')),  size=(15,15))
        

        self.document_d = CTkImage(Image.open(self.resource_path('images/document_d.png')),  size=(20,20))
        self.program_d = CTkImage(Image.open(self.resource_path('images/program_d.png')),  size=(20,20))
        self.zip_d = CTkImage(Image.open(self.resource_path('images/zip_d.png')),  size=(20,20))
        self.music_d = CTkImage(Image.open(self.resource_path('images/music_d.png')),  size=(20,20))
        self.video_d = CTkImage(Image.open(self.resource_path('images/video_d.png')),  size=(20,20))

        self.document_d2 = CTkImage(Image.open(self.resource_path('images/document_d2.png')),  size=(20,20))
        self.program_d2 = CTkImage(Image.open(self.resource_path('images/program_d2.png')),  size=(20,20))
        self.zip_d2 = CTkImage(Image.open(self.resource_path('images/zip_d2.png')),  size=(20,20))
        self.music_d2 = CTkImage(Image.open(self.resource_path('images/music_d2.png')),  size=(20,20))
        self.video_d2 = CTkImage(Image.open(self.resource_path('images/video_d2.png')),  size=(20,20))
        self.image_d2 = CTkImage(Image.open(self.resource_path('images/image_d2.png')),  size=(20,20))

        self.pause = CTkImage(Image.open(self.resource_path('images/pause.png')),  size=(20,20))
        self.play = CTkImage(Image.open(self.resource_path('images/play.png')),  size=(20,20))
        self.restart = CTkImage(Image.open(self.resource_path('images/restart.png')),  size=(20,20))
        self.stop = CTkImage(Image.open(self.resource_path('images/stop.png')),  size=(20,20))
        self.arrowDown = CTkImage(Image.open(self.resource_path('images/arrow_down.png')),  size=(15,15))
        self.open = CTkImage(Image.open(self.resource_path('images/open.png')),  size=(20,20))
        self.delete = CTkImage(Image.open(self.resource_path('images/trash.png')),  size=(20,20))
        self.more = CTkImage(Image.open(self.resource_path('images/more.png')),  size=(20,20))
        self.link = CTkImage(Image.open(self.resource_path('images/link.png')),  size=(15,15)) 
        self.checked = CTkImage(Image.open(self.resource_path('images/checked_enabled.png')),  size=(15,15))

        self.close_image = CTkImage(Image.open(self.resource_path('images/close.png')),  size=(15,15))
        self.minimize_image = CTkImage(Image.open(self.resource_path('images/minimize.png')),  size=(15,15))

        self.sub_logo = CTkImage(Image.open(self.resource_path('xe-logos/xe-128.png')),  size=(25,25))

        self.huge_logo = CTkImage(Image.open(self.resource_path('xe-logos/xe-128.png')),  size=(100,100))


        self.logo = Image.open(self.resource_path('xe-logos/xe-128.png'))


class DownloadingIndicatorBox():
    def __init__(self, parent):
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12 = CTkFont(weight='bold', family='Helvetica', size=10) 
        self.container = ctk.CTkFrame(parent.content_container, width=150, height=60, fg_color='#3d539f', bg_color='#edeef0', corner_radius=20)
        self.my_canvas = ctk.CTkCanvas(self.container, height=60, width=60,bg='#3d539f', highlightbackground='#3d539f', highlightcolor='#3d539f', insertbackground='#3d539f' )
        self.my_canvas.place(x=15,y=13)

        self.info = ctk.CTkLabel(self.container, text='Task is \n Downloading', font=self.font12, text_color='white')
        self.info.place(x=60, y=10)
        self.container.place(relx = .97, rely=.82, anchor='ne')
        self.container.pack_propagate(False)

        self.my_canvas.create_oval(5, 5 ,55, 55,width=5, outline='#edeef0')
        self.my_canvas.create_arc(5,5, 55, 55, start=90, extent=-320, width=5, outline='#5b74d8', style=ctk.ARC)
        self.my_canvas.create_text(30, 30, text='90%', fill='white',font=CTkFont(weight='bold', family='Helvetica', size=14))

class Colors():
    def __init__(self) -> None: 
          
        self.primary_color = '#1b1c1e'
        self.secondary_color = "#232428"
        self.text_color = '#edeef0'
        self.utils_color ="#48D1CC"

        
class ConfigFilesHandler:
    def __init__(self) -> None:
        # Define the path to the config file
        self.path_to_config_file = Path.home() / ".blackjuice" / "config.txt"

        self.defaut_download_path = Path.home() / "Downloads" / "blackjuice"

    def create_config_file(self):
        self.settings_config = [
            "### Settings configuration for Blackjuice ### \n",
            "\n",
            "*Note* Do not write or edit this file because your Blackjuice Downloader will be faulty! Very faulty!\n",
            "\n",
            f"default_download_path <x:e> {self.defaut_download_path} \n",
            "max_concurrent_downloads <x:e> 5 \n",
            "auto_resume_download <x:e> false \n",
            "override_file <x:e> false\n",
            "show_progress_window <x:e> true \n",
            "show_download_complete_window <x:e> true \n",
            "\n",
            "extensions_link <x:e> https://blackjuice.imaginekenya.site/addons\n",
            "VERSION <x:e> blackjuice 2.0 \n"
        ]

        try:
           
            if not self.path_to_config_file.parent.exists():
                self.path_to_config_file.parent.mkdir(parents=True, exist_ok=True)

            # Check if the config file already exists
            if not self.path_to_config_file.exists():
                # Write the settings to the config file if it doesn't exist
                with self.path_to_config_file.open('w') as f:
                    f.writelines(self.settings_config)
            

        except Exception as e:
            # Configure logging
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            # Log the exception
            logger.error(f"An error occurred: {e}")

class OtherMethods():

    def get_base_url(self, url):
        parsed_url = urlparse(url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '/', '', '', ''))
        return base_url
    
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
        
    def get_m3u8_in_link(self, link):
        pursed_url = urlparse(link)

        file_path = pursed_url.path

        return file_path.lower().endswith('.m3u8')
    
    def return_filesize_in_correct_units(self, filesize):
       
        try:
            filesize = int(filesize)
            if filesize >= (1024*1024*1024):  # For GB
                return f'{round(filesize / (1024**3), 2)} GB'
            elif filesize >= (1024*1024):  # For MB
                return f'{round(filesize / (1024**2), 2)} MB'
            elif filesize >= 1024:  # For KB
                return f'{round(filesize / 1024, 2)} KB'
            else:  # For bytes
                return f'{filesize} bytes'
        except Exception as e:
            return '---'
    
    def return_file_type(self, filename):
        xe_images = Images()

        name , extension = os.path.splitext(filename)
        extension = extension.lower()# converting all extensions to lower case
        video_extensions = {
            '.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.webm', 
            '.mpg', '.mpeg', '.3gp', '.m4v', '.ts', '.ogv', '.vob'
        }

        audio_extensions = {
            '.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma', 
            '.aiff', '.alac', '.opus', '.amr', '.mid', '.midi'
        }

        document_extensions = {
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', 
            '.txt', '.odt', '.ods', '.odp', '.html', '.htm', 
            '.rtf', '.csv', '.xml', '.xhtml', '.epub', '.md'
        }

        program_extensions = {
            '.exe', '.msi', '.bat', '.sh', '.py', '.jar', '.bin', 
            '.cmd', '.csh', '.pl', '.vb', '.wsf', '.vbs'
        }

        compressed_extensions = {
            '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', 
            '.xz', '.iso', '.dmg', '.tgz', '.z', '.lzma'
        }

        image_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', 
            '.svg', '.webp', '.ico', '.heic', '.heif', '.psd'
        }


        if extension in video_extensions:
            return xe_images.video_d2
        elif extension in document_extensions:
            return xe_images.document_d2
        elif extension in program_extensions:
            return xe_images.program_d2
        elif extension in audio_extensions:
            return xe_images.music_d2
        elif extension in compressed_extensions:
            return xe_images.zip_d2
        elif extension in image_extensions:
            return xe_images.image_d2
        else: return xe_images.document_d2


    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    

    content_type_to_extension = {
            # Text types
            'text/html': '.html',
            'text/plain': '.txt',
            'text/css': '.css',
            'text/csv': '.csv',
            'text/javascript': '.js',

            # Image types
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif',
            'image/bmp': '.bmp',
            'image/webp': '.webp',
            'image/tiff': '.tiff',
            'image/svg+xml': '.svg',
            'image/x-icon': '.ico',

            # Audio types
            'audio/mpeg': '.mp3',
            'audio/wav': '.wav',
            'audio/ogg': '.ogg',
            'audio/midi': '.midi',
            'audio/x-aiff': '.aiff',

            # Video types
            'video/mp4': '.mp4',
            'video/x-msvideo': '.avi',
            'video/x-ms-wmv': '.wmv',
            'video/quicktime': '.mov',
            'video/webm': '.webm',
            'video/x-flv': '.flv',
            'video/mpeg': '.mpeg',

            'application/vnd.apple.mpegurl': '.m3u8',    # HLS master playlist
            'application/x-mpegURL': '.m3u8',            # HLS media playlist
            'video/mp2t': '.ts',                         # MPEG-2 Transport Stream
            'video/mp4': '.mp4',                         # MP4 segments
            'audio/aac': '.aac',                         # AAC audio segments
            'video/webm': '.webm',                       # WebM segments
            'video/ogg': '.ogv',                         # Ogg Video segments
            'audio/webm': '.weba',                       # WebM audio segments
            'audio/ogg': '.oga',                         # Ogg Audio segments

            # Application types
            'application/json': '.json',
            'application/pdf': '.pdf',
            'application/zip': '.zip',
            'application/x-tar': '.tar',
            'application/x-gzip': '.gz',
            'application/x-7z-compressed': '.7z',
            'application/x-rar-compressed': '.rar',
            'application/msword': '.doc',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'application/vnd.ms-excel': '.xls',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
            'application/vnd.ms-powerpoint': '.ppt',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
            'application/x-www-form-urlencoded': '.urlencoded',
            'application/octet-stream': '',  # Generic binary file
            'application/xml': '.xml',
            'application/xhtml+xml': '.xhtml',
            'application/x-shockwave-flash': '.swf',
            'application/java-archive': '.jar',
            'application/x-msdownload': '.exe',
            'application/x-bittorrent': '.torrent',

            # Multipart types
            'multipart/form-data': '',
            'multipart/byteranges': '',
            
            # Other types
            'application/rtf': '.rtf',
            'application/postscript': '.ps',
            'application/x-iso9660-image': '.iso',
            'application/x-dosexec': '.exe',
            'application/vnd.android.package-archive': '.apk',
            'application/x-apple-diskimage': '.dmg',
            'application/x-csh': '.csh',
            'application/x-perl': '.pl',
            'application/x-python-code': '.pyc',
            'application/x-httpd-php': '.php',
            'application/x-sh': '.sh',
            'application/pgp-signature': '.sig',
            'application/vnd.oasis.opendocument.text': '.odt',
            'application/vnd.oasis.opendocument.spreadsheet': '.ods',
            'application/x-font-ttf': '.ttf',
            'application/x-font-woff': '.woff',
            'application/x-font-woff2': '.woff2',


            
        }

            

            

                
            



