import customtkinter as ctk
import tkinter as tk
from customtkinter import CTkFont, CTkImage
from PIL import Image

class DownloadingPage(ctk.CTk):
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
    def __init__(self):
        super().__init__()


        self.geometry('800x500+300+100')

        self.hero_container = ctk.CTkFrame(self, fg_color='green')
        self.hero_container.pack(expand=True, fill=ctk.BOTH)

        self.top_container = ctk.CTkFrame(self.hero_container, fg_color='red', height=100)
        self.top_container.pack(fill='x')
        self.downloading_list = ctk.CTkScrollableFrame(self.hero_container, fg_color='#edeef0')
        self.downloading_list.pack(expand=True, fill='both')
        values = ["1","2","3","4","5","6","7","8","9","10"]
        number_var = ctk.StringVar()
        number_var.set("3")
        self.set_max_download = ctk.CTkComboBox(self.top_container, values=values, variable=number_var).pack()

        self.segmented_btns = ctk.CTkFrame(self.top_container,width=180,  fg_color="#3d539f", corner_radius=20)
        
        self.all_down = ctk.CTkButton(self.segmented_btns, corner_radius=20,command=self.all_downloads,text='All',width=60, height=32, hover=False,fg_color='#3d539f')
        self.downloading = ctk.CTkButton(self.segmented_btns, corner_radius=20,command=self.downloading_downloads,text='Downloading',width=60, height=32, hover=False,fg_color='#3d539f')
        self.failed = ctk.CTkButton(self.segmented_btns, corner_radius=20,command=self.failed_downloads,text='Failed',width=60, height=32, hover=False,fg_color='#3d539f')

        self.all_down.pack(padx=5, pady=5,side='left')

        self.downloading.pack(padx=5, pady=5,side='left')

        self.failed.pack(padx=5, pady=5,side='left')
        self.segmented_btns.pack()

        
        
        self.files_on_list = []
        self.previous_clicked_file = None
        
        self.files = DownloadingTask().files
        self.files_on_list = []
        self.previous_clicked_file = None
        self.state_popup_open = None
        

        for btn in self.files:
            name = btn
            DownloadFile(self).create_button(self, name)

        


            

        
class DownloadFile():
    def __init__(self, parent):
        self.blue = '#3d539f'
        self.font14 = CTkFont(weight='bold', family='Helvetica', size=14)
        self.font12 = CTkFont(weight='normal', family='Helvetica', size=12)

       

        moreOfDownloading(parent)


    def create_button(self, parent, name):
        self.file_btn = ctk.CTkButton(parent.downloading_list, fg_color='#ffffff',command= lambda : self.item_clicked(self.file_btn, parent), height=60, cursor='hand2')
        self.download_item = ctk.CTkFrame(self.file_btn, fg_color='transparent', cursor='hand2')
        self.canvas_box = ctk.CTkFrame(self.download_item, height=60, width=60, fg_color="#3d539f")
        self.my_canvas = ctk.CTkCanvas(self.canvas_box, height=60, width=60, bg='#3d539f', highlightbackground='#3d539f', highlightcolor='#3d539f', insertbackground='#3d539f' )
        self.my_canvas.place(relx=.5, rely=.5, anchor='center')
        self.canvas_box.pack(side='left', padx=5, pady=5)
        self.canvas_box.pack_propagate(False)
        self.my_canvas.create_oval(5, 5 ,55, 55,width=5, outline='#5b74d8')
        self.my_canvas.create_arc(5,5, 55, 55, start=90, extent=-10, width=5, outline='#edeef0', style=ctk.ARC)
        self.my_canvas.create_text(30, 30, text='90%', fill='black',font=self.font14)

        self.xe_images = Images()

        self.file_type = ctk.CTkLabel(self.download_item, text='', image=self.xe_images.video_d, fg_color='transparent')
        self.file_type.pack(side='left')

        self.file_name = ctk.CTkLabel(self.download_item,text=name, font=self.font14,fg_color='transparent', anchor='sw')
        self.file_name.pack(side='top', fill='x', padx=10, pady=1)

        self.file_size = ctk.CTkLabel(self.download_item,text="Size : 235 MB",font=self.font12, fg_color='transparent', anchor='sw')
        self.file_size.pack(side='left', fill='x',expand=True, padx=10, pady=5)
        self.file_download_speed = ctk.CTkLabel(self.download_item,text="Speed : 1.5mb/s",font=self.font14,fg_color='transparent', anchor='se')
        self.file_download_speed.pack(side='left', fill='x',expand=True, padx=10, pady=5)

        self.download_item.place(x=5, y=0, relwidth=.97, relheight=1.0)
        self.download_item.pack_propagate(False)
        self.file_btn.pack(fill='x', pady=5, padx=10)

        self.download_item.bind('<Button-1>', command=self.propagate_file_btn)
            
       
        self.file_size.bind('<Button-1>', command=self.propagate_file_btn)
        self.file_name.bind('<Button-1>', command=self.propagate_file_btn)
        self.file_download_speed.bind('<Button-1>', command=self.propagate_file_btn)


        parent.files_on_list.append(self.file_btn)


        
            


    def propagate_file_btn(self,event):
        self.file_btn.invoke()

    def item_clicked(self , me, parent):
       
        if parent.previous_clicked_file:
            for i in parent.previous_clicked_file:  
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

        parent.previous_clicked_file = [
            self.file_btn,
            self.download_item,
            self.file_download_speed,
            self.file_name,
            self.file_size,
        ]
        
           
        
        
                        
