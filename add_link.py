import customtkinter as ctk
from customtkinter import CTkFont
import app_utils 
from progress import Progressor
import customtkinter as ctk
from customtkinter import CTkFont
from customtkinter import filedialog
from pathlib import Path
from asyncio import Queue
import os, asyncio, threading
from urllib.parse import urlparse
from app_utils import Colors
import app_utils , re

      

class LinkBox(ctk.CTkToplevel):
    def self_destruct(self):
        self.destroy()
            
    def __init__(self, parent, xdm_instance):
        super().__init__(parent)
       
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        half_w = int((width/2))
        half_h = int((height/2))
        
        self.geometry(f'+{half_w}+{half_h}')

        self.update()
        self.update_idletasks()
        self.dropdown_is_open = False

        
      
        self.colors = Colors() 
        self.parent = parent  
        self.xe_images = app_utils.Images()
        self.xdm_instance = xdm_instance
        self.default_download_path = f"{Path.home()}\\Downloads\\BlackJuice"
        self.selected_path = None
        self.save_at_variable = ctk.StringVar()
        self.save_at_variable.set(self.default_download_path)

        self.enter_link_box = ctk.CTkFrame(self, height=220, width=400, fg_color=self.colors.utils_color, corner_radius=5, bg_color='transparent')
        self.font2 =CTkFont(weight='bold', family='Helvetica', size=9)
        self.font =CTkFont(weight='bold', family='Helvetica', size=11)
        self.address_label = ctk.CTkLabel(self.enter_link_box,text_color=self.colors.text_color,  font=self.font,text='Address').place(y=63, x=10)
        self.filename_label = ctk.CTkLabel(self.enter_link_box,text_color=self.colors.text_color, font=self.font,text='File').place(y=92, x=15)
        self.save_in_label = ctk.CTkLabel(self.enter_link_box,text_color=self.colors.text_color, font=self.font,text='Save in').place(y=124, x=10)
        
        self.title_bar = ctk.CTkFrame(self.enter_link_box, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.logo = ctk.CTkLabel(self.title_bar,text='', width=25, cursor='hand2',fg_color='transparent',  height=25, image=self.xe_images.sub_logo )
        self.logo.place(x=5, y=2.5,anchor='nw' )
        self.status_label = ctk.CTkLabel(self.enter_link_box, text='', font=self.font)
        self.status_label.pack()

        self.link_text = ctk.StringVar()
        self.filename_text = ctk.StringVar()
        self.pos = .45
        self.pos2 = 0

        self.close = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command=self.self_destruct, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close )
        self.close.place(x=395, y=5,anchor='ne' )
        self.link_entry = ctk.CTkEntry(self.enter_link_box, height=30, textvariable=self.link_text,font=CTkFont(weight='bold', family='Helvetica', size=10), border_width=0, corner_radius=3, placeholder_text='insert link')
        self.link_entry.pack(pady=2, fill='x', padx=60)
        
        self.filename_entry = ctk.CTkEntry(self.enter_link_box, border_width=0, textvariable=self.filename_text,font=CTkFont(weight='bold', family='Helvetica', size=10), placeholder_text='file name', height=25, corner_radius=3)
        self.filename_entry.pack(pady=2, fill='x', padx=60)        

        self.save_at_container = ctk.CTkFrame(self.enter_link_box, fg_color='transparent', height=25)
        self.save_at_entry = ctk.CTkEntry(self.save_at_container, border_width=0, textvariable=self.save_at_variable,font=CTkFont(weight='bold', family='Helvetica', size=10), placeholder_text='save at', height=25, corner_radius=3)
        self.save_at_entry.pack(pady=2,side='left', fill='x', expand=True)
        self.save_at_dropdown_btn = ctk.CTkButton(self.save_at_container, text='',command=self.open_save_at_dropdown, image=self.xe_images.arrowDown,cursor='hand2', width=20, height=20, hover=False, fg_color=self.colors.secondary_color, corner_radius=5)
        self.save_at_dropdown_btn.pack(side='left')
        self.save_at_container.pack(fill='x', padx=60)
        self.save_at_container.pack_propagate(False)




        self.start_download = ctk.CTkButton(self.enter_link_box,hover=False,command=self.add_task_to_downloads,  cursor='hand2', text='Download',font=CTkFont(weight='bold', family='Helvetica', size=11), width=120, height=40, corner_radius=5, fg_color=self.colors.secondary_color)
        self.start_download.pack(side='bottom' ,pady=10)

        

        self.save_at_dropdown = ctk.CTkFrame(self.enter_link_box,width=280, fg_color=self.colors.secondary_color, corner_radius=5, height=60)
        self.enter_link_box.pack()
        
        self.enter_link_box.pack_propagate(False)
        
        self.link_entry.bind('<KeyRelease>', self.getInputValue)

        
        
        self.title_bar.bind('<ButtonPress-1>', self.set_mouse_pos)
        self.title_bar.bind('<B1-Motion>', self.drag_container)

    def open_save_at_dropdown(self):
        
        if not self.dropdown_is_open:
            self.save_at_dropdown = ctk.CTkFrame(self.enter_link_box,width=280, fg_color=self.colors.secondary_color, corner_radius=5, height=60)
            self.browse_btn = ctk.CTkButton(self.save_at_dropdown,height=25, command=self.openDownloadToFolder,text='Browse...',font=CTkFont(weight='bold', family='Helvetica', size=10), fg_color='transparent',hover_color=self.colors.primary_color,corner_radius=5, cursor='hand2',anchor='w')
            self.browse_btn.pack(fill='x', pady=2, padx=5)
            self.default_path_btn = ctk.CTkButton(self.save_at_dropdown,height=25,command=self.setDownloadFolderToDefault, text=self.default_download_path,font=CTkFont(weight='bold', family='Helvetica', size=10), fg_color=self.colors.primary_color,hover_color=self.colors.primary_color,corner_radius=5, cursor='hand2',anchor='w' )
            self.default_path_btn.pack(fill='x', padx=5)
            self.save_at_dropdown.place(x=60, y=148)
            self.save_at_dropdown.pack_propagate(False)
            
        self.dropdown_is_open = True
    def drag_container(self, event):
        x = self.winfo_pointerx() -self.x_offset
        y = self.winfo_pointery() - self.y_offset

        self.geometry(f'+{x}+{y}')
    def set_mouse_pos(self, event):

        self.x_offset = event.x
        self.y_offset = event.y
   

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
            custom_name = link.split('//')[1].split('.')[0]
            self.filename_text.set(custom_name)

    def setDownloadFolderToDefault(self):
        self.save_at_variable.set(self.default_download_path)
        if self.save_at_dropdown.winfo_exists():
            self.save_at_dropdown.destroy()

        self.dropdown_is_open = False


    def openDownloadToFolder(self):
              
        home = Path.home()
        file_location = filedialog.askdirectory(mustexist=True,initialdir=home, title='Select Folder', parent=self)
        if file_location:
            self.selected_path = file_location
            self.save_at_variable.set(file_location)
        else:
            self.selected_path = None
        
        if self.save_at_dropdown.winfo_exists():
            self.save_at_dropdown.destroy()  

        self.dropdown_is_open = False

    def sanitize_filename(self, filename):
        # Remove any invalid characters for filenames on most operating systems
        return re.sub(r'[\\/*?:"<>|]', "", filename)

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

                
                if not name:
                    self.status_label.configure(text=f'No file name!', text_color='brown')
                 
                else:
                    name = self.sanitize_filename(name)# removes \\/*?:"<>| which are invalid characters

                    filename_and_path = name + extension
                    
                    filename = os.path.basename(filename_and_path)

                    

                    self.selected_filename = filename
                    self.selected_link = link
                    
                    ## adds link filename and path if selected to a queue
                    asyncio.run_coroutine_threadsafe(self.xdm_instance.addQueue((link, filename, self.selected_path)),self.xdm_instance.loop)
                    
                    if self.xdm_instance.is_downloading:
                        
                        self.status_label.configure(text="Task Added!")

                    else:                        
                        self.status_label.configure(text="Started Downloading")

                    self.selected_path = None # resets path stored
                    self.destroy()## once link is added the add_link is destroyed while the process toplevel is packed
                    

                    



                    


                    

             

                    

   
    
            


           
            

