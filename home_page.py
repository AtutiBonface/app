import customtkinter as ctk
from customtkinter import CTkFont
import app_utils
class Home():
    def __init__(self, parent):
        self.enter_link_box = ctk.CTkFrame(parent.content_container, height=200, width=300, fg_color='#3d539f', corner_radius=20, bg_color='#edeef0')
        self.enter_link_box.place(relx=.4, rely=.4, anchor='center')
        self.enter_link_box.pack_propagate(False)

        self.link_entry = ctk.CTkEntry(self.enter_link_box, height=30, width=200,font=CTkFont(weight='bold', family='Helvetica', size=10), corner_radius=10, placeholder_text='insert link').pack(pady=50)

        self.start_download = ctk.CTkButton(self.enter_link_box, text='Download',font=CTkFont(weight='bold', family='Helvetica', size=11), width=120, height=40, corner_radius=15, fg_color='#5b74d8').place(rely=.7, relx=.5, anchor='center')


        app_utils.DownloadingIndicatorBox(parent)