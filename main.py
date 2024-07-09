import customtkinter as ctk
import app_utils ,re, os, subprocess, platform
from app_utils import Colors, ConfigFilesHandler, downloadDetailsHandler
from add_link import LinkBox
from customtkinter import CTkFont
from xdm import TaskManager
from about import About
from settings import Settings

class MyApp(ctk.CTk):
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')
    def add_file_downloading(self, filename, extention):
        print('This has been called')

    def return_filesize_in_correct_units(self, filesize):
        try:
            filesize = int(filesize)
            if filesize > (1024*1024*1024):
                return f'{round(filesize/1000000000,2)} GB' 
            
            elif filesize > (1024*1024):
                return f'{round(filesize/1000000,2)} MB' 
            
            elif filesize > (1024):
                return f'{round(filesize/1000,2)} Kbs' 
            else: 
                return f'{round(filesize,1)} bytes' 
        except Exception as e:
            return '---'
    
    def return_file_type(self, filename):
        name , extension = os.path.splitext(filename)
        extension = extension.lower()# converting all extensions to lower case
        video_extensions = {'.mp4', '.mkv', '.flv', '.avi', '.mov', '.wmv', '.webm'}
        audio_extensions = {'.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a', '.wma'}
        document_extensions = {'.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.odt', '.ods', '.odp','.html', '.htm'}
        program_extensions = {'.exe', '.msi', '.bat', '.sh', '.py', '.jar', '.bin'}
        compressed_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp'}

        if extension in video_extensions:
            return self.xe_images.video_d2
        elif extension in document_extensions:
            return self.xe_images.document_d2
        elif extension in program_extensions:
            return self.xe_images.program_d2
        elif extension in audio_extensions:
            return self.xe_images.music_d2
        elif extension in compressed_extensions:
            return self.xe_images.zip_d2
        elif extension in image_extensions:
            return self.xe_images.image_d2
        else: return self.xe_images.document_d2

   
    def clear_btn_styles(self):
        self.all_down.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.downloading.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.failed.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
    def filter_all_downloads(self):
        self.clear_btn_styles()
        self.all_down.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)

    def filter_downloading_downloads(self):
        self.clear_btn_styles()
        self.downloading.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
    def filter_failed_downloads(self):
        self.clear_btn_styles()
        self.failed.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)

       
    def btns_to_default(self):
        self.home_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        
        self.about_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.settings_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)

    ## remove widget from content-container
    def destroy_widgets_in_content_container(self):
        for child in self.content_container.winfo_children():
            child.destroy()


    ## pages lauching
    def open_home_page(self):
        self.about_page_opened = False
        self.settings_page_opened = False
        if self.home_page_opened:
            if self.about_frame:
                self.about_frame.destroy()
            else:
                self.about_frame = None

            if self.settings_frame:
                self.settings_frame.destroy()

            else:
                self.about_frame = None
        
            self.btns_to_default()
            self.home_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
            self.side_nav_bar.update()
    
     
        
   
    def open_about_page(self):
         ## prevents opening page twice
        self.settings_page_opened = False
        if not self.about_page_opened:
            if self.settings_frame:
                self.settings_frame.destroy()
            
            self.btns_to_default()
            self.about_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
            self.about_frame = About(self.content_container)
            self.about_frame.place(relwidth=1, relheight=1)
            self.about_page_opened = True
    def open_settings_page(self):
        ## prevents opening page twice
        self.about_page_opened = False
        if not self.settings_page_opened:
            if self.about_frame:
                self.about_frame.destroy()
            
            self.btns_to_default()
            self.settings_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
            self.settings_frame = Settings(self.content_container)
            self.settings_frame.place(relwidth=1, relheight=1)
            self.settings_page_opened = True

    def open_link_box(self):
        LinkBox(self, self.xdm_class)



    def __init__(self):
        super().__init__()

        downloadDetailsHandler()
        self.index_of_page_opened = 0 # 0 home // 1 downloadin // 2 downloaded // 3 about // 4 settings
        self.about_frame = None
        self.settings_frame = None

        self.about_page_opened = False
        self.settings_page_opened = False
        self.home_page_opened = True
      
        window_width = 800
        window_height = 500

        self.geometry(f'{window_width}x{window_height}')
        self.update_idletasks()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.previously_clicked_file = None


        half_w = int((screen_width / 2) - (window_width / 2))
        half_h = int((screen_height / 2) - (window_height / 2))

        self.geometry(f'{window_width}x{window_height}+{half_w}+{half_h}')

        self.minsize(800,500)
        self.iconbitmap('xe-logos/main.ico')
        self.title('Xengine Downloader')
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12 = CTkFont(weight='normal', family='Helvetica', size=12) 
        self.font11 = CTkFont(weight='normal', family='Helvetica', size=11, slant='italic') 
        self.xe_images = app_utils.Images()
        self.colors = Colors()
        
        

        self.app_container = ctk.CTkFrame(self)
        self.app_container.pack(expand=True, fill='both')




        
        
        self.side_nav_bar = ctk.CTkFrame(self.app_container, width=200, fg_color=self.colors.primary_color, corner_radius=5, bg_color=self.colors.secondary_color)
        self.btn_bottom = ctk.CTkFrame(self.side_nav_bar, fg_color=self.colors.primary_color, height=80, width= 150)
        self.font12 = CTkFont(weight='bold', size=10, family='Arial')

        self.home_btn = ctk.CTkButton(self.side_nav_bar, command=self.open_home_page, corner_radius=5,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='Home', hover=False,fg_color=self.colors.utils_color)
        self.filter_files_box = ctk.CTkFrame(self.side_nav_bar, height=300, width=130, fg_color='transparent')
        self.video_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Videos',anchor='w', font=self.font12,text_color=self.colors.text_color,fg_color='transparent', image=self.xe_images.video_d, compound='left')
        self.video_files.pack(fill='x',  pady=2)
        self.music_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Music',anchor='w', font=self.font12,text_color=self.colors.text_color,fg_color='transparent', image=self.xe_images.music_d, compound='left')
        self.music_files.pack(fill='x',  pady=2)
        self.document_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Document',anchor='w', font=self.font12,text_color=self.colors.text_color,fg_color='transparent', image=self.xe_images.document_d, compound='left')
        self.document_files.pack(fill='x',  pady=2)
        self.zip_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Compressed',anchor='w', font=self.font12,text_color=self.colors.text_color,fg_color='transparent', image=self.xe_images.zip_d, compound='left')
        self.zip_files.pack(fill='x',  pady=2)
        self.application_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Application',anchor='w', font=self.font12,text_color=self.colors.text_color,fg_color='transparent', image=self.xe_images.program_d, compound='left')
        self.application_files.pack(fill='x',  pady=2)

        self.filter_files_box.place(x=60, y=90)
        self.filter_files_box.pack_propagate(False)
        self.about_btn = ctk.CTkButton(self.btn_bottom, command=self.open_about_page, corner_radius=5,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='Help and support', hover=False,fg_color=self.colors.secondary_color)
        self.settings_btn = ctk.CTkButton(self.btn_bottom, command=self.open_settings_page, corner_radius=5,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='Settings', hover=False,fg_color=self.colors.secondary_color)


        self.home_btn.place(x=60, y=50)
        
        self.about_btn.pack(pady=5)
        self.settings_btn.pack(pady=5)

        self.side_bar_icon_btns = ctk.CTkFrame(self.side_nav_bar,fg_color=self.colors.secondary_color, width=50, corner_radius=5)
        self.side_bar_icon_btns.pack_propagate(False)

        self.icon_btn_bottom = ctk.CTkFrame(self.side_bar_icon_btns, height=80,width=50, fg_color=self.colors.secondary_color)
        
        self.home_icon_btn = ctk.CTkButton(self.side_bar_icon_btns, command= self.open_home_page, width=30,height=30, text='', hover_color=self.colors.secondary_color,fg_color=self.colors.secondary_color,image=self.xe_images.homeImg)
        
        self.about_icon_btn = ctk.CTkButton(self.icon_btn_bottom, command= self.open_about_page, width=30,height=30, text='', hover_color=self.colors.secondary_color,fg_color=self.colors.secondary_color,image=self.xe_images.aboutImg)
        self.settings_icon_btn = ctk.CTkButton(self.icon_btn_bottom, command= self.open_settings_page, width=30,height=30, text='', hover_color=self.colors.secondary_color,fg_color=self.colors.secondary_color,image=self.xe_images.settingsImg)

        self.home_icon_btn.place(x=5, y=45)
        
        self.about_icon_btn.pack(pady=5)
        self.settings_icon_btn.pack(pady=5)
        self.icon_btn_bottom.pack(side='bottom', pady=20)




        self.side_bar_icon_btns.pack(side=ctk.LEFT, fill='y' , pady=5, padx=5)
        self.btn_bottom.pack(side='bottom', pady=20)

        self.side_nav_bar.pack(fill=ctk.Y, side='left')
        self.side_nav_bar.pack_propagate(False)

        self.content_container = ctk.CTkFrame(self.app_container, fg_color=self.colors.secondary_color, corner_radius=0)
        
        self.content_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.search_entry = ctk.CTkEntry(self.app_container, width=200, height=30, placeholder_text="Search", corner_radius=5,border_color='#3d539f', bg_color=self.colors.text_color)


        self.top_container = ctk.CTkFrame(self.content_container, fg_color=self.colors.primary_color, height=100)
        self.add_link = ctk.CTkButton(self.top_container,image=self.xe_images.link,command=self.open_link_box, text='New',hover=False,cursor='hand2',font=self.font12,fg_color=self.colors.secondary_color,  width=50).pack(padx=10, side='left')
        self.segmented_btns = ctk.CTkFrame(self.top_container,width=150,  fg_color="transparent", corner_radius=5)
        
        self.all_down = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.filter_all_downloads,text='All',width=50, height=30, hover=False,fg_color=self.colors.secondary_color)
        self.downloading = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.filter_downloading_downloads,text='Complete',width=60, height=30, hover=False,fg_color=self.colors.secondary_color)
        self.failed = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.filter_failed_downloads,text='Incomplete',width=50, height=30, hover=False,fg_color=self.colors.secondary_color)

        self.all_down.pack(padx=5, pady=5,side='left')

        self.downloading.pack(padx=5, pady=5,side='left')

        self.failed.pack(padx=5, pady=5,side='left')
        self.segmented_btns.pack(side='right', padx=10, pady=2)  
        self.top_container.pack(fill='x', padx=5, pady=5)



       
        ### files here
        self.files_labels = ctk.CTkFrame(self.content_container, fg_color='transparent', height=20)
        self.name_label = ctk.CTkLabel(self.files_labels,text_color=self.colors.text_color,font=self.font12, text='Name', anchor='w')
        self.name_label.pack(side='left', padx=60)
        self.status_label = ctk.CTkLabel(self.files_labels,text_color=self.colors.text_color,font=self.font12, text='Status',width=70,  anchor='w')
        self.date_label = ctk.CTkLabel(self.files_labels,text_color=self.colors.text_color,font=self.font12, text='Date',width=60, anchor='w')
        self.size_label = ctk.CTkLabel(self.files_labels,text_color=self.colors.text_color,font=self.font12, text='Size', width=60, anchor='w')
        self.size_label.pack(side='right', padx=5)
        self.date_label.pack(side='right', padx=5)
        self.status_label.pack(side='right', padx=5)

        self.files_labels.pack(fill='x')
        self.files_labels.pack_propagate(False)
        self.downloading_list = ctk.CTkScrollableFrame(self.content_container, fg_color=self.colors.secondary_color)
        self.downloading_list.pack(expand=True, fill='both')

        self.previously_clicked_btn = {}
        self.details_of_file_clicked = None
        self.running_tasks = {}
        self.file_widgets = []
        self.last_mtime = None

        self.w_state = self.wm_state()
       
        
        
        self.xdm_class = TaskManager(self)
        
        self.display_files_in_ui()
        actionsForDisplayedFiles(self)

    def delete_details_or_make_changes(self, filename):
        file_details = []
        origin = downloadDetailsHandler().path_to_download_conf_file
        self.origin_and_conf = f'{origin}/downloading.txt'
        try:
            with open(self.origin_and_conf, 'r') as f:
                entry = {}
                for line in f.readlines():
                    line = line.strip()
                    if line.startswith('<file>'):
                        entry = {}
                    elif line.startswith('</file>'):
                        file_details.append(entry)
                    else:
                        match = re.findall(r'\s*(\S+):\s*(.+)', line)
                        if match:
                            key, value = match[0]
                        
                            entry[key.strip()] = value.strip()

            
            updated_file_details = [entry for entry in file_details if entry.get('filename') != filename]

           
            
            with open(self.origin_and_conf, 'w') as f:
                for entry in updated_file_details:                
                    f.write("<file>\n")
                    for key, value in entry.items():
                        f.write(f"{key}: {value}\n")
                    f.write("</file>\n")
                    f.write("\n")
            
        except Exception as e:
            pass

    def clear_displayed_files_widgets(self):
        for widget in self.file_widgets:
            widget.destroy()
        self.file_widgets.clear()

    def display_files_in_ui(self):
        origin = downloadDetailsHandler().path_to_download_conf_file
        self.origin_and_conf = f'{origin}/downloading.txt'

        
        file_details = []
        try:
            current_mtime = os.path.getmtime(self.origin_and_conf)
            if self.last_mtime != current_mtime:
                self.last_mtime = current_mtime
                with open(self.origin_and_conf, 'r') as f:
                    entry = {}
                    for line in f.readlines():
                        line.strip()

                        if line.startswith('<file>'):
                            entry = {}
                        elif line.startswith('</file>'):
                            file_details.append(entry)

                        else:
                            match = re.findall(r'\s*(\S+):\s*(.+)', line)
                            
                            if match:
                                key , value = match[0]

                                entry[key.strip()] =  value.strip()

                self.clear_displayed_files_widgets()

                for value in file_details:
                    
                    size = f'{self.return_filesize_in_correct_units(value['size'])}'
                    filename = value['filename']
                    path = value['path']
                    name, exten = os.path.splitext(filename)
                    filename.strip()
                    if(len(name) > 45):
                        filename = f'{name[:20]}...{name[-22:]}{exten}'

                    file_widget = File(self, filename, size, value['status'], value['date-modified'], path)
                    file_widget.pack(fill='x')
                    self.file_widgets.append(file_widget)
        except Exception as e:
            pass


        self.after(300, self.display_files_in_ui)

        
            

           



        
    




