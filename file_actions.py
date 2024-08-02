from customtkinter import CTkFont
from app_utils import Colors, Images
import customtkinter as ctk
import subprocess, os, platform

class actionsForDisplayedFiles():
    

    def __init__(self, parent):
        self.parent = parent
        self.colors = Colors()
        self.font11 = CTkFont(weight='bold', family='Helvetica', size=11)
        self.font17 = CTkFont(weight='bold', family='Helvetica', size=17)
        self.font12 = CTkFont(weight='bold', family='Helvetica', size=12, slant='italic') 

        self.container = ctk.CTkFrame(parent.content_container, height=50, fg_color=self.colors.primary_color,bg_color='transparent', corner_radius=5)
        self.actions_label = ctk.CTkLabel(self.container, text=" ",  fg_color='transparent', height=20,width=70, font=self.font11, text_color=self.colors.text_color)
        self.actions_label.place(x=20, rely=.5 , anchor='w')
        self.more_actions = ctk.CTkButton(self.container, hover=False,width=30, fg_color='transparent',cursor='hand2' ,text='', image=parent.xe_images.more)
        self.more_actions.place(relx=1, rely=.5, anchor='e')
        self.actions = ctk.CTkFrame(self.container, fg_color=self.colors.primary_color, bg_color='transparent')

        self.xe_images =Images()
        self.open = ctk.CTkButton(self.actions, text='',command=lambda state='Open':self.perform_file_actions(state, self.open), image=self.xe_images.open, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.delete = ctk.CTkButton(self.actions, text='',command=lambda state='Delete':self.perform_file_actions(state, self.delete), image=self.xe_images.delete, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.pause = ctk.CTkButton(self.actions, text='',command=lambda state='Pause':self.perform_file_actions(state, self.pause), image=self.xe_images.pause, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.resume = ctk.CTkButton(self.actions, text='',command=lambda state='Resume':self.perform_file_actions(state, self.resume), image=self.xe_images.play, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        self.restart = ctk.CTkButton(self.actions, text='',command=lambda state='Restart':self.perform_file_actions(state, self.restart), image=self.xe_images.restart, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)
        #self.stop = ctk.CTkButton(self.actions, text='',command=lambda state='Stop':self.perform_file_actions(state, self.stop), image=self.xe_images.stop, width=30,hover=False, cursor='hand2',height=30, fg_color=self.colors.secondary_color)

        self.open.pack(side='left', padx=10, pady=10)
        self.delete.pack(side='left', padx=10, pady=10)
        self.pause.pack(side='left', padx=10, pady=10)
        self.resume.pack(side='left', padx=10, pady=10)
        #self.stop.pack(side='left', padx=10, pady=10)
        self.restart.pack(side='left', padx=10, pady=10)
    
        self.actions.place(rely=.5, relx=.5, anchor='center')
        self.container.pack(side='bottom', fill='x', padx=5, pady=2)
        self.container.pack_propagate(False)
        self.open.bind('<Enter>', lambda event , state='Open':self.on_actions_enter(event, state))
        self.delete.bind('<Enter>', lambda event , state='Delete':self.on_actions_enter(event, state))
        self.pause.bind('<Enter>', lambda event , state='Pause':self.on_actions_enter(event, state))
        self.resume.bind('<Enter>', lambda event , state='Resume':self.on_actions_enter(event, state))
        self.restart.bind('<Enter>', lambda event , state='Restart':self.on_actions_enter(event, state))
        #self.stop.bind('<Enter>', lambda event , state='Stop':self.on_actions_enter(event, state))

        self.more_actions.bind('<Enter>', parent.show_more)

        self.open.bind('<Leave>', lambda event:self.on_actions_leave(event, self.open))
        self.delete.bind('<Leave>', lambda event:self.on_actions_leave(event, self.delete))
        self.pause.bind('<Leave>', lambda event:self.on_actions_leave(event, self.pause))
        self.resume.bind('<Leave>', lambda event:self.on_actions_leave(event, self.resume))
        self.restart.bind('<Leave>', lambda event:self.on_actions_leave(event, self.restart))
        #self.stop.bind('<Leave>', lambda event:self.on_actions_leave(event, self.stop))

        
    def close_opened_popup_window(self, window):
        window.destroy()

    def delete_file_from_storage_temp_file_or_both(self,window):
        f_name , path, status = self.parent.details_of_file_clicked 

        file_to_delete = os.path.join(path, f_name)
        if self.check_value.get() == 1:
            try:
                self.parent.delete_details_or_make_changes(f_name)
            except Exception as e: 
                pass
            if os.path.exists(file_to_delete):
                try:
                    os.remove(file_to_delete)
                except Exception as e:
                    print(e)

        else:
            try:
                self.parent.delete_details_or_make_changes(f_name)
            except Exception as e: 
                pass

        
        window.destroy()
        
    def show_filenotfound_popup(self, parent):
        self.error_top_window = ctk.CTkToplevel(parent)
        self.error_top_window.overrideredirect(True)
        width = self.error_top_window.winfo_screenwidth()
        height = self.error_top_window.winfo_screenheight()
        half_w = int((width/2))
        half_h = int((height/2))
        self.error_top_window.geometry(f'+{half_w}+{half_h}')
        
        self.message_box = ctk.CTkFrame(self.error_top_window, height=180, width=320, fg_color=self.colors.utils_color, corner_radius=5)
        self.title_bar = ctk.CTkFrame(self.message_box, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.logo = ctk.CTkLabel(self.title_bar,text='', width=25, cursor='hand2',fg_color='transparent',  height=25, image=self.xe_images.sub_logo )
        self.logo.place(x=5, y=2.5,anchor='nw' )
        self.close = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command=lambda : self.close_opened_popup_window(self.error_top_window), width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=315, y=5,anchor='ne' )
        self.error = ctk.CTkLabel(self.message_box, anchor='w',text='File not found!', text_color=self.colors.text_color,font=self.font17)
        self.error.pack(fill='x',pady=5, padx=10)
        self.about_error = ctk.CTkLabel(self.message_box,anchor='w', text='The file has been moved,renamed or deleted', font=self.font12)
        self.about_error.pack(padx=10, fill='x')
        self.okay = ctk.CTkButton(self.message_box, text='ok', height=40,command=lambda : self.close_opened_popup_window(self.error_top_window), width=100,hover=False, corner_radius=5, fg_color=self.colors.secondary_color)
        self.okay.pack(side='bottom', pady=10)
        self.message_box.pack_propagate(False)
        self.message_box.pack()

    def show_delete_file_popup(self, parent):
        self.delete_file_top_window = ctk.CTkToplevel(parent)
        self.delete_file_top_window.overrideredirect(True)
        width = self.delete_file_top_window.winfo_screenwidth()
        height = self.delete_file_top_window.winfo_screenheight()
        half_w = int((width/2))
        half_h = int((height/2))
        self.check_value = ctk.IntVar()
        self.delete_file_top_window.geometry(f'+{half_w}+{half_h}')

        self.message_box = ctk.CTkFrame(self.delete_file_top_window, height=210, width=360, fg_color=self.colors.utils_color, corner_radius=5)
        self.title_bar = ctk.CTkFrame(self.message_box, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.logo = ctk.CTkLabel(self.title_bar,text='', width=25, cursor='hand2',fg_color='transparent',  height=25, image=self.xe_images.sub_logo )
        self.logo.place(x=5, y=2.5,anchor='nw' )
        self.close = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command= lambda :self.close_opened_popup_window(self.delete_file_top_window), width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=355, y=5,anchor='ne' )
        self.prompt = ctk.CTkLabel(self.message_box, anchor='w',text='Confirm Deletion', text_color=self.colors.text_color,font=self.font17)
        self.prompt.pack(fill='x',pady=5, padx=10)
        self.prompt_error = ctk.CTkLabel(self.message_box,anchor='w', text='Are you sure you want to delete selected downloads?', font=self.font11)
        self.prompt_error.pack(padx=20, fill='x')
        self.check_box = ctk.CTkCheckBox(self.message_box,checkbox_height=15,corner_radius=1,text_color='white',font=self.font11,offvalue=0, onvalue=1,variable=self.check_value, checkbox_width=15, hover=False, text='Delete file from disk')
        self.check_box.pack(padx=20, pady=5,fill='x')
        self.delete_actions = ctk.CTkFrame(self.message_box, fg_color='transparent')
        self.delete_actions.pack()
        self.no = ctk.CTkButton(self.delete_actions, text='NO', height=40,command= lambda :self.close_opened_popup_window(self.delete_file_top_window), width=100,hover=False, corner_radius=5, fg_color=self.colors.secondary_color)
        self.no.pack(side='left', pady=10, padx=5)
        self.yes = ctk.CTkButton(self.delete_actions, text='YES', height=40,command= lambda :self.delete_file_from_storage_temp_file_or_both(self.delete_file_top_window), width=100,hover=False, corner_radius=5, fg_color='red')
        self.yes.pack(side='left', pady=10, padx=5)
        self.message_box.pack_propagate(False)
        self.message_box.pack()




    def perform_file_actions(self, state,me):
        if self.parent.details_of_file_clicked:
            f_name , path, status = self.parent.details_of_file_clicked 


            path_and_file = os.path.join(path, f_name)


            if state == 'Open':
                if not os.path.exists(path_and_file):
                    self.show_filenotfound_popup(self.parent)
                    
                else:
                    system_name = platform.system()   
                
                    if system_name == 'Windows':
                        os.startfile(path_and_file)

                    elif system_name == 'Linux':
                        subprocess.Popen(["xdg-open", path_and_file])
            elif state == 'Delete':
                self.show_delete_file_popup(self.parent)

            elif state == 'Pause':
                self.parent.pause_downloading_file(path_and_file)

            elif state == 'Resume':
                self.parent.resume_paused_file(path_and_file)

            
            me.configure(fg_color = self.colors.utils_color)
        else:
            pass

    def on_actions_enter(self, event, state):
        self.state_color = self.colors.utils_color
        if state == 'Delete':
            self.state_color = 'red'
        elif state == 'Stop':
            self.state_color = 'orange'
        elif state == 'Resume':
            self.state_color = 'green'
        self.actions_label.configure(text=state, fg_color=self.state_color)

    def on_actions_leave(self,event, me):
        self.actions_label.configure(text='', fg_color=self.colors.primary_color)
        me.configure(fg_color=self.colors.secondary_color)

class More(ctk.CTkFrame):
    def __init__(self, parent):        

        super().__init__(parent.content_container,width=150, height=200, fg_color=parent.colors.primary_color) 
        self.colors = Colors()
        font12 = CTkFont(family="Helvetica", size=11, weight="bold") 

        self.add_link = ctk.CTkButton(self,font=font12,anchor='w', fg_color=self.colors.secondary_color, hover_color=self.colors.utils_color,corner_radius=5,   text='Add Link')
        self.clear_finished = ctk.CTkButton(self,font=font12,anchor='w', fg_color=self.colors.secondary_color, hover_color=self.colors.utils_color,corner_radius=5,   text='Clear Finished')
        self.delete_download = ctk.CTkButton(self,font=font12,anchor='w', fg_color=self.colors.secondary_color, hover_color=self.colors.utils_color,corner_radius=5,   text='Delete Download')
        self.speed_limiter = ctk.CTkButton(self,font=font12,anchor='w', fg_color=self.colors.secondary_color, hover_color=self.colors.utils_color,corner_radius=5,   text='Limit Speed')
        self.exit = ctk.CTkButton(self,font=font12,anchor='w', fg_color=self.colors.secondary_color, hover_color=self.colors.utils_color,corner_radius=5,   text='close')

         

       

        self.add_link.pack(pady=5)
        self.clear_finished.pack(pady=5)
        self.delete_download.pack(pady=5)
        self.speed_limiter.pack(pady=5)
        self.exit.pack(pady=5)
         
   