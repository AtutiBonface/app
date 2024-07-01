import customtkinter as ctk
from customtkinter import CTkFont
import app_utils , downloads_tasks

class DownloadingPage():
    def return_file_type(self, file_t):
        if file_t == 'Video':
            return self.xe_images.video_d
        elif file_t == 'Document':
            return self.xe_images.document_d
        elif file_t == 'Program':
            return self.xe_images.program_d
        elif file_t == 'Audio':
            return self.xe_images.music_d
        else:
            return self.xe_images.zip_d
    def return_arc_extent(self,percentage):

        extent = (359.9*percentage)/100

        return round(extent, 1)
    
    def update_ui(self, filename, size, complete, speed, file_type): 
        pass
    def propagate_file_btn(self,event):
        pass

    def item_clicked(self , me):
       
        if self.previously_clicked_btn:
            for i in self.previously_clicked_btn:  
                try:
                    i.configure(fg_color='#ffffff', text_color='black', bg_color='#ffffff')
                except:
                    i.configure(fg_color='#ffffff')
        
        new_color = 'transparent'
        self.file_btn.configure(fg_color='#3d539f')
        self.download_item.configure(fg_color=new_color, bg_color=new_color)
        self.file_download_speed.configure(fg_color=new_color, text_color='#ffffff')
        self.file_name.configure(fg_color=new_color, text_color='#ffffff')
        self.file_size.configure(fg_color=new_color, text_color='#ffffff')

        self.previously_clicked_btn = [
            self.file_btn,
            self.download_item,
            self.file_download_speed,
            self.file_name,
            self.file_size,
        ]


        
       
    
    
    def clear_btn_styles(self):
        self.all_down.configure(text_color="#edeef0", fg_color='#3d539f')
        self.downloading.configure(text_color="#edeef0", fg_color='#3d539f')
        self.failed.configure(text_color="#edeef0", fg_color='#3d539f')
    def all_downloads(self):
        self.clear_btn_styles()
        self.all_down.configure(text_color='#3d539f', fg_color='#2C3539')

    def downloading_downloads(self):
        self.clear_btn_styles()
        self.downloading.configure(text_color='#3d539f', fg_color='#2C3539')
    def failed_downloads(self):
        self.clear_btn_styles()
        self.failed.configure(text_color='#3d539f', fg_color='#2C3539')

    def __init__(self, parent):
       
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12 = CTkFont(weight='bold', family='Helvetica', size=11) 

       
        self.top_container = ctk.CTkFrame(parent.content_container, fg_color='#3d539f', height=100)
        self.no_of_down_box = ctk.CTkFrame(self.top_container, fg_color='red')
        self.segmented_btns = ctk.CTkFrame(self.top_container,width=150,  fg_color="#3d539f", corner_radius=10)
        
        self.all_down = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.all_downloads,text='All',width=50, height=30, hover=False,fg_color='#3d539f')
        self.downloading = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.downloading_downloads,text='Complete',width=60, height=30, hover=False,fg_color='#3d539f')
        self.failed = ctk.CTkButton(self.segmented_btns, font=self.font12,corner_radius=5,command=self.failed_downloads,text='Incomplete',width=50, height=30, hover=False,fg_color='#3d539f')

        self.all_down.pack(padx=5, pady=5,side='left')

        self.downloading.pack(padx=5, pady=5,side='left')

        self.failed.pack(padx=5, pady=5,side='left')
        self.segmented_btns.pack(side='right', padx=10, pady=2)  
        self.top_container.pack(fill='x', padx=5, pady=5)
        self.files_labels = ctk.CTkFrame(parent.content_container, fg_color='transparent', height=20)
        self.name_label = ctk.CTkLabel(self.files_labels,text_color='white',font=self.font12, text='Name', anchor='w')
        self.name_label.pack(side='left', padx=60)
        self.status_label = ctk.CTkLabel(self.files_labels,text_color='white',font=self.font12, text='Status',width=70,  anchor='w')
        self.date_label = ctk.CTkLabel(self.files_labels,text_color='white',font=self.font12, text='Date',width=60, anchor='w')
        self.size_label = ctk.CTkLabel(self.files_labels,text_color='white',font=self.font12, text='Size', width=60, anchor='w')
        self.size_label.pack(side='right', padx=5)
        self.date_label.pack(side='right', padx=5)
        self.status_label.pack(side='right', padx=5)

        self.files_labels.pack(fill='x')
        self.files_labels.pack_propagate(False)
        self.downloading_list = ctk.CTkScrollableFrame(parent.content_container, fg_color='#2C3539')
        self.downloading_list.pack(expand=True, fill='both')

        self.previously_clicked_btn = None
        
        self.all_downloads()

        self.xe_images = app_utils.Images()
    
        
      
        self.download_item = ctk.CTkFrame(self.downloading_list, fg_color='#353839',height=40,corner_radius=5, cursor='hand2')
        
        self.file_type = ctk.CTkLabel(self.download_item, text='', image=self.return_file_type('Program'), fg_color='transparent')
        self.file_type.pack(side='left', padx=10)

        self.file_name = ctk.CTkLabel(self.download_item, text_color='white',text="19818859/19818859-uhd_2732_1440_25fps.mp4", font=self.font12,fg_color='transparent', anchor='w')
        self.file_name.pack(side='left', fill='x', expand=True, padx=10, pady=1)
       
        self.file_size = ctk.CTkLabel(self.download_item,text=f"10mb",text_color='white',font=self.font12, fg_color='transparent', width=60)
        self.file_size.pack(side='right',  padx=5, pady=5)
        self.file_download_date = ctk.CTkLabel(self.download_item,text_color='white',text=f"7/10/2022",font=self.font12, width=60,fg_color='transparent')
        self.file_download_date.pack(side='right', padx=5, pady=5)
        self.download_status = ctk.CTkLabel(self.download_item,text_color='white', text="pending", width=70, font=self.font12)
        self.download_status.pack(side='right')

        self.download_item.pack(fill='x')
        self.download_item.pack_propagate(False)
        

        self.download_item.bind('<Button-1>', command=self.propagate_file_btn)
            
        
        self.file_size.bind('<Button-1>', command=self.propagate_file_btn)
        self.file_name.bind('<Button-1>', command=self.propagate_file_btn)
        self.file_download_date.bind('<Button-1>', command=self.propagate_file_btn)
        

        
    
       
                        
