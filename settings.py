import customtkinter as ctk
from customtkinter import CTkFont
from app_utils import Colors, ConfigFilesHandler
import clipboard,os
from customtkinter import filedialog
from pathlib import Path



class Settings(ctk.CTkFrame):
    def return_setting_value(self, setting):
        path_to_config = ConfigFilesHandler().path_to_config_file

        if os.path.exists(path_to_config):        
            with open(path_to_config, 'r') as f:
                for line in f.readlines():
                    if line.startswith(setting):
                        new_line = str(line.split('<x:e>')[1].strip())

                        return new_line
        else:
            ConfigFilesHandler()
            with open(path_to_config, 'r') as f:
                for line in f.readlines():
                    if line.startswith(setting):
                        new_line = str(line.split('<x:e>')[1].strip())

                        return new_line

    def change_settings_state(self, setting, value):
        lines = []
        path_to_config = ConfigFilesHandler().path_to_config_file

        if os.path.exists(path_to_config):
            with open(path_to_config, 'r') as file:
                lines = file.readlines()

            with open(path_to_config, 'w') as f:
                for line in lines:
                    if line.startswith(setting):
                        f.write(f'{setting} <x:e> {value}\n')
                    else:
                        f.write(line)
        else:
            ConfigFilesHandler()
            with open(path_to_config, 'r') as file:
                lines = file.readlines()

            with open(path_to_config, 'w') as f:
                for line in lines:
                    if line.startswith(setting):
                        f.write(f'{setting} <x:e> {value}\n')
                    else:
                        f.write(line)

                
    def onOptionSelection(self, event):
          
        value = self.max_value_selected.get() 
        self.change_settings_state('max_concurrent_downloads', value)
        
    def changePathFn(self):
        home = Path().home()
        path = filedialog.askdirectory(initialdir=home, mustexist=True, title='Select default folder')
        if path:
            self.change_settings_state('defaut_download_path', path)
            self.access_download_path.set(path)
            self.xengine_download_path_global = path
        else:
            pass
        
    def __init__(self, parent):
        super().__init__(parent) 
        self.colors = Colors()
        self.proges_w = ctk.StringVar()
        self.download_c_w = ctk.StringVar()
        self.auto_resume_downl = ctk.StringVar()
        self.overide_fi_exis = ctk.StringVar()
        self.max_value_selected = ctk.StringVar()
        self.access_download_path = ctk.StringVar()

        self.VERSION = f'{self.return_setting_value('VERSION')}'
        
        self.max_value_selected.set(f'{self.return_setting_value('max_concurrent_downloads')}')
        self.overide_fi_exis.set(f'{self.return_setting_value('overide_file')}')
        self.auto_resume_downl.set(f'{self.return_setting_value('auto_resume_download')}')
        self.download_c_w.set(f'{self.return_setting_value('show_download_complete_window')}')
        self.proges_w.set(f'{self.return_setting_value('show_progress_window')}')
        self.access_download_path.set(f'{self.return_setting_value('defaut_download_path')}')

        self.xengine_download_path_global = f'{self.return_setting_value('defaut_download_path')}'
        

        
        
        self.configure(fg_color='transparent')  
        self.font14_bold = CTkFont(family='Helvetica', weight='bold', size=14)
        self.font11_bold = CTkFont(family='Helvetica', weight='normal', size=11, slant='italic')
        self.font11_bold2 = CTkFont(family='Helvetica', weight='bold', size=11)
        self.font15_bold  = CTkFont(family='Helvetica', weight='bold', size=16)

        self.version_label = ctk.CTkLabel(self, text=self.VERSION, text_color=self.colors.primary_color, font=self.font15_bold)
        self.version_label.place(relx=.8, rely=.94, anchor='nw')
        self.general_s = ctk.CTkFrame(self, fg_color='transparent', width=500)
        self.title = ctk.CTkLabel(self.general_s, text='General Settings',text_color=self.colors.text_color, anchor='w' ,font=self.font14_bold)
        self.title.pack(padx=20,pady=10, fill='x')
        # path to where files are downloaded to 
        self.defaut_download_box = ctk.CTkFrame(self.general_s,fg_color='transparent')
        self.defaut_download_title = ctk.CTkLabel(self.defaut_download_box,text='Default download path',anchor='w', text_color=self.colors.text_color, font=self.font11_bold)
        self.defaut_download_title.pack(pady=5,fill='x', side='top')
        self.path_entry = ctk.CTkEntry(self.defaut_download_box,font=self.font11_bold2,border_width=0,width=300,textvariable=self.access_download_path, corner_radius=5, height=30, state='disabled')
        self.path_entry.pack(fill='x',side='left')
        self.change_path_btn = ctk.CTkButton(self.defaut_download_box,command=self.changePathFn, text='change',cursor='hand2',font=self.font11_bold2,hover=False, width=50, height=32, fg_color=self.colors.utils_color, corner_radius=5)
        self.change_path_btn.pack(side='left', padx=5)
        self.defaut_download_box.pack(fill='x', padx=15)
        ##
        ## others eg max-downloads 
        self.other_s = ctk.CTkFrame(self.general_s, fg_color='transparent')
        #max downloads
        self.select_max_simult_download_t = ctk.CTkLabel(self.other_s,height=40, text='Maximum concurrent downloads',anchor='w', text_color=self.colors.text_color, font=self.font11_bold)
        self.select_max_simult_download_t.pack(fill='x',)
        self.values = ["1", "3", "5", "10", "20", "100"]
        
        self.option_box = ctk.CTkOptionMenu(self.other_s,button_color=self.colors.utils_color, width=70,corner_radius=5,dropdown_text_color=self.colors.text_color,dropdown_hover_color=self.colors.utils_color, height=30, dropdown_fg_color=self.colors.secondary_color,command=self.onOptionSelection ,fg_color=self.colors.primary_color, values=self.values, variable=self.max_value_selected)
        self.option_box.place(relx=.6, y=20, anchor='w')

        #other settings on auto-resume-download , overide file, show windows for process, and download complete
        # auto-resume override-file progress-window , complete-window
        self.resume_downloading = ctk.CTkSwitch(self.other_s, command=lambda setting ='auto_resume_download':self.change_settings_state(setting,self.auto_resume_downl.get()),onvalue='true', offvalue='false', variable=self.auto_resume_downl ,fg_color=self.colors.text_color, progress_color=self.colors.utils_color, text='Auto Resume downloading',text_color=self.colors.text_color, font=self.font11_bold)
        self.resume_downloading.pack(fill='x', pady=5)
        self.overide_file = ctk.CTkSwitch(self.other_s, command=lambda setting ='overide_file':self.change_settings_state(setting, self.overide_fi_exis.get()),onvalue='true', offvalue='false', variable=self.overide_fi_exis, fg_color=self.colors.text_color, progress_color=self.colors.utils_color, text='Overide existing file',text_color=self.colors.text_color, font=self.font11_bold)
        self.overide_file.pack(fill='x', pady=5)
        
        self.progress_window = ctk.CTkSwitch(self.other_s, command=lambda setting ='show_progress_window':self.change_settings_state(setting, self.proges_w.get()),onvalue='true', offvalue='false', variable=self.proges_w, fg_color=self.colors.text_color, progress_color=self.colors.utils_color, text='Show download progress window',text_color=self.colors.text_color, font=self.font11_bold)
        self.progress_window.pack(fill='x', pady=5)
        self.download_complete = ctk.CTkSwitch(self.other_s, command=lambda setting ='show_download_complete_window':self.change_settings_state(setting, self.download_c_w.get()),onvalue='true', offvalue='false', variable=self.download_c_w,fg_color=self.colors.text_color, progress_color=self.colors.utils_color, text='Show download complete dialog',text_color=self.colors.text_color, font=self.font11_bold)
        self.download_complete.pack(fill='x', pady=5)
        ##
        self.other_s.pack(fill='x',padx=15, pady=10)
        ## browser and extensions settings
        subtitle_text = 'To allow Xengine to take over downloads and'
        subtitle_text2 = 'capture streaming videos on your browser, install browser extension'
        subtitle_text3 = 'from  link below'
        self.extensions_link = f"{self.return_setting_value('extensions_link')}"
        self.browser_monitor_s = ctk.CTkFrame(self.general_s, fg_color='transparent')
        self.browser_title = ctk.CTkLabel(self.browser_monitor_s,height=15,text='Browser monitoring',text_color=self.colors.text_color, anchor='w' ,font=self.font14_bold)
        self.browser_title.pack(padx=20,pady=10, fill='x')
        self.browser_subtitle = ctk.CTkLabel(self.browser_monitor_s,height=15,text=subtitle_text,text_color=self.colors.text_color, anchor='w' ,font=self.font11_bold)
        self.browser_subtitle.pack(fill='x', padx=20)
        self.browser_subtitle2 = ctk.CTkLabel(self.browser_monitor_s,height=15,text=subtitle_text2,text_color=self.colors.text_color, anchor='w' ,font=self.font11_bold)
        self.browser_subtitle2.pack(fill='x', padx=20)
        self.browser_subtitle3 = ctk.CTkLabel(self.browser_monitor_s,height=15,text=subtitle_text3,text_color=self.colors.text_color, anchor='w' ,font=self.font11_bold)
        self.browser_subtitle3.pack(fill='x', padx=20)
        self.link = ctk.CTkLabel(self.browser_monitor_s,fg_color=self.colors.primary_color ,text=self.extensions_link,text_color=self.colors.text_color ,font=self.font11_bold2)
        self.link.pack(fill='x', padx=20, pady=10)
        ##
        #button to copy extensions link to the system clipboard
        self.copy_link = ctk.CTkButton(self.browser_monitor_s,hover=False,command=lambda :self.copy_to_clipboard(self.extensions_link), font=self.font11_bold2,text='copy link', width=70, corner_radius=5, fg_color=self.colors.utils_color)
        self.copy_link.pack(side='left', pady=10, padx=15)
        self.browser_monitor_s.pack(fill='x')
        
        self.general_s.pack(side='left', fill='both')

        self.copy_link.bind('<Leave>', lambda event : self.return_btn_to_default(event,self.copy_link))
        self.change_path_btn.bind('<Leave>', lambda event : self.return_btn_to_default(event,self.change_path_btn))
       
        self.general_s.pack_propagate(False)

        ## call function onComboSelection when value is selected in the Combobox
        
        

    def copy_to_clipboard(self, link):
        self.copy_link.configure(fg_color=self.colors.primary_color, text='copied')
        
        ## pasting extension link to system clipboard
        clipboard.copy(link)
        # returns text of button to default after 2 seconds from copied to copy link
        self.after(2000, self.return_btn_text)

    def return_btn_text(self):
        self.copy_link.configure(text='copy link')

    #reverting the color of button once mouse leaves the button
    def return_btn_to_default(self,event, btn):
        btn.configure(fg_color=self.colors.utils_color)   
        
        