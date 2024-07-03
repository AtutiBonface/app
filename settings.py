import customtkinter as ctk
from customtkinter import CTkFont
from app_utils import Colors


class Settings(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent) 
        self.colors = Colors()
        self.configure(fg_color='transparent')  
        self.font14_bold = CTkFont(family='Helvetica', weight='bold', size=14)
        self.font11_bold = CTkFont(family='Helvetica', weight='bold', size=11, slant='italic')

        self.general_s = ctk.CTkFrame(self, fg_color='transparent')
        self.title = ctk.CTkLabel(self.general_s, text='General Settings',text_color=self.colors.text_color, anchor='w' ,font=self.font14_bold)
        self.title.pack(padx=20,pady=15, fill='x')

        self.defaut_download_box = ctk.CTkFrame(self.general_s,fg_color='transparent')
        self.defaut_download_title = ctk.CTkLabel(self.defaut_download_box,text='Default download folder',anchor='w', text_color=self.colors.text_color, font=self.font11_bold)
        self.defaut_download_title.pack(pady=5,fill='x', side='top')
        self.path_entry = ctk.CTkEntry(self.defaut_download_box,border_width=0,width=200, corner_radius=5, height=30, state='disabled')
        self.path_entry.pack(fill='x',side='left', expand=True)
        self.change_path_btn = ctk.CTkButton(self.defaut_download_box, text='change',cursor='hand2',hover=False, width=50, height=30, fg_color=self.colors.utils_color, corner_radius=5)
        self.change_path_btn.pack(side='left', padx=5)
        self.defaut_download_box.pack()

        ## others eg max-downloads 
        self.other_s = ctk.CTkFrame(self.general_s, fg_color='red')
        #max downloads
        self.select_max_simult_download_t = ctk.CTkLabel(self.other_s,height=40, text='Maximum concurrent downloads',anchor='w', text_color=self.colors.text_color, font=self.font11_bold)
        self.select_max_simult_download_t.pack(fill='x',)
        self.values = ["1", "3", "5", "10", "20"]
        self.max_value_selected = ctk.StringVar()
        self.max_value_selected.set("20")
        self.option_box = ctk.CTkComboBox(self.other_s,border_width=0,button_color=self.colors.utils_color, width=70,corner_radius=5,dropdown_text_color=self.colors.text_color,dropdown_hover_color=self.colors.utils_color, height=30, dropdown_fg_color=self.colors.secondary_color, values=self.values, variable=self.max_value_selected)
        self.option_box.place(relx=.7, y=20, anchor='w')
        #overide existing file
        self.overide_file_t = ctk.CTkLabel(self.other_s, text='Overide existing file',anchor='e', text_color=self.colors.text_color, font=self.font11_bold)
        self.overide_file_t.pack(fill='x')
        self.other_s.pack(fill='x',padx=15, pady=10)
        self.other_s.pack_propagate(False)

        self.browser_monitor_s = ctk.CTkFrame(self, fg_color='red')
        self.general_s.pack(side='left',expand=True, fill='both')
        self.browser_monitor_s.pack_propagate(False)
        self.general_s.pack_propagate(False)
        self.browser_monitor_s.pack(side='left',expand=True, fill='both')
        
        