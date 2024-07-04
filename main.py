import customtkinter as ctk
import app_utils
from app_utils import Colors
from add_link import LinkBox
from customtkinter import CTkFont
from xdm import TaskManager
from about import About
from settings import Settings

class MyApp(ctk.CTk):
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')

    def update_ui(self, filename, size, complete, speed, file_type):
        print(filename, size, complete, speed, file_type)

    def return_file_type(self, file_t):
        if file_t == 'Video':
            return self.xe_images.video_d2
        elif file_t == 'Document':
            return self.xe_images.document_d2
        elif file_t == 'Program' or file_t == 'Application':
            return self.xe_images.program_d2
        elif file_t == 'Audio' or file_t == 'Music':
            return self.xe_images.music_d2
        elif file_t == 'Zip' or file_t == 'Compressed':
            return self.xe_images.zip_d2
        else: return self.xe_images.document_d2
    def return_arc_extent(self,percentage):

        extent = (359.9*percentage)/100

        return round(extent, 1)
    
    
    

    
    def clear_btn_styles(self):
        self.all_down.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.downloading.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.failed.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
    def all_downloads(self):
        self.clear_btn_styles()
        self.all_down.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)

    def downloading_downloads(self):
        self.clear_btn_styles()
        self.downloading.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
    def failed_downloads(self):
        self.clear_btn_styles()
        self.failed.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)

       
    def btns_to_default(self):
        self.home_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        
        self.about_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)
        self.settings_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.secondary_color)

    ## remove widget from content-container
    def destroy_widgets(self):
        for child in self.content_container.winfo_children():
            child.destroy()


    ## pages lauching
    def open_home_page(self):
        if self.about_frame:
            self.about_frame.destroy()

        if self.settings_frame:
            self.settings_frame.destroy()

        
        self.about_frame = About(self.content_container)
        self.index_of_page_opened = 0
        self.btns_to_default()
        self.home_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
        self.side_nav_bar.update()
    
     
        
   
    def open_about_page(self):
        
        if self.settings_frame:
            self.settings_frame.destroy()
        
        
        
        self.btns_to_default()
        self.index_of_page_opened = 3
        self.about_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
        self.about_frame = About(self.content_container)
        self.about_frame.place(relwidth=1, relheight=1)
    def open_settings_page(self):
        if self.about_frame:
            self.about_frame.destroy()
        
        self.btns_to_default()
        self.index_of_page_opened = 4
        self.settings_btn.configure(text_color=self.colors.text_color, fg_color=self.colors.utils_color)
        self.settings_frame = Settings(self.content_container)
        self.settings_frame.place(relwidth=1, relheight=1)


    def open_link_box(self):
        LinkBox(self, self.xdm_class)



    def __init__(self):
        super().__init__()
        

        self.index_of_page_opened = 0 # 0 home // 1 downloadin // 2 downloaded // 3 about // 4 settings
        self.about_frame = None
        self.settings_frame = None
      
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
        
        self.all_down = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.all_downloads,text='All',width=50, height=30, hover=False,fg_color=self.colors.secondary_color)
        self.downloading = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.downloading_downloads,text='Complete',width=60, height=30, hover=False,fg_color=self.colors.secondary_color)
        self.failed = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.failed_downloads,text='Incomplete',width=50, height=30, hover=False,fg_color=self.colors.secondary_color)

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
        
       
        
        
        self.xdm_class = TaskManager(self)
        File(self, 'home.png', '6M', 100, 1.5, 'Zip')
        File(self, 'rihanna-work-ft-drake-.mp4', '27M', 100, 1, 'Video')
        File(self, 'with-you-ft-ChrisBrown', '3.5M', 100, 1.2, 'Music')
        File(self, 'file.html', '300Kb', 100, 1.8, 'Document')
        File(self, 'Xengine Downloader.exe', '57M', 100, 0.8, 'Program')
        moreOfDownloading(self)
        
        