class moreOfDownloading():
    def __init__(self, parent):

        self.colors = ''
        self.font12 = ''
        self.container = ctk.CTkFrame(parent.hero_container, height=100, fg_color='#3d539f',bg_color='#edeef0', corner_radius=15)

        self.actions = ctk.CTkFrame(self.container, fg_color='#3d539f', bg_color='transparent', height=70)

        self.xe_images = Images()

        self.pause = ctk.CTkButton(self.actions, text='',command=lambda state='pause':self.change_download_state(state), image=self.xe_images.pause, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')
        self.resume = ctk.CTkButton(self.actions, text='',command=lambda state='resume':self.change_download_state(state), image=self.xe_images.play, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')
        self.restart = ctk.CTkButton(self.actions, text='',command=lambda state='restart':self.change_download_state(state), image=self.xe_images.restart, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')
        self.stop = ctk.CTkButton(self.actions, text='',command=lambda state='stop':self.change_download_state(state), image=self.xe_images.stop, width=30, hover_color='black', cursor='hand2',height=30, fg_color='#5b74d8')

        self.pause.pack(side='left', padx=10, pady=10)
        self.resume.pack(side='left', padx=10, pady=10)
        self.stop.pack(side='left', padx=10, pady=10)
        self.restart.pack(side='left', padx=10, pady=10)
        

        self.actions.place(rely=.2, relx=.5, anchor='center')

        self.container.place(relx=.5,relwidth=.5, rely=1, anchor='center')
        
    def remove_popup(self, ob):
        if ob.state_popup_open:
            ob.state_popup_open.destroy()
    def change_download_state(self, state):
        print(state)

    
        
        
            



        

    
class Images():
    def __init__(self):


        
        self.homeImg = CTkImage(Image.open('images/home.png'), size=(25,25))
        self.settingsImg = CTkImage(Image.open('images/settings.png'),  size=(25,25))
        self.downloadImg = CTkImage(Image.open('images/download.png'),  size=(25,25))
        self.aboutImg = CTkImage(Image.open('images/about.png'),  size=(25,25))
        self.folderImg = CTkImage(Image.open('images/folder.png'),  size=(25,25))

        self.document_d = CTkImage(Image.open('images/document_d.png'),  size=(30,30))
        self.program_d = CTkImage(Image.open('images/program_d.png'),  size=(30,30))
        self.zip_d = CTkImage(Image.open('images/zip_d.png'),  size=(30,30))
        self.music_d = CTkImage(Image.open('images/music_d.png'),  size=(30,30))
        self.video_d = CTkImage(Image.open('images/video_d.png'),  size=(30,30))

        self.pause = CTkImage(Image.open('images/pause.png'),  size=(20,20))
        self.play = CTkImage(Image.open('images/play.png'),  size=(20,20))
        self.restart = CTkImage(Image.open('images/restart.png'),  size=(20,20))
        self.stop = CTkImage(Image.open('images/stop.png'),  size=(20,20))

class DownloadingTask():
    def __init__(self) :
        self.files = [
            'Into the Badlands',
            'Into the Badlands',
            'Into the Badlands',
            'Into the Badlands',
            'Into the Badlands',
            'Into the Badlands',
            'Into the Badlands',
           
            
        ]
page = DownloadingPage()
page.mainloop()

