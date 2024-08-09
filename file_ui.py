import customtkinter as ctk
from app_utils import Colors, OtherMethods, os
import os, subprocess , platform

class File(ctk.CTkFrame):
    def resetFileStyles(self):
        self.configure(fg_color=self.colors.secondary_color)
        self.file_type.configure(fg_color=self.colors.secondary_color)
        self.download_status.configure(fg_color=self.colors.secondary_color, text_color='gray')
        self.file_size.configure(fg_color=self.colors.secondary_color, text_color='gray')
        self.file_name.configure(fg_color=self.colors.secondary_color, text_color='gray')
        self.file_download_date.configure(fg_color=self.colors.secondary_color, text_color='gray')

    def update_filename(self,new_filename):
        filename = os.path.basename(new_filename)
        self.alter_details = (filename, self.f_path, self.f_status)
        self.file_type.configure(image=self.ui_methods.return_file_type(filename))
        self.file_name.configure(text=self.return_short_filename(filename))
        
    def propagate_file_btn(self, event):

        parent = self.parent
        if parent.previously_clicked_file is None:
            parent.previously_clicked_file = None
        if parent.previously_clicked_file and parent.details_of_file_clicked:
            parent.details_of_file_clicked = None
            for widget in parent.previously_clicked_file:
                try:
                    widget.configure(fg_color=self.colors.secondary_color, text_color='gray')
                    if widget == self.file_name:
                        widget.configure(fg_color=self.colors.secondary_color, text_color=self.colors.text_color)
                except:
                    widget.configure(fg_color=self.colors.secondary_color)

        self.configure(fg_color=self.colors.utils_color)
        self.file_type.configure(fg_color=self.colors.utils_color)
        self.download_status.configure(fg_color=self.colors.utils_color, text_color=self.colors.secondary_color)
        self.file_size.configure(fg_color=self.colors.utils_color, text_color=self.colors.secondary_color)
        self.file_name.configure(fg_color=self.colors.utils_color, text_color=self.colors.secondary_color)
        self.file_download_date.configure(fg_color=self.colors.utils_color, text_color=self.colors.secondary_color)

        parent.previously_clicked_file = [
            self,
            self.file_name,
            self.file_size,
            self.file_type,
            self.file_download_date,
            self.download_status,
        ]
        parent.details_of_file_clicked = self.alter_details

        

    def update_file_info(self, status, size, date):
        self.download_status.configure(text=status)
        self.file_size.configure(text=self.ui_methods.return_filesize_in_correct_units(size))
        self.file_download_date.configure(text=date)

        if status in ('completed.', '100.0%'):
            self.download_status.configure(text_color='green')

        elif status == 'failed!':
            self.download_status.configure(text_color='red')
        else:
            self.download_status.configure(text_color= self.colors.text_color)
            

    def return_short_filename(self, filename):
        filename = filename.strip()
        name, exten = os.path.splitext(filename)
        if len(name) > 45:
            filename = f'{name[:20]}...{name[-22:]}{exten}'
        return filename

    def __init__(self, parent, filename, size, status, date, path) -> None:
        super().__init__(parent.downloading_list, fg_color=parent.colors.secondary_color,height=40,corner_radius=5, cursor='hand2')
        self.task_name = ''
        self.parent = parent
        self.colors = Colors()
        self.file_id = os.path.basename(filename)

        self.ui_methods = OtherMethods()

        self.appended_files = []

        self.f_path = path
        self.f_status = status

        

        self.alter_details = (filename, path, status)

       
        
        
        self.file_type = ctk.CTkLabel(self, text='', image=self.ui_methods.return_file_type(filename), fg_color='transparent')
        self.file_type.pack(side='left', padx=10)

        self.file_name = ctk.CTkLabel(self, text_color='gray',text=self.return_short_filename(filename), font=self.parent.font11,fg_color='transparent', anchor='w')
        self.file_name.pack(side='left', fill='x', expand=True, padx=10, pady=1)
       
        self.file_size = ctk.CTkLabel(self,text=self.ui_methods.return_filesize_in_correct_units(size),anchor='w',text_color='gray',font=self.parent.font12, fg_color='transparent', width=60)
        self.file_size.pack(side='right',  padx=5, pady=5)
        self.file_download_date = ctk.CTkLabel(self,anchor='w',text_color='gray',text=date,font=self.parent.font12, width=60,fg_color='transparent')
        self.file_download_date.pack(side='right', padx=5, pady=5)
        self.download_status = ctk.CTkLabel(self,text_color='gray',anchor='w', text=status, width=70, font=self.parent.font12)
        self.download_status.pack(side='right')


        
        self.pack_propagate(False)

        
        self.bind('<Button-1>', self.propagate_file_btn)
        self.file_type.bind('<Button-1>', self.propagate_file_btn)
        self.download_status.bind('<Button-1>', self.propagate_file_btn)
        self.file_size.bind('<Button-1>', self.propagate_file_btn)
        self.file_name.bind('<Button-1>', self.propagate_file_btn)
        self.file_download_date.bind('<Button-1>', self.propagate_file_btn)


        self.bind('<Double-1>', self.openFile)
        self.file_type.bind('<Double-1>', self.openFile)
        self.download_status.bind('<Double-1>', self.openFile)
        self.file_size.bind('<Double-1>', self.openFile)
        self.file_name.bind('<Double-1>', self.openFile)
        self.file_download_date.bind('<Double-1>', self.openFile)


    def openFile(self, event):
        f_name, path, _ = self.alter_details
        path_and_file = os.path.join(path, f_name)
            
        if not os.path.exists(path_and_file):
            pass
            
        else:
            system_name = platform.system()   
        
            if system_name == 'Windows':
                os.startfile(path_and_file)

            elif system_name == 'Linux':
                subprocess.Popen(["xdg-open", path_and_file])