class moreOfDownloading():
    def __init__(self, parent):
        self.parent = parent
        self.colors = Colors()
        self.font11 = CTkFont(weight='bold', family='Helvetica', size=11)
        self.container = ctk.CTkFrame(parent.content_container, height=50, fg_color=self.colors.primary_color,bg_color='transparent', corner_radius=5)
        self.actions_label = ctk.CTkLabel(self.container, text="", anchor='w', fg_color='transparent', height=10, font=self.font11, text_color=self.colors.text_color)
        self.actions_label.pack(padx=10, fill='x', expand=True)
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
        

        
        
    def change_download_state(self, state,me):
        if self.parent.previously_clicked_file:       
            print(state)
            me.configure(fg_color = self.colors.utils_color)
        else:
            print("Nothing has been selected")

    def on_actions_enter(self, event, state):
        self.actions_label.configure(text=state)

    def on_actions_leave(self,event, me):
        self.actions_label.configure(text='')
        me.configure(fg_color=self.colors.secondary_color)
class File():
   
    

    def propagate_file_btn(self,event, parent):
        if parent.previously_clicked_file:
            for i in parent.previously_clicked_file:  
                try:
                    i.configure(fg_color=parent.colors.secondary_color, text_color=parent.colors.text_color)
                except:
                    i.configure(fg_color=parent.colors.secondary_color)
        

        self.download_item.configure(fg_color=parent.colors.utils_color)
        self.file_type.configure(fg_color=parent.colors.utils_color)
        self.download_status.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)
        self.file_size.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)
        self.file_name.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)
        self.file_download_date.configure(fg_color=parent.colors.utils_color, text_color=parent.colors.secondary_color)

        ## adding clic
        parent.previously_clicked_file = [
            self.download_item,
            self.file_name,
            self.file_size,
            self.file_type,
            self.file_download_date,
            self.download_status,
        ]


    def __init__(self, parent, filename, size, complete, speed, file_type) -> None:
        self.task_name = filename
        self.download_item = ctk.CTkFrame(parent.downloading_list, fg_color=parent.colors.secondary_color,height=40,corner_radius=5, cursor='hand2')
        
        self.file_type = ctk.CTkLabel(self.download_item, text='', image=parent.return_file_type(file_type), fg_color='transparent')
        self.file_type.pack(side='left', padx=10)

        self.file_name = ctk.CTkLabel(self.download_item, text_color=parent.colors.text_color,text=filename, font=parent.font11,fg_color='transparent', anchor='w')
        self.file_name.pack(side='left', fill='x', expand=True, padx=10, pady=1)
       
        self.file_size = ctk.CTkLabel(self.download_item,text=f"{size}",text_color=parent.colors.text_color,font=parent.font12, fg_color='transparent', width=60)
        self.file_size.pack(side='right',  padx=5, pady=5)
        self.file_download_date = ctk.CTkLabel(self.download_item,text_color=parent.colors.text_color,text=f"7/10/2022",font=parent.font12, width=60,fg_color='transparent')
        self.file_download_date.pack(side='right', padx=5, pady=5)
        self.download_status = ctk.CTkLabel(self.download_item,text_color=parent.colors.text_color, text=complete, width=70, font=parent.font12)
        self.download_status.pack(side='right')

        self.download_item.pack(fill='x')
        self.download_item.pack_propagate(False)
        

        self.download_item.bind('<Button-1>', command=lambda event: self.propagate_file_btn(event, parent))
        self.file_type.bind('<Button-1>', command=lambda event: self.propagate_file_btn(event, parent))
        self.download_status.bind('<Button-1>', command=lambda event: self.propagate_file_btn(event, parent))
        self.file_size.bind('<Button-1>', command=lambda event: self.propagate_file_btn(event, parent))
        self.file_name.bind('<Button-1>', command=lambda event: self.propagate_file_btn(event, parent))
        self.file_download_date.bind('<Button-1>', command=lambda event: self.propagate_file_btn(event, parent))
app = MyApp()
app.mainloop()