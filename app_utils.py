from PIL import Image
from customtkinter import CTkImage, CTkFont
import customtkinter as ctk
from pathlib import Path
import os, sys

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


        self.close_image = CTkImage(Image.open(self.resource_path('images/close.png')),  size=(15,15))
        self.minimize_image = CTkImage(Image.open(self.resource_path('images/minimize.png')),  size=(15,15))

        self.sub_logo = CTkImage(Image.open(self.resource_path('xe-logos/xe-128.png')),  size=(25,25))


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

        
class ConfigFilesHandler():

    def __init__(self) -> None:
        # writing config file to BlackJuice folder at home folder

        self.path_to_config_file = f"{Path().home()}/.blackjuice/config.txt"
        
        self.settings_config = [
        "### Settings configuration for Blackjuice ### \n",
        "\n",
        "*Note* Do not write or edit on this file because your Blackjuice Downloader will be faulty! Very faulty!\n",
        "\n",
        "defaut_download_path <x:e> C:/Users/Bonface/Downloads/Blackjuice \n",
        "max_concurrent_downloads <x:e> 100 \n",
        "auto_resume_download <x:e> false \n",
        "overide_file <x:e> false\n",
        "show_progress_window <x:e> true\n",
        "show_download_complete_window <x:e> true \n",
        "\n",
        "extensions_link <x:e> https://blackjuice.imaginekenya.site/xe-extensions\n",
        "VERSION <x:e> blackjuice 1.0.1 \n"
        ]

        xengine_config_path = f"{Path().home()}/.blackjuice"
        file = 'config.txt'

        try:           
            os.makedirs(xengine_config_path)
            

            with open(f"{xengine_config_path}/{file}", 'w') as f:
                for line in self.settings_config:
                    f.write(line)

        except FileExistsError:
            pass
        except Exception as e:
            pass



class OtherMethods():
    
    def return_filesize_in_correct_units(self, filesize):
        try:
            filesize = int(filesize)
            if filesize > (1024*1024*1024):
                return f'{round(filesize/10**9,2)} GB' 
            
            elif filesize > (1024*1024):
                return f'{round(filesize/10**6,2)} MB' 
            
            elif filesize > (1024):
                return f'{round(filesize/10**3,2)} Kbs' 
            else: 
                return f'{round(filesize,1)} bytes' 
        except Exception as e:
            return '---'
    
    def return_file_type(self, filename):
        xe_images = Images()

        name , extension = os.path.splitext(filename)
        extension = extension.lower()# converting all extensions to lower case
        video_extensions = {'.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.webm'}
        audio_extensions = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'}
        document_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.odt', '.ods', '.odp','.html', '.htm'}
        program_extensions = {'.exe', '.msi', '.bat', '.sh', '.py', '.jar', '.bin'}
        compressed_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'}

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
    

    

        
       



