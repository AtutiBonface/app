import customtkinter as ctk
from customtkinter import CTkFont
from PIL import Image
from app_utils import Colors, Images, OtherMethods
from customtkinter import CTkImage, CTkFont
import os, time
import subprocess
import platform


class Progressor(ctk.CTkToplevel):

    ## opens file that finished downloading if open folder is clicked
    def open_folder(self, path):
        
        system_name = platform.system()
        # returns a system name  
        if system_name == "Windows":
            os.startfile(f'{path}') ## for windows
        
        elif system_name == "Linux":
            subprocess.Popen(["xdg-open", path]) ## for kali linux

        else:
            pass

        self.destroy()
        
    def download_failed(self):
        for child in self.container.winfo_children():
            child.destroy()
        
        self.title_bar = ctk.CTkFrame(self.container, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.close = ctk.CTkButton(self.container,text='',corner_radius=2,command=self.self_close, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=355, y=5,anchor='ne' )

        self.message = ctk.CTkLabel(self.container, text='Failed to download! \n Server returned bad response!', font=self.font12_ro, text_color=self.colors.secondary_color)
        self.message.place(relx=.5, rely=.5, anchor='center')


        self.okay_btn = ctk.CTkButton(self.container, text='close',command=self.self_close, height=40, width=100, corner_radius=5, hover=False, fg_color=self.colors.secondary_color)
        self.okay_btn.pack(side='bottom', pady=10)
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)

    def download_complete(self, path, filename):
        for child in self.container.winfo_children():
            child.destroy()

        self.title_bar = ctk.CTkFrame(self.container, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.close = ctk.CTkButton(self.container,text='',corner_radius=2,command=self.self_close, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=355, y=5,anchor='ne' )

        self.message = ctk.CTkLabel(self.container, text='Download Complete !', font=CTkFont(family='Helvetica', weight='bold',size=18), text_color=self.colors.text_color)
        self.message.pack()

        self.filename_vari = ctk.StringVar()
        self.filename_vari.set(filename)

        self.location_vari = ctk.StringVar()
        self.location_vari.set(path)

        self.filename_box = ctk.CTkFrame(self.container, fg_color='transparent', height=30)
        self.filename_title = ctk.CTkLabel(self.filename_box, text='Filename',font=self.font12_ro, width=80)
        self.filename_title.pack(side='left')
        self.filename_name = ctk.CTkEntry(self.filename_box,state='disabled',font=self.font10_ro,border_width=0,corner_radius=3,width=240 ,textvariable=self.filename_vari)
        self.filename_name.pack(side='left', fill='x')
       
        self.location_box = ctk.CTkFrame(self.container, fg_color='transparent', height=30)
        self.location_title = ctk.CTkLabel(self.location_box, text='Location',font=self.font12_ro, width=80)
        self.location_title.pack(side='left')
        self.location_name = ctk.CTkEntry(self.location_box,state='disabled',font=self.font10_ro, border_width=0,corner_radius=3,width=240 ,textvariable=self.location_vari)
        self.location_name.pack(side='left', fill='x')

        self.filename_box.pack(fill='x', pady=10)
        self.location_box.pack(fill='x',pady=10)


        self.okay_btn = ctk.CTkButton(self.container,font=self.font12_ro, text='Open Folder',command=lambda :self.open_folder(self.location_vari.get()), height=40, width=100, corner_radius=5, hover=False, fg_color=self.colors.secondary_color)
        self.okay_btn.pack(side='bottom', pady=10)

        ## used for moving window using titlebar
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)
    def self_close(self):
        self.destroy()
    def self_minimize(self):
        self.withdraw()

    def update_progressor_ui(self, filename,size,downloaded, path, status, speed):
        try:
            if status == 'failed!':
                self.download_failed()
            elif status == 'completed.':
                self.download_complete(path, filename)
            else:                
                progress_value = self.return_progress_value(size, downloaded)    

                if self.progress_bar.winfo_exists():
                    self.progress_bar.set(progress_value)
                else:
                    pass
                

                n_downloaded = self.other_methods.return_filesize_in_correct_units(downloaded)
                n_size = self.other_methods.return_filesize_in_correct_units(size)

                if self.file_size.winfo_exists() and self.size_downloaded.winfo_exists() and self.download_speed.winfo_exists():
                    self.file_size.configure(text=f'Size {n_size}')
                    self.size_downloaded.configure(text=f'Downloaded {n_downloaded}')
                    self.download_speed.configure(text=speed)
                else:
                    pass
        except Exception as e:
            pass


    
        
    def return_progress_value(self, size, downloaded):
        if '---' in (size, downloaded):
            return 0
        else:
            try:
                size = int(size)
                downloaded = int(downloaded)

                value = round(downloaded/size, 2)

                return value
            except Exception as e:                
                return 0
    def __init__(self, parent):
        super().__init__(parent)
        self.xe_images = Images()
        self.colors = Colors()

        self.parent = parent
        
       
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        half_w = int((width/2))
        half_h = int((height/2))
        self.geometry(f'+{half_w}+{half_h}')

        self.other_methods = OtherMethods()
       

        self.font_12 = CTkFont(family='Helvetica', weight='normal',size=12, slant='italic' )
        self.font_12_bold = CTkFont(family='Helvetica', weight='bold',size=12, slant='italic' )
        self.font_16_bold = CTkFont(family='Helvetica', weight='bold',size=16)
        self.font_16 = CTkFont(family='Helvetica',size=16)
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12_ro = CTkFont(weight='bold', family='Helvetica', size=12) 
        self.font10_ro = CTkFont(weight='bold', family='Helvetica', size=10) 

        self.progress_value_variable = ctk.IntVar()
        self.progress_value_variable.set(0)
        

          # Set the window title
         # Set the window size
        self.configure(fg_color=self.colors.secondary_color)  # Set the background color
        self.overrideredirect(True)
        
        
        self.container = ctk.CTkFrame(self, height=210, width=360, fg_color=self.colors.utils_color, corner_radius=5)
        self.container.pack(fill='both', expand=True)
        
        self.container.pack_propagate(False)
        ## used for moving window using titlebar
       

        #used to make window to be topmost
        self.attributes('-topmost', True)

        

        
    ## used for moving window using titlebar
    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_drag(self, event):
        x = self.winfo_pointerx() - self.x_offset
        y = self.winfo_pointery() - self.y_offset
        self.geometry(f"+{x}+{y}")

    def pause_file_downloading_fn(self, filename, path):
        f_name_plus_path = os.path.join(path, filename)
        self.parent.pause_downloading_file(f_name_plus_path)
        self.destroy()


    def start(self, filename, address, status, size, downloaded, path):
        self.title_bar = ctk.CTkFrame(self.container, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.logo = ctk.CTkLabel(self.title_bar,text='', width=25, cursor='hand2',fg_color='transparent',  height=25, image=self.xe_images.sub_logo )
        self.logo.place(x=5, y=2.5,anchor='nw' )
        self.close = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command=self.self_close, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=355, y=5,anchor='ne' )
        self.minimize = ctk.CTkButton(self.container,text='',corner_radius=2,command=self.self_minimize, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.minimize_image )
        self.minimize.place(x=320, y=5,anchor='ne' )
        self.filename = ctk.CTkLabel(self.container, text=filename, text_color=self.colors.text_color, font=self.font12_ro)
        self.filename.pack(pady=15)
        self.middle_box = ctk.CTkFrame(self.container, fg_color='transparent')

        self.middle_box.place(relwidth=1, rely=.5,relx=.5, anchor='center')
        
        
        self.my_canvas = ctk.CTkCanvas(self.middle_box, height=80, width=80,bg=self.colors.utils_color, highlightbackground=self.colors.utils_color, highlightcolor=self.colors.utils_color, insertbackground=self.colors.utils_color )
        self.my_canvas.pack(side='left', padx=30)
        self.to_right = ctk.CTkFrame(self.middle_box, fg_color='transparent')
        self.to_right.pack(fill='x')
        self.size_downloaded = ctk.CTkLabel(self.to_right,font=self.font10_ro,height=15,text_color=self.colors.secondary_color, text='Downloaded ---', anchor='w')
        self.size_downloaded.pack(side='top', fill='x', pady=5)
        self.progress_bar_box = ctk.CTkFrame(self.to_right, width=150, fg_color='transparent', height=10)
        self.progress_bar = ctk.CTkProgressBar(self.progress_bar_box,fg_color='gray',mode='indeterminate', variable=self.progress_value_variable,progress_color=self.colors.text_color, corner_radius=2)
        self.progress_bar.place(x=0)
        self.progress_bar_box.pack(side='top', fill='x')
        
        self.file_size = ctk.CTkLabel(self.to_right,font=self.font10_ro,text_color=self.colors.secondary_color,height=15, text='Size ---', anchor='w')
        self.file_size.pack(side='top', fill='x', pady=5)
        self.download_speed = ctk.CTkLabel(self.container,font=self.font12_ro,text_color=self.colors.secondary_color, text='---')
        self.download_speed.place(y=130, x=15)
        self.pause_downloading = ctk.CTkButton(self.container, text='pause',command=lambda : self.pause_file_downloading_fn(filename, path), height=40, width=100,hover=False, corner_radius=5, fg_color=self.colors.secondary_color)
        self.pause_downloading.pack(side='bottom', pady=10)
        


        self.my_canvas.create_oval(5, 5 ,75, 75,width=7, outline='gray')
        self.my_canvas.create_arc(5,5, 75, 75, start=90, extent=-320, width=7, outline=self.colors.text_color, style=ctk.ARC)
        self.my_canvas.create_text(40, 40, text='90%', fill=self.colors.secondary_color,font=CTkFont(weight='bold', family='Helvetica', size=14))
        
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)

        