import customtkinter as ctk
from tkinter import filedialog
from app_utils import Colors, Images
from customtkinter import CTkFont

class FileAddedWidget(ctk.CTkFrame):
    def __init__(self, master, file_name, file_url, file_size, **kwargs):
        super().__init__(master, height=50, corner_radius=5 ,fg_color="#1b1c1e",**kwargs)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.images = Images()
        self.colors = Colors()

        self.font12 = CTkFont(weight='normal', family='Helvetica', size=12) 
        self.font11 = CTkFont(weight='normal', family='Helvetica', size=11, slant='italic') 

        

        self.checkbox_var = ctk.BooleanVar()
        self.checkbox = ctk.CTkCheckBox(self, text="", width=15,checkbox_width=16,checkbox_height=16, fg_color=self.colors.utils_color,corner_radius=2, variable=self.checkbox_var)
        self.checkbox.grid(row=0, column=0, padx=(10, 0), pady=10)
        self.checkbox.grid_remove()  # Hide checkbox by default

        file_info = ctk.CTkFrame(self, fg_color="transparent", height=40)
        file_info.grid(row=0, column=1, sticky="nsew", padx=10)
        file_info.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(file_info, text=file_name,font=self.font12,text_color='white', anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(file_info, text=file_url,font=self.font11, anchor="w", text_color="gray").grid(row=1, column=0, sticky="w")
        
        ctk.CTkLabel(self, text=file_size, font=self.font12,text_color="white").grid(row=0, column=2, padx=10)

    def toggle_checkbox(self, show):
        if show:
            self.checkbox.grid()
        else:
            self.checkbox.grid_remove()

class MultipleFilePickerWindow(ctk.CTkToplevel):
    def self_close(self):        
        self.destroy()

    def start_drag(self, event):
        self.x_offset = event.x
        self.y_offset = event.y

    def do_drag(self, event):
        x = self.winfo_pointerx() - self.x_offset
        y = self.winfo_pointery() - self.y_offset
        self.geometry(f"+{x}+{y}")

    def __init__(self,master):
        super().__init__(master, fg_color='#232428')
       
        self.geometry("600x470")
        self.update_idletasks()
        master_x = master.winfo_rootx()
        master_y = master.winfo_rooty()
        master_width = master.winfo_width()
        master_height = master.winfo_height()
        
        window_x = master_x + (master_width // 2) - (600 // 2)
        window_y = master_y + (master_height // 2) - (470 // 2)


        
        self.geometry(f'600x470+{window_x}+{master_y}')
        
        self.update()
        self.update_idletasks()

        self.xe_images = Images()
        self.colors = Colors()
        self.configure(fg_color=self.colors.utils_color)
        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.buttons_font = CTkFont(family="Helvetica", size=11, weight="bold")
       

        
        self.title_bar = ctk.CTkFrame(self, height=30, fg_color=self.colors.text_color, corner_radius=1)
        self.title_bar.pack(fill='x')
        self.close = ctk.CTkButton(self.title_bar,text='',corner_radius=2,command=self.self_close, width=20,hover=False, cursor='hand2',fg_color=self.colors.secondary_color,  height=20, image=self.xe_images.close_image )
        self.close.place(x=595, y=5,anchor='ne' )
        self.title_bar.bind("<ButtonPress-1>", self.start_drag)
        self.title_bar.bind("<B1-Motion>", self.do_drag)


        self.files = [
            {"name": "Example Video 1.mp4", "url": "https://example.com/video1.mp4", "size": "250 MB"},
            {"name": "Cool Music.mp3", "url": "https://example.com/music.mp3", "size": "10 MB"},
            {"name": "Important Document.pdf", "url": "https://example.com/document.pdf", "size": "5 MB"},
            {"name": "Funny Meme.jpg", "url": "https://example.com/meme.jpg", "size": "1 MB"},
            {"name": "Tutorial Video.mp4", "url": "https://example.com/tutorial.mp4", "size": "500 MB"},
            {"name": "Important Document.pdf", "url": "https://example.com/document.pdf", "size": "5 MB"},
            {"name": "Funny Meme.jpg", "url": "https://example.com/meme.jpg", "size": "1 MB"},
            {"name": "Tutorial Video.mp4", "url": "https://example.com/tutorial.mp4", "size": "500 MB"},
            {"name": "Important Document.pdf", "url": "https://example.com/document.pdf", "size": "5 MB"},
            {"name": "Funny Meme.jpg", "url": "https://example.com/meme.jpg", "size": "1 MB"},
            {"name": "Tutorial Video.mp4", "url": "https://example.com/tutorial.mp4", "size": "500 MB"},
        ]

        self.selection_mode = False

        self.create_widgets()

    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self, fg_color=self.colors.secondary_color)
        self.main_frame.pack(expand=True, fill="both", padx=5)
        self.top_actions = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.select_button = ctk.CTkButton(self.top_actions, text="Select Files",hover=False,corner_radius=5,font=self.buttons_font, width=120,height=30, command=self.toggle_selection_mode, fg_color=self.colors.utils_color, text_color="black")
        self.select_button.pack(side="right", padx=5)
        self.top_actions.pack(fill="x",pady=5)
        

        # Files list frame with scrollbar
        self.files_frame = ctk.CTkScrollableFrame(self.main_frame, corner_radius=5, fg_color=self.colors.secondary_color)
        self.files_frame.pack(expand=True, side='top', fill="both", padx=10, pady=(0, 10))

        # Populate files

        self.file_widgets = []
        for file in self.files:
            fw = FileAddedWidget(self.files_frame, file["name"], file["url"], file["size"])
            fw.pack(fill="x", pady=5)
            self.file_widgets.append(fw)

        # Button frame
        button_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        button_frame.pack(fill="x", padx=10, pady=10)

        # Buttons
        ctk.CTkButton(button_frame, text="Add File", command=self.add_file, hover=False,cursor='hand2',fg_color=self.colors.utils_color,corner_radius=5, font=self.buttons_font, text_color="black").pack(side="left", padx=5)
        
        self.remove_button = ctk.CTkButton(button_frame, text="Remove Selected", command=self.remove_selected, hover=False,cursor='hand2',fg_color=self.colors.utils_color,corner_radius=5, font=self.buttons_font, text_color="black")
        self.remove_button.pack(side="left", padx=5)
        self.remove_button.pack_forget()  # Hide initially
        self.download_button = ctk.CTkButton(button_frame, text="Download All", command=self.download_all, hover=False,cursor='hand2',fg_color=self.colors.utils_color,corner_radius=5, font=self.buttons_font, text_color="black")
        self.download_button.pack(side="left", padx=5)

    def add_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            new_file = {"name": file_path.split("/")[-1], "url": "file://" + file_path, "size": "Unknown"}
            self.files.append(new_file)
            fw = FileAddedWidget(self.files_frame, new_file["name"], new_file["url"], new_file["size"])
            fw.pack(fill="x", pady=5)
            self.file_widgets.append(fw)
            if self.selection_mode:
                fw.toggle_checkbox(True)

    def toggle_selection_mode(self):
        self.selection_mode = not self.selection_mode
        for widget in self.file_widgets:
            widget.toggle_checkbox(self.selection_mode)
        
        if self.selection_mode:
            self.select_button.configure(text="Cancel Selection")
            self.remove_button.pack(side="left", padx=5)
            self.download_button.configure(text="Download Selected")
        else:
            self.select_button.configure(text="Select Files")
            self.remove_button.pack_forget()
            self.download_button.configure(text="Download All")

    def remove_selected(self):
        for widget in self.file_widgets[:]:
            if widget.checkbox_var.get():
                widget.destroy()
                self.file_widgets.remove(widget)
        self.files = [file for file, widget in zip(self.files, self.file_widgets) if not widget.checkbox_var.get()]

    def download_all(self):
        if self.selection_mode:
            selected_files = [file for file, widget in zip(self.files, self.file_widgets) if widget.checkbox_var.get()]
            print("Downloading selected files:", selected_files)
        else:
            print("Downloading all files:", self.files)

    

