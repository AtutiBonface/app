import customtkinter as ctk
import home_page
import app_utils
import downloading_page
import downloaded_page
import about_page
import settings_page
from customtkinter import CTkFont

class MyApp(ctk.CTk):
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')
    def change_btn_color(self, event, me):
        me.configure(text_color='#3d539f', fg_color='#5b74d8')
        
       
    def revert_btn_color(self, event , me, myindex):
       
        if self.index_of_page_opened == myindex:
            me.configure(text_color='#3d539f', fg_color='#edeef0')
        else:
            me.configure(text_color='#edeef0', fg_color='#3d539f')

    def btns_to_default(self):
        self.home_btn.configure(text_color='#edeef0', fg_color='#3d539f')
        self.downloading_btn.configure(text_color='#edeef0', fg_color='#3d539f')
        self.downloaded_btn.configure(text_color='#edeef0', fg_color='#3d539f')
        self.about_btn.configure(text_color='#edeef0', fg_color='#3d539f')
        self.settings_btn.configure(text_color='#edeef0', fg_color='#3d539f')

    ## remove widget from content-container
    def destroy_widgets(self):
        for child in self.content_container.winfo_children():
            child.destroy()


    ## pages lauching
    def open_home_page(self):
        self.destroy_widgets()
        home_page.Home(self)
        self.index_of_page_opened = 0
        self.btns_to_default()
        self.home_btn.configure(text_color='#3d539f', fg_color='#edeef0')
        self.side_nav_bar.update()
    
    def open_downloading_page(self):
        self.destroy_widgets()
        self.btns_to_default()
        downloading_page.DownloadingPage(self)
        self.index_of_page_opened = 1      
        self.downloading_btn.configure(text_color='#3d539f', fg_color='#edeef0')
        
    def open_downloaded_page(self):
        self.destroy_widgets()
        self.btns_to_default()
        downloaded_page.Downloadedpage(self)
        self.index_of_page_opened = 2
        self.downloaded_btn.configure(text_color='#3d539f', fg_color='#edeef0')
    def open_about_page(self):
        self.destroy_widgets()
        self.btns_to_default()
        self.index_of_page_opened = 3
        self.about_btn.configure(text_color='#3d539f', fg_color='#edeef0')
       
    def open_settings_page(self):
        self.destroy_widgets()
        self.btns_to_default()
        self.index_of_page_opened = 4
        self.settings_btn.configure(text_color='#3d539f', fg_color='#edeef0')
      
    def __init__(self):
        super().__init__()
        self.xe_images = app_utils.Images()

        self.index_of_page_opened = 0 # 0 home // 1 downloadin // 2 downloaded // 3 about // 4 settings

        self.geometry('800x500+300+100')
        self.minsize(800,500)
        self.iconbitmap('xe-logos/main.ico')
        self.title('Xengine Downloader')

        self.app_container = ctk.CTkFrame(self)
        self.app_container.pack(expand=True, fill='both')

        
        self.side_nav_bar = ctk.CTkFrame(self.app_container, width=200, fg_color='#3d539f', corner_radius=20, bg_color="#edeef0")
        self.btn_bottom = ctk.CTkFrame(self.side_nav_bar, fg_color='#3d539f', height=80, width= 150)
        

        self.home_btn = ctk.CTkButton(self.side_nav_bar, command=self.open_home_page, corner_radius=20,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='Home', hover_color='#3d539f',fg_color='#3d539f')
        self.downloading_btn = ctk.CTkButton(self.side_nav_bar, command=self.open_downloading_page, corner_radius=20,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='Downloading', hover_color='#3d539f',fg_color='#3d539f')
        self.downloaded_btn = ctk.CTkButton(self.side_nav_bar, command=self.open_downloaded_page, corner_radius=20,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='Downloaded', hover_color='#3d539f',fg_color='#3d539f')
        self.about_btn = ctk.CTkButton(self.btn_bottom, command=self.open_about_page, corner_radius=20,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='About', hover_color='#3d539f',fg_color='#3d539f')
        self.settings_btn = ctk.CTkButton(self.btn_bottom, command=self.open_settings_page, corner_radius=20,font=CTkFont(family="Helvetica", size=11, weight="bold"), width=120,height=30, text='Settings', hover_color='#3d539f',fg_color='#3d539f')


        self.home_btn.place(x=60, y=50)
        self.downloading_btn.place(x=60, y=100)
        self.downloaded_btn.place(x=60, y=150)
        self.about_btn.pack(pady=5)
        self.settings_btn.pack(pady=5)

        self.side_bar_icon_btns = ctk.CTkFrame(self.side_nav_bar,fg_color='#5b74d8', width=50, corner_radius=20)
        self.side_bar_icon_btns.pack_propagate(False)

        self.icon_btn_bottom = ctk.CTkFrame(self.side_bar_icon_btns, height=80,width=50, fg_color='#5b74d8')
        
        self.home_icon_btn = ctk.CTkButton(self.side_bar_icon_btns, command= self.open_home_page, width=30,height=30, text='', hover_color='#5b74d8',fg_color='#5b74d8',image=self.xe_images.homeImg)
        self.downloading_icon_btn = ctk.CTkButton(self.side_bar_icon_btns, command= self.open_downloading_page, width=30,height=30, text='', hover_color='#5b74d8',fg_color='#5b74d8',image=self.xe_images.downloadImg)
        self.downloaded_icon_btn = ctk.CTkButton(self.side_bar_icon_btns, command= self.open_downloaded_page, width=30,height=30, text='', hover_color='#5b74d8',fg_color='#5b74d8',image=self.xe_images.folderImg)
        self.about_icon_btn = ctk.CTkButton(self.icon_btn_bottom, command= self.open_about_page, width=30,height=30, text='', hover_color='#5b74d8',fg_color='#5b74d8',image=self.xe_images.aboutImg)
        self.settings_icon_btn = ctk.CTkButton(self.icon_btn_bottom, command= self.open_settings_page, width=30,height=30, text='', hover_color='#5b74d8',fg_color='#5b74d8',image=self.xe_images.settingsImg)

        self.home_icon_btn.place(x=5, y=50)
        self.downloading_icon_btn.place(x=5, y=100)
        self.downloaded_icon_btn.place(x=5, y=150)
        self.about_icon_btn.pack(pady=5)
        self.settings_icon_btn.pack(pady=5)
        self.icon_btn_bottom.pack(side='bottom', pady=20)




        self.side_bar_icon_btns.pack(side=ctk.LEFT, fill='y')
        self.btn_bottom.pack(side='bottom', pady=20)

        self.side_nav_bar.pack(fill=ctk.Y, side='left')
        self.side_nav_bar.pack_propagate(False)

        self.content_container = ctk.CTkFrame(self.app_container, fg_color='#edeef0', corner_radius=0)
        self.content_container.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        self.search_entry = ctk.CTkEntry(self.app_container, width=200, height=30, placeholder_text="Search", corner_radius=10,border_color='#3d539f', bg_color='#edeef0')


        self.search_entry.place(y=20, relx=.5, anchor='center')

        
        #DownloadingIndicatorBox(self)


        self.home_icon_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.home_btn))
        self.downloaded_icon_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.downloaded_btn))
        self.downloading_icon_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.downloading_btn))
        self.about_icon_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.about_btn))
        self.settings_icon_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.settings_btn))


        self.home_icon_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.home_btn, 0))
        self.downloading_icon_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.downloading_btn, 1))
        self.downloaded_icon_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.downloaded_btn, 2))
        self.about_icon_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.about_btn, 3))
        self.settings_icon_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.settings_btn, 4))

        self.home_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.home_btn, ))
        self.downloaded_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.downloaded_btn))
        self.downloading_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.downloading_btn))
        self.about_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.about_btn))
        self.settings_btn.bind("<Enter>", command=lambda event:self.change_btn_color(event , self.settings_btn))


        self.home_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.home_btn , 0))
        self.downloading_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.downloading_btn, 1))
        self.downloaded_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.downloaded_btn, 2))
        self.about_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.about_btn, 3))
        self.settings_btn.bind("<Leave>", command=lambda event:self.revert_btn_color(event , self.settings_btn, 4))


        self.open_home_page()



       



app = MyApp()
app.mainloop()