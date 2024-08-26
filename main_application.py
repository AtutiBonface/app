import customtkinter as ctk
import os, sys, asyncio , websockets, threading , json
from app_utils import Colors, Images
from file_actions import actionsForDisplayedFiles, More
from add_link import LinkBox
from customtkinter import CTkFont
from progress import Progressor
from xdm import TaskManager
from about import About
from settings import Settings
from file_ui import File
from app_utils import OtherMethods
import database, queue,time
import tkinter as tk
from multi_file_window import MultipleFilePickerWindow

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        database.initiate_database()        
        self.setup_data()
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_layout()
        self.bind_events()
        self.start_background_tasks()
        

    def setup_window(self):
        window_width = 800
        window_height = 500
        self.geometry(f'{window_width}x{window_height}')
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        half_w = int((screen_width / 2) - (window_width / 2))
        half_h = int((screen_height / 2) - (window_height / 2))
        self.geometry(f'{window_width}x{window_height}+{half_w}+{half_h}')
        self.minsize(800,500)
        self.maxsize(900, 550)
        print(self.other_methods.resource_path('xe-logos/main.ico'))
        self.iconbitmap(self.other_methods.resource_path('xe-logos/main.ico'))
        self.title('BlackJuice')

    def setup_styles(self):
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12 = CTkFont(weight='bold', family='Helvetica', size=12) 
        self.font11 = CTkFont(weight='normal', family='Helvetica', size=11, slant='italic')
        self.font10_bold = CTkFont(weight='bold', size=10, family='Arial') 
        self.font11_bold = CTkFont(family="Helvetica", size=11, weight="bold")

        self.xe_images =Images()
        self.colors = Colors()

    def setup_data(self):
        self.xengine_downloads  = {}
        self.load_downloads_from_db()
        self.xdm_class = TaskManager(self)
        self.other_methods = OtherMethods()
        self.update_queue = queue.Queue()
        self.about_page_opened = False
        self.settings_page_opened = False
        self.home_page_opened = True
        self.about_frame = None
        self.settings_frame = None
        self.previously_clicked_btn = None
        self.details_of_file_clicked = None
        self.more_actions = None
        self.running_tasks = {}
        self.file_widgets = {}
        self.last_mtime = None
        self.w_state = self.wm_state() 
        self.multi_file_picker_window = None
        self.files_to_be_downloaded = []   
        self.filter_page = 'all'
        self.progress_toplevels = {} 
        

    def create_widgets(self):   
        self.create_app_container()    
        self.create_sidebar()
        self.create_content_area()
        self.create_file_list()
        self.create_file_list_order_labels()
        self.create_bottom_bar()
        self.create_top_bar()

    def create_app_container(self):
        self.app_container = ctk.CTkFrame(self)
        self.app_container.pack(expand=True, fill='both') 
       
    def setup_layout(self): 
        # dont alter the orderof these as it will disrupt the ui of the Blackjuice
        
        self.sidebar.pack(fill=ctk.Y, side='left') 
        self.content_area.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.top_bar.pack(fill='x', padx=5, pady=5)
        self.file_list_order.pack(fill='x')
        self.file_list_order.pack_propagate(False)
        self.file_list.pack(expand=True, fill='both')  
        self.bottom_bar.pack( fill='x', padx=5, pady=2)
        self.bottom_bar.pack_propagate(False)
       
        

    def bind_events(self):
        # Event binding code here
        pass

    def start_background_tasks(self):
        threading.Thread(target=self.start_websocket_server, daemon=True).start()
        threading.Thread(target=self.process_updates, daemon=True).start()

    # Sidebar related methods
    def create_sidebar(self):
        self.sidebar = Sidebar(self.app_container, self)
        

    # Content area related methods
    def create_content_area(self):       
        self.content_area = ContentArea(self.app_container, self)
        self.settings_frame = Settings(self.content_area)

        self.is_opening_progress_window_allowed = self.settings_frame.return_setting_value('show_progress_window')

        self.is_opening_download_complete_window_allowed = self.settings_frame.return_setting_value('show_download_complete_window')

       

        

        
        

    # Top bar related methods
    def create_top_bar(self):
        self.top_bar = TopBar(self.content_area, self)
        
    def create_file_list_order_labels(self):
        self.file_list_order = FileListOrderLabel(self.content_area, self)


    
       

    # File list related methods
    def create_file_list(self):
        self.file_list = FileList(self.content_area, self)
        

    def create_bottom_bar(self):
        self.bottom_bar = actionsForDisplayedFiles(self.content_area, self)

    # WebSocket related methods
    async def handle_websockets(self, websocket, path):
        #handling sockets from extension here
        try:
            async for message in websocket:
                if message:
                    data = json.loads(message) 
                                 
                    count = int(data['count'])
                    digit = 1
                    if count > 1:
                        self.files_to_be_downloaded = data['files'] 
                        self.after(0, lambda: self.open_multi_file_picker_window(data['files']))
                                                                  
                        
                    else:
                        url = ''
                        filename = ''            
                        for file in data['files']:
                            url = file['link']
                            filename = file['name']                      

                        self.after(0, lambda : self.openUrlPopup(url =url, filename=filename))
                    
                else:
                    print("No message")
        except Exception as e:
            pass

    def start_websocket_server(self):
        asyncio.run(self.websocket_main())

    async def websocket_main(self):
        async with websockets.serve(self.handle_websockets, '127.0.0.1', 65432):
            await asyncio.Future()

   
    # Database related methods
    def load_downloads_from_db(self):
        all_downloads = database.get_all_data()
        for download in all_downloads:
            id, filename, address, filesize, downloaded, status, modification_date, path = download
            self.xengine_downloads[filename] = {
                'url': address,
                'status': status,
                'downloaded': downloaded,
                'filesize': filesize,
                'modification_date': modification_date,
                'path': path
            }

    # File management methods
    def add_download_to_list(self, filename, address, path, date):
        
        self.xengine_downloads[filename] = {
            'url': address,
            'status': 'waiting...',
            'downloaded': '---',
            'filesize': '---',
            'modification_date': date,
            'path': path
        }
        self.update_queue.put((filename, 'waiting...', '---','---', date))
        self.after(100, lambda : self.open_progress_window(filename, address, 'waiting...', '---', '---', path))
        
    def open_progress_window(self, filename, address, status, size, downloaded, path):

        if self.is_opening_progress_window_allowed.strip() == 'true':
            self.progress_toplevels[filename] = Progressor(self)

            self.progress_toplevels[filename].start(filename, address, status, size, downloaded, path)
            if  self.progress_toplevels[filename].progress_bar.winfo_exists():
                self.progress_toplevels[filename].progress_bar.start()
            else:
                pass
        elif 'true' in self.is_opening_download_complete_window_allowed.split():
            print("The window is no allowed ")
            self.progress_toplevels[filename] = Progressor(self)
            self.progress_toplevels[filename].withdraw()

       
     

    def update_download(self, filename, status, size, downloaded ,date, speed):
        name = os.path.basename(filename)
        path = self.xengine_downloads[name]['path']       
        if name in self.xengine_downloads:
            updateDict = self.xengine_downloads[name]           
            if 'failed' in status.lower():  # Convert status to lowercase for case-insensitive comparison
                updateDict['status'] = 'failed!'
            else:
                updateDict['status'] = status
            updateDict['filesize'] = size
            updateDict['modification_date'] = date
            updateDict['downloaded'] = downloaded
            self.update_queue.put((name, updateDict['status'], size, downloaded ,date))

            if name in self.progress_toplevels :
                #self.is_opening_download_complete_window_allowed.split() == 'true'
                #self.is_opening_progress_window_allowed.strip() == 'true'
                try:
                    progressor = self.progress_toplevels[name]
                    if  progressor.winfo_exists():
                        if hasattr(progressor, 'progress_bar') and progressor.progress_bar.winfo_exists():
                            progressor.progress_bar.stop()
                            progressor.progress_bar.configure(mode='determinate')                            
                    
                        if  'failed' in status or 'completed' in status:                            
                            if progressor.state() == 'withdrawn':
                                progressor.deiconify()                           
                            progressor.lift() 
                        self.after(0, progressor.update_progressor_ui, name,size,downloaded, path, status, speed)

                    else:  
                        if name in   self.progress_toplevels:                    
                            del self.progress_toplevels[name]

            
                except tk.TclError as e:
                    del self.progress_toplevels[name]
            elif name in self.progress_toplevels and self.progress_toplevels[name].winfo_exists():
                self.progress_toplevels[name].destroy()
                del self.progress_toplevels[name]

            if name in self.file_widgets and self.file_widgets[name].winfo_exists():
                if 'completed' in status:
                    pass
                    time.sleep(2)                    
                    self.file_widgets[name].destroy()
                    del self.file_widgets[name]
                    

            


    # UI update methods
    def process_updates(self):
        while True:
            try:
                filename, status, size, downloaded ,date = self.update_queue.get(timeout=0.1)
                self.update_file_widget(filename, status, size, downloaded ,date)
                                
            except queue.Empty:
                continue

    def update_file_widget(self, filename, status, size, downloaded ,date):
        
        
        if filename in self.file_widgets:
            if self.file_widgets[filename].winfo_exists():
                self.file_widgets[filename].update_file_info(status, size, date)
        else:
            self.add_new_file_widget(filename, status, size, date)

    def add_new_file_widget(self, filename, status, size, date):       

        new_widget = File(self.file_list,self, filename, size, status, date, self.xengine_downloads[filename]['path'])
        new_widget.pack(fill='x', side='bottom')
        self.file_widgets[filename] = new_widget
  
    
    def display_all_downloads_on_page(self):
        self.previously_clicked_btn = None
        self.previously_clicked_file = None
        for filename, detail in self.return_all_downloads().items():
            if filename not in self.file_widgets and not 'completed' in detail['status']:
                self.add_new_file_widget(filename, detail['status'], detail['filesize'], detail['modification_date'])

            elif filename in self.file_widgets and  self.file_widgets[filename].winfo_exists():
                self.file_widgets[filename].destroy()
                del self.file_widgets[filename]
            else:
                if not 'completed.' in  detail['status']:
                    self.add_new_file_widget(filename, detail['status'], detail['filesize'], detail['modification_date'])
   
           
            #self.file_widgets[filename].resetFileStyles()

    def display_complete_downloads_on_page(self):
        self.previously_clicked_btn = None
        self.previously_clicked_file = None
        for filename, detail in self.return_all_downloads().items():
            if filename  in self.file_widgets  and  detail['status'] == 'completed.' and self.file_widgets[filename].winfo_exists():
                pass
            elif filename in self.file_widgets and  self.file_widgets[filename].winfo_exists():
                self.file_widgets[filename].destroy()
                del self.file_widgets[filename]
            else:
                if detail['status'] == 'completed.':
                    self.add_new_file_widget(filename, detail['status'], detail['filesize'], detail['modification_date'])




    
    # File operations
    def pause_downloading_file(self, filename_with_path):
        f_name = os.path.basename(filename_with_path)
        self.load_downloads_from_db()## reasign values to xengine_downloads to get updated values for downloaded chuck
        for name , details in self.xengine_downloads.items():
            if name == f_name and not (details['status'] == 'completed.' or details['status'] == '100.0%'):
                size = details['filesize']
                link = details['url']
                downloaded = details['downloaded']           
                asyncio.run_coroutine_threadsafe(self.xdm_class.pause_downloads_fn(filename_with_path, size, link ,downloaded), self.xdm_class.loop)
                if f_name in self.progress_toplevels:
                   
                    if self.progress_toplevels[f_name].winfo_exists():
                        self.progress_toplevels[f_name].destroy()
                    del self.progress_toplevels[f_name]


    def resume_paused_file(self, filename_with_path):
        f_name = os.path.basename(filename_with_path) 
        self.load_downloads_from_db()## reasign values to xengine_downloads to get updated values for downloaded chuck
        for name , details in self.xengine_downloads.items():
            if name == f_name and not (details['status'] == 'completed.' or details['status'] == '100.0%'):
                self.downloaded_chuck = 0
                try:
                    self.downloaded_chuck = int(details['downloaded'])                    

                except Exception as e:                   
                    self.downloaded_chuck = 0
                
                if name in self.progress_toplevels:
                    if self.progress_toplevels[name].winfo_exists():
                        self.progress_toplevels[name].destroy()
                    del self.progress_toplevels[name]
                if self.is_opening_progress_window_allowed.strip() == 'true':
                    self.progress_toplevels[name] = Progressor(self)                
                    self.progress_toplevels[name].start(name, details['url'], 'resuming...',details['filesize'] ,self.downloaded_chuck, details['path'])
                    if  self.progress_toplevels[name].progress_bar.winfo_exists():
                            self.progress_toplevels[name].progress_bar.start()
                            self.progress_toplevels[name].progress_bar.configure(mode='indeterminate')
                elif 'true' in self.is_opening_download_complete_window_allowed:
                    self.progress_toplevels[name] = Progressor(self)   
                    self.progress_toplevels[name].withdraw()

                    

                asyncio.run_coroutine_threadsafe(self.xdm_class.resume_downloads_fn(filename_with_path,  details['url'], self.downloaded_chuck), self.xdm_class.loop)

    def update_filename(self, old_name, new_name):       

        pathless_old_name = os.path.basename(old_name)
        pathless_new_name = os.path.basename(new_name)

        if pathless_old_name in self.xengine_downloads:
            value = self.xengine_downloads.pop(pathless_old_name)

            self.xengine_downloads[pathless_new_name] = value
                
                
        if pathless_old_name in self.file_widgets:
            value = self.file_widgets.pop(pathless_old_name) 

            self.file_widgets[pathless_new_name] = value

            file_widget = self.file_widgets[pathless_new_name]

            if file_widget.winfo_exists():
                file_widget.update_filename(new_name)

        if pathless_old_name in self.progress_toplevels:
            value = self.progress_toplevels.pop(pathless_old_name)

            self.progress_toplevels[pathless_new_name] = value

            progressor = self.progress_toplevels[pathless_new_name]

            if progressor.winfo_exists():
                progressor.update_filename(new_name)


    def return_all_downloads(self):
        return self.xengine_downloads
    
    

    def open_multi_file_picker_window(self, files):
        if self.multi_file_picker_window is None or not self.multi_file_picker_window.winfo_exists():
            self.after(100, lambda : self._create_multi_file_picker_window(files))
            print("The is NO multi file window here")
        else:
            print("The is a multi file window here")
            self.multi_file_picker_window.appendFiles(files)
            if self.multi_file_picker_window.wm_state() == 'withdrawn':
                self.multi_file_picker_window.deiconify()
            self.multi_file_picker_window.lift()
            self.multi_file_picker_window.focus_force()

    def _create_multi_file_picker_window(self, files):
        try:
            self.multi_file_picker_window = MultipleFilePickerWindow(self, self.xdm_class, files)
            self.multi_file_picker_window.update_idletasks()
            self.multi_file_picker_window.update()
        except Exception as e:
            print(f"Error creating MultipleFilePickerWindow: {e}")
            self.multi_file_picker_window = None

    def openUrlPopup(self, url , filename):        
        link_box = LinkBox(self, self.xdm_class)
        link_box.update_idletasks()
        link_box.link_text.set(url)
        link_box.filename_text.set(filename)

    def delete_details_or_make_changes(self, filename):        
        database.delete_individual_file(filename)## delete from database       
        self.remove_individual_file_widget(filename) ## destroy widget
    def remove_individual_file_widget(self, filename):
        
        
        if self.file_widgets[filename].winfo_exists():
            self.file_widgets[filename].destroy()
            del self.file_widgets[filename]
            del self.xengine_downloads[filename]
            
            self.previously_clicked_btn = None
            self.previously_clicked_file = None
        else: 
            pass

           

    def clear_displayed_files_widgets(self):
        for widget in self.file_widgets.items():
            widget.destroy()
        self.file_widgets = {}
        
          

