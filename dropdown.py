import customtkinter as ctk
from app_utils import Colors
from customtkinter import CTkFont

root = ctk.CTk()
root.geometry('400x250')

colors = Colors()
font14 = CTkFont(weight='bold', family='Helvetica', size=14)
font12 = CTkFont(weight='normal', family='Helvetica', size=12) 
font11 = CTkFont(weight='normal', family='Helvetica', size=11, slant='italic') 

dropdown = ctk.CTkFrame(root, width=150, height=200, fg_color=colors.primary_color)
add_link = ctk.CTkButton(dropdown,font=font12,anchor='w', fg_color=colors.secondary_color, hover_color=colors.utils_color,corner_radius=5,   text='Add Link')
clear_finished = ctk.CTkButton(dropdown,font=font12,anchor='w', fg_color=colors.secondary_color, hover_color=colors.utils_color,corner_radius=5,   text='Clear Finished')
delete_download = ctk.CTkButton(dropdown,font=font12,anchor='w', fg_color=colors.secondary_color, hover_color=colors.utils_color,corner_radius=5,   text='Delete Download')
speed_limiter = ctk.CTkButton(dropdown,font=font12,anchor='w', fg_color=colors.secondary_color, hover_color=colors.utils_color,corner_radius=5,   text='Limit Speed')
exit = ctk.CTkButton(dropdown,font=font12,anchor='w', fg_color=colors.secondary_color, hover_color=colors.utils_color,corner_radius=5,   text='Exit')


add_link.pack(pady=5)
clear_finished.pack(pady=5)
delete_download.pack(pady=5)
speed_limiter.pack(pady=5)
exit.pack(pady=5)
dropdown.pack()
dropdown.pack_propagate(False)

root.mainloop()