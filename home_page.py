import customtkinter as ctk
from customtkinter import CTkFont
import app_utils
class Home():
    def __init__(self, parent):
        self.xe_images = app_utils.Images()
        self.enter_link_box = ctk.CTkFrame(parent.content_container, height=200, width=400, fg_color='#3d539f', corner_radius=20, bg_color='#edeef0')
        self.enter_link_box.place(relx=.4, rely=.4, anchor='center')
        self.enter_link_box.pack_propagate(False)
        self.font =CTkFont(weight='bold', family='Helvetica', size=11)
        self.address_label = ctk.CTkLabel(self.enter_link_box,text_color='white',  font=self.font,text='Address').place(y=55, x=20)
        self.filename_label = ctk.CTkLabel(self.enter_link_box,text_color='white', font=self.font,text='Filename').place(y=90, x=20)

        self.status_label = ctk.CTkLabel(self.enter_link_box, text='xxx')
        self.status_label.pack(pady=10)

        self.link_text = ctk.StringVar()
        self.filename_text = ctk.StringVar()

       

        self.link_entry = ctk.CTkEntry(self.enter_link_box, height=30, width=250, textvariable=self.link_text,font=CTkFont(weight='bold', family='Helvetica', size=10), border_width=0, corner_radius=5, placeholder_text='insert link')
        self.link_entry.pack(pady=5)
        self.directory_box = ctk.CTkFrame(self.enter_link_box, fg_color='transparent')
        self.filename_entry = ctk.CTkEntry(self.directory_box, border_width=0, width=200, textvariable=self.filename_text,font=CTkFont(weight='bold', family='Helvetica', size=10), placeholder_text='file name', height=25)
        self.filename_entry.pack(side='left', fill='x')
        self.change_folder_btn = ctk.CTkButton(self.directory_box, text='', cursor='hand2', image=self.xe_images.folderImg, fg_color='#3d539f',width=20, height=25, hover=False)
        self.change_folder_btn.pack(side='left')
        self.directory_box.pack()
        self.start_download = ctk.CTkButton(self.enter_link_box,hover=False, cursor='hand2', text='Download',font=CTkFont(weight='bold', family='Helvetica', size=11), width=120, height=40, corner_radius=15, fg_color='#5b74d8')
        self.start_download.pack(pady=15)

        

        self.link_entry.bind('<KeyRelease>', self.getInputValue)

        app_utils.DownloadingIndicatorBox(parent)
    def getInputValue(self, event):
        print(self.link_text.get())


        