class TopBar(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=app.colors.primary_color, height=100)
        self.app = app
        self.create_widgets(app)
        self.filter_all_downloads()

    def create_widgets(self, app):

        self.add_link = ctk.CTkButton(self,image=app.xe_images.link,command=self.open_link_box, text='New',hover=False,cursor='hand2',font=app.font11_bold,fg_color=app.colors.secondary_color,  width=60).pack(padx=10, side='left')
        self.segmented_btns = ctk.CTkFrame(self,width=150,  fg_color="transparent", corner_radius=5)
        
        self.all_down = ctk.CTkButton(self.segmented_btns,command=self.filter_all_downloads, font=app.font11_bold,corner_radius=5,text='Active',width=80, height=30, hover=False,fg_color=app.colors.secondary_color)
        self.downloading = ctk.CTkButton(self.segmented_btns,command=self.filter_complete_downloads, font=app.font11_bold,corner_radius=5,text='Complete',width=80, height=30, hover=False,fg_color=app.colors.secondary_color)
        
        self.all_down.pack(padx=5, pady=5,side='left')
        self.downloading.pack(padx=5, pady=5,side='left')
       
        self.segmented_btns.pack(side='right', padx=10, pady=2)  

    def clear_btn_styles(self):
        self.all_down.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.secondary_color)
        self.downloading.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.secondary_color)
        
    def filter_all_downloads(self):
        
        self.clear_btn_styles()
        self.all_down.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.utils_color)
        self.app.display_all_downloads_on_page()

    def filter_complete_downloads(self):
        
        self.clear_btn_styles()
        self.downloading.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.utils_color)
        self.app.display_complete_downloads_on_page()
    

    def open_link_box(self):
        LinkBox(self.app, self.app.xdm_class)

    

