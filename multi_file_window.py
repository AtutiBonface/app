from typing import Tuple
import customtkinter as ctk
from tkinter import filedialog
from app_utils import Colors, Images
from customtkinter import CTkFont
import asyncio, time,re, os
from urllib.parse import urlparse

class FileAddedWidget(ctk.CTkFrame):
    def __init__(self, master, file_name, file_url, file_size, **kwargs):
        super().__init__(master, height=50, corner_radius=5 ,fg_color="#1b1c1e",**kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.images = Images()
        self.colors = Colors()

        self.font12 = CTkFont(weight='normal', family='Helvetica', size=12) 
        self.font11 = CTkFont(weight='normal', family='Helvetica', size=11, slant='italic') 

        

        self.checkbox_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(self, text="", width=15,checkbox_width=16,checkbox_height=16, fg_color=self.colors.utils_color,corner_radius=2, variable=self.checkbox_var)
        self.checkbox.grid(row=0, column=0, padx=(10, 0), pady=10)
        self.checkbox.grid_remove()  # Hide checkbox by default

        file_info = ctk.CTkFrame(self, fg_color="transparent", height=40)
        file_info.grid(row=0, column=1, sticky="nsew", padx=10)
        file_info.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(file_info, text=file_name,font=self.font12,text_color='white', anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(file_info, text=file_url,font=self.font11, anchor="w", text_color="gray").grid(row=1, column=0, sticky="w")
        
        ctk.CTkLabel(self, text=file_size, font=self.font12,text_color="white").grid(row=0, column=2, padx=10)

    def toggle_checkbox(self, show):
        if show:
            self.checkbox.grid()
        else:
            self.checkbox.grid_remove()

class MultipleFilePickerWindow(ctk.CTkToplevel):
    def self_close(self):   
        self.parent.multi_file_picker_window = None     
        self.destroy()

    def self_minimize(self):
        self.withdraw()

    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_drag(self, event):
        x = self.winfo_pointerx() - self.x_offset
        y = self.winfo_pointery() - self.y_offset
        self.geometry(f"+{x}+{y}")

    def __init__(self,master, xdm_instance):
        super().__init__(master, fg_color='#232428')
       
        self.geometry("600x470")
        self.xdm_instance = xdm_instance
        self.update_idletasks()
        master_x = master.winfo_rootx()
        master_y = master.winfo_rooty()
        master_width = master.winfo_width()
        master_height = master.winfo_height()

        self.parent = master
        
        window_x = master_x + (master_width // 2) - (600 // 2)
        window_y = master_y + (master_height // 2) - (470 // 2)


        
        self.geometry(f'600x470+{window_x}+{master_y}')
        
        self.update()
        self.update_idletasks()

        self.xe_images = Images()
        self.colors = Colors()
        self.configure(fg_color=self.colors.utils_color)
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.buttons_font = CTkFont(family="Helvetica", size=11, weight="bold")
       

        
        self.title_bar = ctk.CTkFrame(self, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.minimize = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command=self.self_minimize, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.minimize_image )
        self.minimize.place(x=560, y=5,anchor='ne' )
        self.close = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command=self.self_close, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=595, y=5,anchor='ne' )
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)


        

        self.selection_mode = False

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=self.colors.secondary_color)
        self.main_frame.pack(expand=True, fill="both", padx=5)
        self.top_actions = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.select_button = ctk.CTkButton(self.top_actions, text="Select Files",hover=False,corner_radius=5,font=self.buttons_font, width=120,height=30, command=self.toggle_selection_mode, fg_color=self.colors.utils_color, text_color="black")
        self.select_button.pack(side="right", padx=5)
        self.top_actions.pack(fill="x",pady=5)
        

        # Files list frame with scrollbar
        self.files_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=5, fg_color=self.colors.secondary_color)
        self.files_frame.pack(expand=True, side='top', fill="both", padx=10, pady=(0, 10))

        # Populate files

        self.file_widgets = []
        for file in self.parent.files_to_be_downloaded:
            fw = FileAddedWidget(self.files_frame, file["name"], file["link"], file["size"])
            fw.pack(fill="x", pady=5)
            self.file_widgets.append(fw)

        # Button frame
        button_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        button_frame.pack(fill="x", padx=10, pady=10)

        # Buttons
        ctk.CTkButton(button_frame, text="Add File", command=self.open_addfile_window, hover=False,cursor='hand2',fg_color=self.colors.utils_color,corner_radius=5, font=self.buttons_font, text_color="black").pack(side="left", padx=5)
        
        self.remove_button = ctk.CTkButton(button_frame, text="Remove Selected", command=self.remove_selected, hover=False,cursor='hand2',fg_color=self.colors.utils_color,corner_radius=5, font=self.buttons_font, text_color="black")
        self.remove_button.pack(side="left", padx=5)
        self.remove_button.pack_forget()  # Hide initially
        self.download_button = ctk.CTkButton(button_frame, text="Download All", command=self.download_all, hover=False,cursor='hand2',fg_color=self.colors.utils_color,corner_radius=5, font=self.buttons_font, text_color="black")
        self.download_button.pack(side="left", padx=5)

    def add_file(self, filename, url, size='unknown'):      
        fw = FileAddedWidget(self.files_frame, filename, url, size)
        fw.pack(fill="x", pady=5)
        self.file_widgets.append(fw)
        self.parent.files_to_be_downloaded.append({'link' : url, 'name' : filename, 'size': size})
        if self.selection_mode:
            fw.toggle_checkbox(True)
    def open_addfile_window(self):
        AddFile(self)

    def toggle_selection_mode(self):
        self.selection_mode = not self.selection_mode
        for widget in self.file_widgets:
            widget.toggle_checkbox(self.selection_mode)
        
        if self.selection_mode:
            self.select_button.configure(text="Cancel Selection")
            self.remove_button.pack(side="left", padx=5)
            self.download_button.configure(text="Download Selected")
        else:
            self.select_button.configure(text="Select Files")
            self.remove_button.pack_forget()
            self.download_button.configure(text="Download All")

    def remove_selected(self):
        for widget in self.file_widgets[:]:
            if widget.checkbox_var.get():
                widget.destroy()
                self.file_widgets.remove(widget)
        self.parent.files_to_be_downloaded = [file for file, widget in zip(self.parent.files_to_be_downloaded, self.file_widgets) if not widget.checkbox_var.get()]

    def download_all(self):
        if self.selection_mode:
            selected_files = [file for file, widget in zip(self.parent.files_to_be_downloaded, self.file_widgets) if widget.checkbox_var.get()]
            for file in selected_files:
                asyncio.run_coroutine_threadsafe(self.xdm_instance.addQueue((file['link'], file['name'], None)),self.xdm_instance.loop)
                
            selected_files = []
        else:
            for file in self.parent.files_to_be_downloaded:
                asyncio.run_coroutine_threadsafe(self.xdm_instance.addQueue((file['link'], file['name'], None)),self.xdm_instance.loop)
                

            self.parent.files_to_be_downloaded = []

        self.self_close()


