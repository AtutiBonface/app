import customtkinter as ctk
import app_utils , os, sys, asyncio , websockets, threading , json
from app_utils import Colors
from file_actions import actionsForDisplayedFiles, More
from add_link import LinkBox
from customtkinter import CTkFont
from progress import Progressor
from xdm import TaskManager
from about import About
from settings import Settings
from file_ui import File
from app_utils import OtherMethods
import database, queue
import tkinter as tk
class MyApp(ctk.CTk):
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')
        
    async def handle_websockets(self, websocket, path):
              
        try:
            async for message in websocket:
                if message:
                    data = json.loads(message)
                    filename = data['name']
                    url = data['link']

                    self.after(0, lambda : self.openUrlPopup(url =url, filename=filename))
                else:
                    pass
        except Exception as e:
            pass

    def openUrlPopup(self, url , filename):
        link_box = LinkBox(self, self.xdm_class)
        link_box.update_idletasks()
        link_box.link_text.set(url)
        link_box.filename_text.set(filename)
    async def extension_main(self):
        async with websockets.serve(self.handle_websockets, '127.0.0.1', 65432):
            await asyncio.Future()
    

    def clear_download_list_from_page(self):
        self.previously_clicked_btn = None
        self.previously_clicked_file = None
        for child in self.downloading_list.winfo_children():
            if child:
                child.destroy()
    def clear_btn_styles(self):
        self.all_down.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.downloading.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.failed.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
    def filter_all_downloads(self):
        
        self.clear_btn_styles()
        self.all_down.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
        self.display_all_downloads_on_page()

    def filter_complete_downloads(self):
        
        self.clear_btn_styles()
        self.downloading.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
        self.display_complete_downloads_on_page()
    def filter_incomplete_downloads(self):
        
        self.clear_btn_styles()
        self.failed.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
        self.display_incomplete_downloads_on_page()

       
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

    

    def start_thread_for_browser_links(self):
        asyncio.run(self.extension_main())


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

    def return_all_downloads(self):
        return self.xengine_downloads
    
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

        self.progress_toplevels[filename] = Progressor(self)

        self.progress_toplevels[filename].start(filename, address, status, size, downloaded, path)
        if  self.progress_toplevels[filename].progress_bar.winfo_exists():
            self.progress_toplevels[filename].progress_bar.start()
        else:
           pass
        


    def update_download(self, filename, status, size, downloaded ,date, speed):
        name = os.path.basename(filename)
        path = self.xengine_downloads[name]['path']

        
        
        if name in self.xengine_downloads:
           
            self.xengine_downloads[name]['status'] = status
            self.xengine_downloads[name]['filesize'] = size
            self.xengine_downloads[name]['modification_date'] = date
            self.xengine_downloads[name]['downloaded'] = downloaded
            self.update_queue.put((name, status, size, downloaded ,date))

            if name in self.progress_toplevels:
                
                try:
                    progressor = self.progress_toplevels[name]
                    if  progressor.winfo_exists():
                        if progressor.progress_bar.winfo_exists():
                            progressor.progress_bar.stop()
                            progressor.progress_bar.configure(mode='determinate')                            
                    
                
                        #progressor.update_progressor_ui(name,size,downloaded, path, status, speed)

                        self.after(0, progressor.update_progressor_ui, name,size,downloaded, path, status, speed)
                    else:
                        
                        del self.progress_toplevels[name]
                except tk.TclError as e:
                    del self.progress_toplevels[name]


               
            

            

    def process_updates(self):
        while True:
            try:
                filename, status, size, downloaded ,date = self.update_queue.get(timeout=0.1)
                self.update_file_widget(filename, status, size, downloaded ,date)
                                
            except queue.Empty:
                continue

    def update_file_widget(self, filename, status, size, downloaded ,date):
        
        
        if filename in self.file_widgets:
            self.file_widgets[filename].update_file_info(status, size, date)
        else:
            self.add_new_file_widget(filename, status, size, date)

    def add_new_file_widget(self, filename, status, size, date):       

        new_widget = File(self, filename, size, status, date, self.xengine_downloads[filename]['path'])
        new_widget.pack(fill='x')
        self.file_widgets[filename] = new_widget
        
    def display_all_downloads_on_page(self):
        self.previously_clicked_btn = None
        self.previously_clicked_file = None
        for filename, detail in self.return_all_downloads().items():
            if filename not in self.file_widgets:
                self.add_new_file_widget(filename, detail['status'], detail['filesize'], detail['modification_date'])
                
            elif self.file_widgets[filename].winfo_exists():
                self.file_widgets[filename].resetFileStyles()
                
        
            
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



    def display_incomplete_downloads_on_page(self):
        self.previously_clicked_btn = None
        self.previously_clicked_file = None
        for filename, detail in self.return_all_downloads().items():
            if filename  in self.file_widgets  and not detail['status'] == 'completed.' and self.file_widgets[filename].winfo_exists():
                pass
            elif filename in self.file_widgets and self.file_widgets[filename].winfo_exists():
                self.file_widgets[filename].destroy()
                del self.file_widgets[filename]
            else:
                if not detail['status'] == 'completed.':
                    self.add_new_file_widget(filename, detail['status'], detail['filesize'], detail['modification_date'])


    
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

                self.progress_toplevels[name] = Progressor(self)                
                self.progress_toplevels[name].start(name, details['url'], 'resuming...',details['filesize'] ,self.downloaded_chuck, details['path'])
                if  self.progress_toplevels[name].progress_bar.winfo_exists():
                        self.progress_toplevels[name].progress_bar.start()
                        self.progress_toplevels[name].progress_bar.configure(mode='indeterminate')
                    

                asyncio.run_coroutine_threadsafe(self.xdm_class.resume_downloads_fn(filename_with_path,  details['url'], self.downloaded_chuck), self.xdm_class.loop)
        
        
        


    def __init__(self):
        super().__init__()
        database.initiate_database()## creates table if it does not exist
        self.update_queue = queue.Queue()
        self.other_methods = OtherMethods()
        
        self.index_of_page_opened = 0 # 0 home // 1 downloadin // 2 downloaded // 3 about // 4 settings
        self.about_frame = None
        self.settings_frame = None

        self.filter_page = 'all'

        self.progress_toplevels = {}
      
        

        self.about_page_opened = False
        self.settings_page_opened = False
        self.home_page_opened = True

        self.xengine_downloads = {}
        self.load_downloads_from_db()
        
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
        self.resizable(False, False)
        self.iconbitmap(self.other_methods.resource_path('xe-logos/main.ico'))
        self.title('BlackJuice')
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
        self.about_btn = ctk.CTkButton(self.btn_bottom, command=self.open_about_page, corner_radius=5,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='About', hover=False,fg_color=self.colors.secondary_color)
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
        self.btn_bottom.pack(side='bottom', pady=25)
        self.side_nav_bar.pack(fill=ctk.Y, side='left')
        self.side_nav_bar.pack_propagate(False)

        self.content_container = ctk.CTkFrame(self.app_container, fg_color=self.colors.secondary_color, corner_radius=0)
        self.content_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.search_entry = ctk.CTkEntry(self.app_container, width=200, height=30, placeholder_text="Search", corner_radius=5,border_color='#3d539f', bg_color=self.colors.text_color)
        self.top_container = ctk.CTkFrame(self.content_container, fg_color=self.colors.primary_color, height=100)
        self.add_link = ctk.CTkButton(self.top_container,image=self.xe_images.link,command=self.open_link_box, text='New',hover=False,cursor='hand2',font=self.font12,fg_color=self.colors.secondary_color,  width=50).pack(padx=10, side='left')
        self.segmented_btns = ctk.CTkFrame(self.top_container,width=150,  fg_color="transparent", corner_radius=5)
        
        self.all_down = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.filter_all_downloads,text='All',width=50, height=30, hover=False,fg_color=self.colors.secondary_color)
        self.downloading = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.filter_complete_downloads,text='Complete',width=60, height=30, hover=False,fg_color=self.colors.secondary_color)
        self.failed = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.filter_incomplete_downloads,text='Incomplete',width=50, height=30, hover=False,fg_color=self.colors.secondary_color)

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

        self.previously_clicked_btn = None
        self.details_of_file_clicked = None

        self.more_actions = None

        self.running_tasks = {}
        self.file_widgets = {}
        self.last_mtime = None
        self.w_state = self.wm_state()      
        self.xdm_class = TaskManager(self)

       
        actionsForDisplayedFiles(self)


        self.filter_all_downloads()


        

    def show_more(self, event):
        if not self.more_actions:
            self.more_actions = More(self)
            self.more_actions.place(relx=.955, rely=.95, anchor='se')
            self.more_actions.pack_propagate(False)   
        self.more_actions = None

   
    
if __name__ == "__main__":
    app = MyApp()
    extension_thread = threading.Thread(target=app.start_thread_for_browser_links, daemon=True)
    extension_thread.start()
    update_ui_thread = threading.Thread(target=app.process_updates, daemon=True)
    update_ui_thread.start()
    app.mainloop()