class moreOfDownloading():
    def __init__(self, parent):

        self.font11 = CTkFont(weight='bold', family='Helvetica', size=11)
        self.container = ctk.CTkFrame(parent.content_container, width=300, height=80, fg_color='#3d539f',bg_color='#edeef0', corner_radius=15)
        self.actions_label = ctk.CTkLabel(self.container, text="", height=10, font=self.font11, text_color='white')
        self.actions_label.place(y=10, relx=.5, anchor='center')
        self.actions = ctk.CTkFrame(self.container, fg_color='#3d539f', bg_color='transparent', height=70)

        self.xe_images =app_utils.Images()

        self.pause = ctk.CTkButton(self.actions, text='',command=lambda state='pause':self.change_download_state(state), image=self.xe_images.pause, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')
        self.resume = ctk.CTkButton(self.actions, text='',command=lambda state='resume':self.change_download_state(state), image=self.xe_images.play, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')
        self.restart = ctk.CTkButton(self.actions, text='',command=lambda state='restart':self.change_download_state(state), image=self.xe_images.restart, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')
        self.stop = ctk.CTkButton(self.actions, text='',command=lambda state='stop':self.change_download_state(state), image=self.xe_images.stop, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')

        self.pause.pack(side='left', padx=10, pady=10)
        self.resume.pack(side='left', padx=10, pady=10)
        self.stop.pack(side='left', padx=10, pady=10)
        self.restart.pack(side='left', padx=10, pady=10)
        

        self.actions.place(y=40, relx=.5, anchor='center')

        self.container.place(relx=.5,   rely=.96, anchor='center')
        self.container.pack_propagate(False)

        self.pause.bind('<Enter>', lambda event , state='pause':self.on_actions_enter(event, state))
        self.resume.bind('<Enter>', lambda event , state='resume':self.on_actions_enter(event, state))
        self.restart.bind('<Enter>', lambda event , state='restart':self.on_actions_enter(event, state))
        self.stop.bind('<Enter>', lambda event , state='stop':self.on_actions_enter(event, state))

        self.pause.bind('<Leave>', self.on_actions_leave)
        self.resume.bind('<Leave>', self.on_actions_leave)
        self.restart.bind('<Leave>', self.on_actions_leave)
        self.stop.bind('<Leave>', self.on_actions_leave)
        

        
        
    def change_download_state(self, state):
       
        print(state)

    def on_actions_enter(self, event, state):
        self.actions_label.configure(text=state)

    def on_actions_leave(self,event):
        self.actions_label.configure(text='')
        