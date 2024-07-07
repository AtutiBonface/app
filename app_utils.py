from PIL import Image
from customtkinter import CTkImage, CTkFont
import customtkinter as ctk
from pathlib import Path
import os

class Images():
    def __init__(self):


        
        self.homeImg = CTkImage(Image.open('images/home.png'), size=(25,25))
        self.settingsImg = CTkImage(Image.open('images/settings.png'),  size=(25,25))
        self.downloadImg = CTkImage(Image.open('images/download.png'),  size=(25,25))
        self.aboutImg = CTkImage(Image.open('images/about.png'),  size=(25,25))
        self.folderImg = CTkImage(Image.open('images/folder.png'),  size=(25,25))
        self.close = CTkImage(Image.open('images/close.png'),  size=(15,15))
        

        self.document_d = CTkImage(Image.open('images/document_d.png'),  size=(20,20))
        self.program_d = CTkImage(Image.open('images/program_d.png'),  size=(20,20))
        self.zip_d = CTkImage(Image.open('images/zip_d.png'),  size=(20,20))
        self.music_d = CTkImage(Image.open('images/music_d.png'),  size=(20,20))
        self.video_d = CTkImage(Image.open('images/video_d.png'),  size=(20,20))

        self.document_d2 = CTkImage(Image.open('images/document_d2.png'),  size=(20,20))
        self.program_d2 = CTkImage(Image.open('images/program_d2.png'),  size=(20,20))
        self.zip_d2 = CTkImage(Image.open('images/zip_d2.png'),  size=(20,20))
        self.music_d2 = CTkImage(Image.open('images/music_d2.png'),  size=(20,20))
        self.video_d2 = CTkImage(Image.open('images/video_d2.png'),  size=(20,20))
        self.image_d2 = CTkImage(Image.open('images/image_d2.png'),  size=(20,20))

        self.pause = CTkImage(Image.open('images/pause.png'),  size=(20,20))
        self.play = CTkImage(Image.open('images/play.png'),  size=(20,20))
        self.restart = CTkImage(Image.open('images/restart.png'),  size=(20,20))
        self.stop = CTkImage(Image.open('images/stop.png'),  size=(20,20))
        self.arrowDown = CTkImage(Image.open('images/arrow_down.png'),  size=(20,20))
        self.open = CTkImage(Image.open('images/open.png'),  size=(20,20))
        self.delete = CTkImage(Image.open('images/trash.png'),  size=(20,20))
        self.link = CTkImage(Image.open('images/link.png'),  size=(15,15))


        self.close_image = CTkImage(Image.open('images/close.png'),  size=(15,15))
        self.minimize_image = CTkImage(Image.open('images/minimize.png'),  size=(15,15))


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
        x = "#48D1CC"       
        self.primary_color = '#1b1c1e'
        self.secondary_color = "#232428"
        self.text_color = '#edeef0'
        self.utils_color = x

class ConfigFilesHandler():
    def __init__(self) -> None:
        # writing config file to xengine folder at home folder

        self.path_to_config_file = f"{Path().home()}/.xengine/config.txt"

        self.settings_config = [
        "### Settings configuration for Xengine ### \n",
        "\n",
        "*Note* Do not write or edit on this file because your Xengine Downloader will be faulty! Very faulty!\n",
        "\n",
        "defaut_download_path <x:e> C:/Users/Bonface/Downloads/Xengine \n",
        "max_concurrent_downloads <x:e> 100 \n",
        "auto_resume_download <x:e> false \n",
        "overide_file <x:e> false\n",
        "show_progress_window <x:e> true\n",
        "show_download_complete_window <x:e> true \n",
        "\n",
        "extensions_link <x:e> https://xengine.imaginekenya.site/xe-extensions\n",
        "VERSION <x:e> Xengine 1.0.1 \n"
        ]

        xengine_config_path = f"{Path().home()}/.xengine"
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




