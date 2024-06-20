import customtkinter as ctk
from customtkinter import CTkFont
import app_utils , downloads_tasks

class DownloadingPage():
    def clear_btn_styles(self):
        self.all_down.configure(text_color="#edeef0", fg_color='#3d539f')
        self.downloading.configure(text_color="#edeef0", fg_color='#3d539f')
        self.failed.configure(text_color="#edeef0", fg_color='#3d539f')
    def all_downloads(self):
        self.clear_btn_styles()
        self.all_down.configure(text_color='#3d539f', fg_color='#edeef0')

    def downloading_downloads(self):
        self.clear_btn_styles()
        self.downloading.configure(text_color='#3d539f', fg_color='#edeef0')
    def failed_downloads(self):
        self.clear_btn_styles()
        self.failed.configure(text_color='#3d539f', fg_color='#edeef0')

    def __init__(self, parent):
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12 = CTkFont(weight='normal', family='Helvetica', size=12) 
        

        self.top_container = ctk.CTkFrame(parent.content_container, fg_color='#edeef0', height=100)
        self.no_of_down_box = ctk.CTkFrame(self.top_container, fg_color='transparent')
        self.no_of_down_label = ctk.CTkLabel(self.no_of_down_box, anchor='se',fg_color='transparent',height=20, text='Maximum Downloads')
        self.no_of_down_label.pack(fill='x', padx=20, pady=5)
        values = ["1","2","3","4","5","6","7","8","9","10"]
        number_var = ctk.StringVar()
        number_var.set("3")
        self.set_max_download = ctk.CTkComboBox(self.no_of_down_box,button_color='#3d539f',button_hover_color='white', dropdown_fg_color='white',border_color='#3d539f', values=values, variable=number_var, corner_radius=10, fg_color='#edeef0')
        self.set_max_download.pack(side='right', padx=10)
        self.no_of_down_box.pack(fill='x')

        self.segmented_btns = ctk.CTkFrame(self.top_container,width=150,  fg_color="#3d539f", corner_radius=10)
        
        self.all_down = ctk.CTkButton(self.segmented_btns, font=self.font14,corner_radius=20,command=self.all_downloads,text='All',width=50, height=30, hover=False,fg_color='#3d539f')
        self.downloading = ctk.CTkButton(self.segmented_btns, font=self.font14,corner_radius=20,command=self.downloading_downloads,text='Downloading',width=60, height=30, hover=False,fg_color='#3d539f')
        self.failed = ctk.CTkButton(self.segmented_btns, font=self.font14,corner_radius=20,command=self.failed_downloads,text='Failed',width=50, height=30, hover=False,fg_color='#3d539f')

        self.all_down.pack(padx=5, pady=5,side='left')

        self.downloading.pack(padx=5, pady=5,side='left')

        self.failed.pack(padx=5, pady=5,side='left')
        self.segmented_btns.pack(side='right', padx=10, pady=2)  
        self.top_container.pack(fill='x')
        self.downloading_list = ctk.CTkScrollableFrame(parent.content_container, fg_color='#edeef0')
        self.downloading_list.pack(expand=True, fill='both')

        self.previously_clicked_btn = None

        tasks = downloads_tasks.DownloadingTask()
        for task in tasks.files:
            DownloadFile(self ,task['name'], task['size'], task['speed'], task['complete'], task['type'])

        moreOfDownloading(parent)
        self.all_downloads()
       
        
class DownloadFile():
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


    def __init__(self, parent, name, size, speed, complete, f_type):
        self.blue = '#3d539f'
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12 = CTkFont(weight='normal', family='Helvetica', size=12)   
        self.file_btn = ctk.CTkButton(parent.downloading_list, fg_color='#ffffff',command= lambda : self.item_clicked(self.file_btn, parent), height=60, cursor='hand2')
        self.download_item = ctk.CTkFrame(self.file_btn, fg_color='transparent', cursor='hand2')
        self.canvas_box = ctk.CTkFrame(self.download_item, height=60, width=60, fg_color="#3d539f")
        self.my_canvas = ctk.CTkCanvas(self.canvas_box, height=60, width=60, bg='#3d539f', highlightbackground='#3d539f', highlightcolor='#3d539f', insertbackground='#3d539f' )
        self.my_canvas.place(relx=.5, rely=.5, anchor='center')
        self.canvas_box.pack(side='left', padx=5, pady=5)
        self.canvas_box.pack_propagate(False)
        self.my_canvas.create_oval(5, 5 ,55, 55,width=5, outline='#5b74d8')
        self.my_canvas.create_arc(5,5, 55, 55, start=90, extent=-self.return_arc_extent(complete), width=5, outline='#edeef0', style=ctk.ARC)
        self.my_canvas.create_text(30, 30, text=f'{complete}%', fill='black',font=self.font14)

        self.xe_images = app_utils.Images()

        self.file_type = ctk.CTkLabel(self.download_item, text='', image=self.return_file_type(f_type), fg_color='transparent')
        self.file_type.pack(side='left')

        self.file_name = ctk.CTkLabel(self.download_item,text=name, font=self.font14,fg_color='transparent', anchor='sw')
        self.file_name.pack(side='top', fill='x', padx=10, pady=1)

        self.file_size = ctk.CTkLabel(self.download_item,text=f"Size : {size}",font=self.font12, fg_color='transparent', anchor='sw')
        self.file_size.pack(side='left', fill='x',expand=True, padx=10, pady=5)
        self.file_download_speed = ctk.CTkLabel(self.download_item,text=f"Speed : {speed}",font=self.font14,fg_color='transparent', anchor='se')
        self.file_download_speed.pack(side='left', fill='x',expand=True, padx=10, pady=5)

        self.download_item.place(x=5, y=0, relwidth=.97, relheight=1.0)
        self.download_item.pack_propagate(False)
        self.file_btn.pack(fill='x', pady=5, padx=10)

        self.download_item.bind('<Button-1>', command=self.propagate_file_btn)
            
        
        self.file_size.bind('<Button-1>', command=self.propagate_file_btn)
        self.file_name.bind('<Button-1>', command=self.propagate_file_btn)
        self.file_download_speed.bind('<Button-1>', command=self.propagate_file_btn)


        #parent.files_on_list.append(self.file_btn)

        

        
            


    def propagate_file_btn(self,event):
        self.file_btn.invoke()

    def item_clicked(self , me, parent):
       
        if parent.previously_clicked_btn:
            for i in parent.previously_clicked_btn:  
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

        parent.previously_clicked_btn = [
            self.file_btn,
            self.download_item,
            self.file_download_speed,
            self.file_name,
            self.file_size,
        ]
                        
class moreOfDownloading():
    def __init__(self, parent):

      
        self.container = ctk.CTkFrame(parent.content_container, height=80, fg_color='#3d539f',bg_color='#edeef0', corner_radius=15)

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
        

        self.actions.place(y=20, relx=.5, anchor='center')

        self.container.place(relx=.5,relwidth=.5, rely=1, anchor='center')
        
    def change_download_state(self, state):
        print(state)