class actionsForDisplayedFiles():

    def __init__(self, parent):
        self.parent = parent
        self.colors = Colors()
        self.font11 = CTkFont(weight='bold', family='Helvetica', size=11)
        self.font17 = CTkFont(weight='bold', family='Helvetica', size=17)
        self.font12 = CTkFont(weight='bold', family='Helvetica', size=12, slant='italic') 

        self.container = ctk.CTkFrame(parent.content_container, height=50, fg_color=self.colors.primary_color,bg_color='transparent', corner_radius=5)
        self.actions_label = ctk.CTkLabel(self.container, text=" ",  fg_color='transparent', height=20,width=70, font=self.font11, text_color=self.colors.text_color)
        self.actions_label.place(x=20, rely=.5 , anchor='w')
        self.actions = ctk.CTkFrame(self.container, fg_color=self.colors.primary_color, bg_color='transparent')

        self.xe_images =app_utils.Images()
        self.open = ctk.CTkButton(self.actions, text='',command=lambda state='Open':self.change_download_state(state, self.open), image=self.xe_images.open, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.delete = ctk.CTkButton(self.actions, text='',command=lambda state='Delete':self.change_download_state(state, self.delete), image=self.xe_images.delete, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.pause = ctk.CTkButton(self.actions, text='',command=lambda state='Pause':self.change_download_state(state, self.pause), image=self.xe_images.pause, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.resume = ctk.CTkButton(self.actions, text='',command=lambda state='Resume':self.change_download_state(state, self.resume), image=self.xe_images.play, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.restart = ctk.CTkButton(self.actions, text='',command=lambda state='Restart':self.change_download_state(state, self.restart), image=self.xe_images.restart, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.stop = ctk.CTkButton(self.actions, text='',command=lambda state='Stop':self.change_download_state(state, self.stop), image=self.xe_images.stop, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)

        self.open.pack(side='left', padx=10, pady=10)
        self.delete.pack(side='left', padx=10, pady=10)
        self.pause.pack(side='left', padx=10, pady=10)
        self.resume.pack(side='left', padx=10, pady=10)
        self.stop.pack(side='left', padx=10, pady=10)
        self.restart.pack(side='left', padx=10, pady=10)
    
        self.actions.place(rely=.5, relx=.5, anchor='center')
        self.container.pack(side='bottom', fill='x', padx=5, pady=2)
        self.container.pack_propagate(False)
        self.open.bind('<Enter>', lambda event , state='Open':self.on_actions_enter(event, state))
        self.delete.bind('<Enter>', lambda event , state='Delete':self.on_actions_enter(event, state))
        self.pause.bind('<Enter>', lambda event , state='Pause':self.on_actions_enter(event, state))
        self.resume.bind('<Enter>', lambda event , state='Resume':self.on_actions_enter(event, state))
        self.restart.bind('<Enter>', lambda event , state='Restart':self.on_actions_enter(event, state))
        self.stop.bind('<Enter>', lambda event , state='Stop':self.on_actions_enter(event, state))

        self.open.bind('<Leave>', lambda event:self.on_actions_leave(event, self.open))
        self.delete.bind('<Leave>', lambda event:self.on_actions_leave(event, self.delete))
        self.pause.bind('<Leave>', lambda event:self.on_actions_leave(event, self.pause))
        self.resume.bind('<Leave>', lambda event:self.on_actions_leave(event, self.resume))
        self.restart.bind('<Leave>', lambda event:self.on_actions_leave(event, self.restart))
        self.stop.bind('<Leave>', lambda event:self.on_actions_leave(event, self.stop))
        
    def close_opened_popup_window(self, window):
        window.destroy()

    def delete_file_from_storage_temp_file_or_both(self,window):
        f_name , path, status = self.parent.details_of_file_clicked 

        file_to_delete = f'{path}/{f_name}'
        if self.check_value.get() == 1:
            try:
                self.parent.delete_details_or_make_changes(f_name)
            except Exception as e: 
                pass
            if os.path.exists(file_to_delete):
                try:
                    os.remove(file_to_delete)
                except Exception as e:
                    print(e)

        else:
            try:
                self.parent.delete_details_or_make_changes(f_name)
            except Exception as e: 
                pass

            
        window.destroy()
        
    def show_filenotfound_popup(self, parent):
        self.error_top_window = ctk.CTkToplevel(parent)
        self.error_top_window.overrideredirect(True)
        width = self.error_top_window.winfo_screenwidth()
        height = self.error_top_window.winfo_screenheight()
        half_w = int((width/2))
        half_h = int((height/2))
        self.error_top_window.geometry(f'+{half_w}+{half_h}')
        
        self.message_box = ctk.CTkFrame(self.error_top_window, height=180, width=320, fg_color=self.colors.utils_color, corner_radius=5)
        self.title_bar = ctk.CTkFrame(self.message_box, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.close = ctk.CTkButton(self.message_box,text='',corner_radius=2,command=lambda : self.close_opened_popup_window(self.error_top_window), width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=315, y=5,anchor='ne' )
        self.error = ctk.CTkLabel(self.message_box, anchor='w',text='File not found!', text_color=self.colors.text_color,font=self.font17)
        self.error.pack(fill='x',pady=5, padx=10)
        self.about_error = ctk.CTkLabel(self.message_box,anchor='w', text='The file has been moved,renamed or deleted', font=self.font12)
        self.about_error.pack(padx=10, fill='x')
        self.okay = ctk.CTkButton(self.message_box, text='ok', height=40,command=lambda : self.close_opened_popup_window(self.error_top_window), width=100,hover=False, corner_radius=5, fg_color=self.colors.secondary_color)
        self.okay.pack(side='bottom', pady=10)
        self.message_box.pack_propagate(False)
        self.message_box.pack()

    def show_delete_file_popup(self, parent):
        self.delete_file_top_window = ctk.CTkToplevel(parent)
        self.delete_file_top_window.overrideredirect(True)
        width = self.delete_file_top_window.winfo_screenwidth()
        height = self.delete_file_top_window.winfo_screenheight()
        half_w = int((width/2))
        half_h = int((height/2))
        self.check_value = ctk.IntVar()
        self.delete_file_top_window.geometry(f'+{half_w}+{half_h}')

        self.message_box = ctk.CTkFrame(self.delete_file_top_window, height=210, width=360, fg_color=self.colors.utils_color, corner_radius=5)
        self.title_bar = ctk.CTkFrame(self.message_box, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.close = ctk.CTkButton(self.message_box,text='',corner_radius=2,command= lambda :self.close_opened_popup_window(self.delete_file_top_window), width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=355, y=5,anchor='ne' )
        self.prompt = ctk.CTkLabel(self.message_box, anchor='w',text='Confirm Deletion', text_color=self.colors.text_color,font=self.font17)
        self.prompt.pack(fill='x',pady=5, padx=10)
        self.prompt_error = ctk.CTkLabel(self.message_box,anchor='w', text='Are you sure you want to delete selected downloads?', font=self.font12)
        self.prompt_error.pack(padx=10, fill='x')
        self.check_box = ctk.CTkCheckBox(self.message_box,checkbox_height=15,corner_radius=1,offvalue=0, onvalue=1,variable=self.check_value, checkbox_width=15, hover=False, text='Delete file from disk')
        self.check_box.pack(padx=10, pady=10,fill='x')
        self.no = ctk.CTkButton(self.message_box, text='no', height=40,command= lambda :self.close_opened_popup_window(self.delete_file_top_window), width=100,hover=False, corner_radius=5, fg_color=self.colors.secondary_color)
        self.no.pack(side='left', pady=10, expand=True)
        self.yes = ctk.CTkButton(self.message_box, text='yes', height=40,command= lambda :self.delete_file_from_storage_temp_file_or_both(self.delete_file_top_window), width=100,hover=False, corner_radius=5, fg_color=self.colors.secondary_color)
        self.yes.pack(side='left', pady=10, expand=True)
        self.message_box.pack_propagate(False)
        self.message_box.pack()




    def change_download_state(self, state,me):
        if self.parent.details_of_file_clicked:
            f_name , path, status = self.parent.details_of_file_clicked 
            if state == 'Open':
                if not os.path.exists(f'{path}/{f_name}'):
                    self.show_filenotfound_popup(self.parent)
                else:
                    system_name = platform.system()   
                
                    if system_name == 'Windows':
                        os.startfile(f'{path}/{f_name}')

                    elif system_name == 'Linux':
                        subprocess.Popen(["xdg-open", f'{path}/{f_name}'])
            elif state == 'Delete':
                self.show_delete_file_popup(self.parent)



            
            me.configure(fg_color = self.colors.utils_color)
        else:
            print("Nothing has been selected")

    def on_actions_enter(self, event, state):
        self.actions_label.configure(text=state, fg_color=self.colors.utils_color)

    def on_actions_leave(self,event, me):
        self.actions_label.configure(text='', fg_color=self.colors.primary_color)
        me.configure(fg_color=self.colors.secondary_color)
class File(ctk.CTkFrame):

    def propagate_file_btn(self, event):
        parent = self.parent
        if parent.previously_clicked_file is None:
            parent.previously_clicked_file = {}
        if parent.previously_clicked_file and parent.details_of_file_clicked:
            parent.details_of_file_clicked = None
            for widget in parent.previously_clicked_file.get(self.file_id, []):
                try:
                    widget.configure(fg_color=parent.colors.secondary_color, text_color='gray')
                except:
                    widget.configure(fg_color=parent.colors.secondary_color)

        self.configure(fg_color=parent.colors.utils_color)
        self.file_type.configure(fg_color=parent.colors.utils_color)
        self.download_status.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)
        self.file_size.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)
        self.file_name.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)
        self.file_download_date.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)

        parent.previously_clicked_file[self.file_id] = [
            self,
            self.file_name,
            self.file_size,
            self.file_type,
            self.file_download_date,
            self.download_status,
        ]
        parent.details_of_file_clicked = self.alter_details

    def update_ui(self, size, complete):
        self.file_size.configure(text=size)
        self.download_status.configure(text=complete)

    def __init__(self, parent, filename, size, status, date, path) -> None:
        super().__init__(parent.downloading_list, fg_color=parent.colors.secondary_color,height=40,corner_radius=5, cursor='hand2')
        self.task_name = ''
        self.parent = parent
        self.colors = Colors()
        self.file_id = filename

        self.appended_files = []

        self.alter_details = (filename, path, status)
        
        self.file_type = ctk.CTkLabel(self, text='', image=self.parent.return_file_type(filename), fg_color='transparent')
        self.file_type.pack(side='left', padx=10)

        self.file_name = ctk.CTkLabel(self, text_color=self.colors.text_color,text=filename, font=self.parent.font11,fg_color='transparent', anchor='w')
        self.file_name.pack(side='left', fill='x', expand=True, padx=10, pady=1)
       
        self.file_size = ctk.CTkLabel(self,text=f"{size}",anchor='w',text_color='gray',font=self.parent.font12, fg_color='transparent', width=60)
        self.file_size.pack(side='right',  padx=5, pady=5)
        self.file_download_date = ctk.CTkLabel(self,anchor='w',text_color='gray',text=date,font=self.parent.font12, width=60,fg_color='transparent')
        self.file_download_date.pack(side='right', padx=5, pady=5)
        self.download_status = ctk.CTkLabel(self,text_color='gray',anchor='w', text=status, width=70, font=self.parent.font12)
        self.download_status.pack(side='right')

        

        
        self.pack_propagate(False)

        
        self.bind('<Button-1>', self.propagate_file_btn)
        self.file_type.bind('<Button-1>', self.propagate_file_btn)
        self.download_status.bind('<Button-1>', self.propagate_file_btn)
        self.file_size.bind('<Button-1>', self.propagate_file_btn)
        self.file_name.bind('<Button-1>', self.propagate_file_btn)
        self.file_download_date.bind('<Button-1>', self.propagate_file_btn)
    
        
app = MyApp()
app.mainloop()