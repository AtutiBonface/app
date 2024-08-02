import customtkinter as ctk
from app_utils import Colors, Images
import webbrowser
from customtkinter import CTkFont


class About(ctk.CTkFrame):
    def open_link_in_browser(self, event):
        webbrowser.open_new(r'https://blackjuice.imaginekenya.site')
    def __init__(self, parent):
        super().__init__(parent) 
        self.colors = Colors()
        self.title_font = CTkFont(weight='bold', size=16, family='Helvetica')
        self.other_font = CTkFont(weight='normal', size=12, family='Helvetica')
        self.link_font = CTkFont(weight='bold', size=13,underline=True, family='Helvetica')
        self.configure(fg_color=self.colors.secondary_color) 
        self.xe_images = Images()
         
        self.outer_container = ctk.CTkFrame(self, fg_color='transparent', width=300, height=450)

        self.logo_label = ctk.CTkLabel(self.outer_container, text='', image=self.xe_images.huge_logo)
        self.logo_label.pack()
        self.app_name = ctk.CTkLabel(self.outer_container,text_color='gray',font=self.title_font, text='BlackJuice Download Manager v1.5.1')
        self.app_name.pack()
        self.app_domain = ctk.CTkLabel(self.outer_container,font=self.link_font,cursor='hand2', text_color=self.colors.utils_color, text='https://blackjuice.imaginekenya.site')
        self.app_domain.pack()
        self.created_by = ctk.CTkLabel(self.outer_container,text_color='gray', font=self.other_font,text='Created by Atuti Bonface')
        self.created_by.pack()
        self.app_copywrite = ctk.CTkLabel(self.outer_container,font=self.other_font, text_color='gray', text=f'{chr(169)} 2024 Xengine, AtutiBonface')
        self.app_copywrite.pack(pady=10)
        self.outer_container.place(relx=.5, rely=.5, anchor='center')

        self.app_domain.bind('<Button-1>', self.open_link_in_browser)
        