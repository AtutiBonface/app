import customtkinter as ctk
from customtkinter import CTkFont
import app_utils 
import customtkinter as ctk
from customtkinter import CTkFont
from customtkinter import filedialog
from pathlib import Path
from asyncio import Queue
import os, asyncio, threading
from urllib.parse import urlparse
from app_utils import Colors
import app_utils
      

class LinkBox():
    
            
    def __init__(self, parent, xdm_instance):
        self.xe_images = app_utils.Images()
        self.xdm_instance = xdm_instance
        self.default_download_path = f"{Path.home()}\\Downloads\\Xengine"
        self.colors = Colors()        
        
        
        self.enter_link_box = ctk.CTkFrame(parent.content_container, height=180, width=360, fg_color=self.colors.utils_color, corner_radius=10, bg_color='transparent')
       
        self.font2 =CTkFont(weight='bold', family='Helvetica', size=9)
        self.font =CTkFont(weight='bold', family='Helvetica', size=11)
        self.address_label = ctk.CTkLabel(self.enter_link_box,text_color=self.colors.text_color,  font=self.font,text='Address').place(y=45, x=20)
        self.filename_label = ctk.CTkLabel(self.enter_link_box,text_color=self.colors.text_color, font=self.font,text='Filename').place(y=80, x=20)

        self.status_label = ctk.CTkLabel(self.enter_link_box, text='', font=self.font)
        self.status_label.pack(pady=5)

        self.link_text = ctk.StringVar()
        self.filename_text = ctk.StringVar()
        self.pos = .45
        self.pos2 = 0

       

        self.link_entry = ctk.CTkEntry(self.enter_link_box, height=30, textvariable=self.link_text,font=CTkFont(weight='bold', family='Helvetica', size=10), border_width=0, corner_radius=5, placeholder_text='insert link')
        self.link_entry.pack(pady=5, fill='x', padx=70)
        self.directory_box = ctk.CTkFrame(self.enter_link_box, fg_color='transparent')
        self.filename_entry = ctk.CTkEntry(self.directory_box, border_width=0, textvariable=self.filename_text,font=CTkFont(weight='bold', family='Helvetica', size=10), placeholder_text='file name', height=25)
        self.filename_entry.pack(side='left', fill='x')
        self.change_folder_btn = ctk.CTkButton(self.directory_box, text='',command=self.openDownloadToFolder, cursor='hand2', image=self.xe_images.folderImg, fg_color=self.colors.utils_color,width=20, height=25, hover=False)
        self.change_folder_btn.pack(side='left')
        self.directory_box.pack(fill='x', padx=70)
        self.path_btn = ctk.CTkLabel(self.directory_box, text='', image=self.xe_images.arrowDown,fg_color=self.colors.utils_color,cursor='hand2', width=18, height=25,)
        self.path_btn.pack(side='left' ,ipadx=0, ipady=0)
        self.path_label = ctk.CTkLabel(self.enter_link_box, text=self.default_download_path,height=15, font=self.font2,fg_color=self.colors.utils_color, text_color=self.colors.utils_color)
        self.path_label.place(rely=.65, relx=.5, relwidth=1,anchor='center')
        self.start_download = ctk.CTkButton(self.enter_link_box,hover=False,command=self.add_task_to_downloads,  cursor='hand2', text='Download',font=CTkFont(weight='bold', family='Helvetica', size=11), width=120, height=40, corner_radius=10, fg_color=self.colors.secondary_color)
        self.start_download.pack(side='bottom' ,pady=10)

        self.enter_link_box.place(relx=.4, rely=.45, anchor='center')
        
        self.enter_link_box.pack_propagate(False)
        
        self.link_entry.bind('<KeyRelease>', self.getInputValue)

        
        self.path_btn.bind('<Enter>', self.on_enter)
        self.path_btn.bind('<Leave>', self.on_leave)
    def on_enter(self, event):
        self.path_label.configure(fg_color=self.colors.secondary_color, text_color=self.colors.text_color)

    def on_leave(self, event):
        self.path_label.configure(fg_color=self.colors.utils_color, text_color=self.colors.utils_color)

    

    def getInputValue(self, event):        
        
        link = self.link_text.get()
        filename = self.filename_text.get() 

       
        if not urlparse(link).scheme:
            link = f'http://{link}'

        url_parsed = urlparse(link)

        if os.path.basename(url_parsed.path):
            filename = os.path.basename(url_parsed.path)

            self.filename_text.set(filename)
        else:
            self.filename_text.set('FILE')


    def returnFilename(self, path):
        pass

    def openDownloadToFolder(self):
        home = Path.home()
        file_location = filedialog.askdirectory(mustexist=True,initialdir=home, title='Select Folder')

    def add_task_to_downloads(self):
        link = self.link_text.get()
        filename = self.filename_text.get() 

       
        if not urlparse(link).scheme:
            link = f'http://{link}'

        if not urlparse(link).netloc:
            self.status_label.configure(text='Insert correct address!', text_color='brown')


        
        else:
            url_parsed = urlparse(link)

            if '.' in link:
                
                initial_filename = self.filename_text.get()
                name, extension = os.path.splitext(initial_filename)

                if not extension:
                    extension = '.html'
                if not name:
                    self.status_label.configure(text=f'No file name!', text_color='brown')
                 
                else:
                    filename_and_path = name + extension
                    
                    filename = os.path.basename(filename_and_path)

                    self.selected_filename = filename
                    self.selected_link = link


                    
                    
                    if self.xdm_instance.is_downloading:
                        
                        self.xdm_instance.addQueue((link , filename))
                        self.status_label.configure(text="Task Added!")


                    else:                        
                        self.theThread((link, filename))
                        self.status_label.configure(text="Started Downloading")


                    self.enter_link_box.after(2000, self.self_destruct)

    def self_destruct(self):
        if self.pos > 0: 
            self.enter_link_box.place(relx=.4, rely=self.pos, anchor='center')
            self.pos -= 0.05
            self.enter_link_box.after(10, self.self_destruct)
        else:
            self.enter_link_box.destroy()  
    def theThread(self, file):
        my_thread = threading.Thread(target=lambda: self.startTask(file), daemon=True)
        my_thread.start()

    def startTask(self, file):         
        
        asyncio.run(self.xdm_instance.main(file))
       
                    

                    

   
    
            


           
            