class FileListOrderLabel(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color='transparent', height=20)

        self.create_widgets(app)

    def create_widgets(self, app):
        self.name_label = ctk.CTkLabel(self,text_color=app.colors.text_color,font=app.font11_bold, text='Name', anchor='w')
        self.name_label.pack(side='left', padx=60)
        self.status_label = ctk.CTkLabel(self,text_color=app.colors.text_color,font=app.font11_bold, text='Status',width=70,  anchor='w')
        self.date_label = ctk.CTkLabel(self,text_color=app.colors.text_color,font=app.font11_bold, text='Date',width=60, anchor='w')
        self.size_label = ctk.CTkLabel(self,text_color=app.colors.text_color,font=app.font11_bold, text='Size', width=60, anchor='w')
        self.size_label.pack(side='right', padx=5)
        self.date_label.pack(side='right', padx=5)
        self.status_label.pack(side='right', padx=5)

class ContentArea(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=app.colors.secondary_color, corner_radius=0)
        

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, width=200, fg_color=app.colors.primary_color, corner_radius=5, bg_color=app.colors.secondary_color)
        self.app = app

        self.xe_images = Images()

        self.video_d = self.xe_images.video_d
        self.document_d = self.xe_images.document_d
        self.music_d = self.xe_images.music_d
        self.program_d = self.xe_images.program_d
        self.zip_d = self.xe_images.zip_d
        self.homeImg = self.xe_images.homeImg
        self.aboutImg = self.xe_images.aboutImg
        self.settingsImg = self.xe_images.settingsImg
       
        self.create_widgets(app)



    def create_widgets(self, app):       
        self.btn_bottom = ctk.CTkFrame(self, fg_color=app.colors.primary_color, height=80, width= 150)
       
        self.home_btn = ctk.CTkButton(self, command=self.open_home_page, corner_radius=5,font=app.font11_bold, width=120,height=30, text='Home', hover=False,fg_color=app.colors.utils_color)
        self.filter_files_box = ctk.CTkFrame(self, height=300, width=130, fg_color='transparent')
        self.video_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Videos',anchor='w', font=app.font10_bold,text_color=app.colors.text_color,fg_color='transparent', image=self.video_d, compound='left')
        self.video_files.pack(fill='x',  pady=2)
        self.music_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Music',anchor='w', font=app.font10_bold,text_color=app.colors.text_color,fg_color='transparent', image=self.music_d, compound='left')
        self.music_files.pack(fill='x',  pady=2)
        self.document_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Document',anchor='w', font=app.font10_bold,text_color=app.colors.text_color,fg_color='transparent', image=self.document_d, compound='left')
        self.document_files.pack(fill='x',  pady=2)
        self.zip_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Compressed',anchor='w', font=app.font10_bold,text_color=app.colors.text_color,fg_color='transparent', image=self.zip_d, compound='left')
        self.zip_files.pack(fill='x',  pady=2)
        self.application_files = ctk.CTkLabel(self.filter_files_box,text=f'{' '}Application',anchor='w', font=app.font10_bold,text_color=app.colors.text_color,fg_color='transparent', image=self.program_d, compound='left')
        self.application_files.pack(fill='x',  pady=2)
        self.filter_files_box.place(x=60, y=90)
        self.filter_files_box.pack_propagate(False)
        self.about_btn = ctk.CTkButton(self.btn_bottom, command=self.open_about_page, corner_radius=5,font=app.font11_bold, width=120,height=30, text='About', hover=False,fg_color=app.colors.secondary_color)
        self.settings_btn = ctk.CTkButton(self.btn_bottom, command=self.open_settings_page, corner_radius=5,font=app.font11_bold, width=120,height=30, text='Settings', hover=False,fg_color=app.colors.secondary_color)

        self.home_btn.place(x=65, y=50)
        self.about_btn.pack(pady=5)
        self.settings_btn.pack(pady=5)

        self.side_bar_icon_btns = ctk.CTkFrame(self,fg_color=app.colors.secondary_color, width=50, corner_radius=5)
        self.side_bar_icon_btns.pack_propagate(False)
        self.icon_btn_bottom = ctk.CTkFrame(self.side_bar_icon_btns, height=80,width=50, fg_color=app.colors.secondary_color)
        self.home_icon_btn = ctk.CTkButton(self.side_bar_icon_btns, command= self.open_home_page, width=30,height=30, text='', hover_color=app.colors.secondary_color,fg_color=app.colors.secondary_color,image=self.homeImg)
        self.about_icon_btn = ctk.CTkButton(self.icon_btn_bottom, command= self.open_about_page, width=30,height=30, text='', hover_color=app.colors.secondary_color,fg_color=app.colors.secondary_color,image=self.aboutImg)
        self.settings_icon_btn = ctk.CTkButton(self.icon_btn_bottom, command= self.open_settings_page, width=30,height=30, text='', hover_color=app.colors.secondary_color,fg_color=app.colors.secondary_color,image=self.settingsImg)
        self.home_icon_btn.place(x=5, y=45)
        self.about_icon_btn.pack(pady=5)
        self.settings_icon_btn.pack(pady=5)
        self.icon_btn_bottom.pack(side='bottom', pady=20)
        self.side_bar_icon_btns.pack(side=ctk.LEFT, fill='y' , pady=5, padx=5)
        self.btn_bottom.pack(side='bottom', pady=25)
        self.pack_propagate(False) 

    


    def btns_to_default(self):
        self.home_btn.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.secondary_color)
        
        self.about_btn.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.secondary_color)
        self.settings_btn.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.secondary_color)

    ## remove widget from content-container
    def destroy_widgets_in_content_container(self):
        for child in self.app.file_list.winfo_children():
            child.destroy()


    ## pages lauching
    def open_home_page(self):
        self.app.about_page_opened = False
        self.app.settings_page_opened = False
        if self.app.home_page_opened:
            if self.app.about_frame:
                self.app.about_frame.destroy()

            else:
                self.app.about_frame = None

            if self.app.settings_frame:
                self.app.settings_frame.destroy()

            else:
                self.app.about_frame = None
        
            self.btns_to_default()
            self.home_btn.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.utils_color)
            self.update()
    
   
    def open_about_page(self):
         ## prevents opening page twice
        self.app.settings_page_opened = False
        if not self.app.about_page_opened:
            if self.app.settings_frame:
                self.app.settings_frame.destroy()
            
            self.btns_to_default()
            self.about_btn.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.utils_color)
            self.app.about_frame = About(self.app.content_area)
            self.app.about_frame.place(relwidth=1, relheight=1)
            self.app.about_page_opened = True
    def open_settings_page(self):
        ## prevents opening page twice
        self.app.about_page_opened = False
        if not self.app.settings_page_opened:
            if self.app.about_frame:
                self.app.about_frame.destroy()
            
            self.btns_to_default()
            self.settings_btn.configure(text_color=self.app.colors.text_color, fg_color=self.app.colors.utils_color)
            self.app.settings_frame = Settings(self.app.content_area)
            self.app.settings_frame.place(relwidth=1, relheight=1)
            self.app.settings_page_opened = True
        
class FileList(ctk.CTkScrollableFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=app.colors.secondary_color)

        