class AddFile(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master, fg_color=master.colors.utils_color )
        self.attributes('-topmost', True)
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        half_w = int((width/2))
        half_h = int((height/2))
        self.geometry("380x200")
        self.geometry(f'+{half_w}+{half_h}')
        self.colors = Colors()
        self.master = master
        self.xe_images = Images()
        self.font11_bold = CTkFont(family="Helvetica", size=11, weight="bold")

        self.filename_text = ctk.StringVar()
        self.link_text = ctk.StringVar()
        self.overrideredirect(True)
        self.title_bar = ctk.CTkFrame(self, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.logo = ctk.CTkLabel(self.title_bar,text='', width=25, cursor='hand2',fg_color='transparent',  height=25, image=self.xe_images.sub_logo )
        self.logo.place(x=5, y=2.5,anchor='nw' )
        self.close = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command=lambda: self.self_close(False), width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=375, y=5,anchor='ne' )
       

        self.error_message_label = ctk.CTkLabel(self ,font=self.font11_bold, text='')
        self.error_message_label.pack(pady=2)
        
        # Entry boxes for link and filename
        self.link_box = ctk.CTkFrame(self, height=40, width=380, fg_color='transparent')
        self.link_label = ctk.CTkLabel(self.link_box,font=self.font11_bold, text="Address", text_color=self.colors.text_color)
        self.link_label.pack(pady=5, padx=12, side='left')

        
        self.link_entry = ctk.CTkEntry(self.link_box, textvariable=self.link_text,font=self.font11_bold,corner_radius=3,border_width=0,width=280)
        self.link_entry.pack(pady=5, side='left')
        self.link_box.pack()
        
        self.filename_box = ctk.CTkFrame(self, height=40, width=380, fg_color='transparent')
        self.filename_label = ctk.CTkLabel(self.filename_box,font=self.font11_bold, text="Filename", text_color=self.colors.text_color)
        self.filename_label.pack(pady=5, padx=10, side='left')
        
        self.filename_entry = ctk.CTkEntry(self.filename_box,font=self.font11_bold,textvariable=self.filename_text, corner_radius=3,border_width=0,width=280)
        self.filename_entry.pack(pady=5,  side='left')
        self.filename_box.pack()


        self.filename_box.pack_propagate(False)
        self.link_box.pack_propagate(False)

        self.link_entry.bind('<KeyRelease>', self.getInputValue)
        
        # Submit Button
        self.submit_button = ctk.CTkButton(self, font=self.font11_bold, text="Submit",width=100,hover=False, height=40, corner_radius=5, fg_color=self.colors.secondary_color, command=self.submit_file)
        self.submit_button.pack(pady=10)
    
    
        
    def sanitize_filename(self, filename):
    # Remove any invalid characters for filenames on most operating systems
        return re.sub(r'[\\/*?:"<>|]', "", filename)

    def submit_file(self):
        link = self.link_text.get()
        filename = self.filename_text.get() 

       
        if not urlparse(link).scheme:
            link = f'http://{link}'

        if not urlparse(link).netloc:
            self.error_message_label.configure(text='Insert correct address!', text_color='brown')


        
        else:
            url_parsed = urlparse(link)

            if '.' in link in link:
                
                initial_filename = self.filename_text.get()
                name, extension = os.path.splitext(initial_filename)

                
                if not name:
                    self.error_message_label.configure(text=f'No file name!', text_color='brown')
                 
                else:
                    name = self.sanitize_filename(name)# removes \\/*?:"<>| which are invalid characters

                    filename_and_path = name + extension
                    
                    filename = os.path.basename(filename_and_path)

                    

                    
                    self.master.add_file(filename, link)
                    self.destroy()

        
        # Close the add file window
        

    def self_close(self, failed = True):        
        self.destroy()

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

