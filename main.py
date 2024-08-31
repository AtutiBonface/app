import customtkinter as ctk
from main_application import MainApplication
if __name__ == "__main__":
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')
    app = MainApplication()
    app.protocol("WM_DELETE_WINDOW", app.withdraw_window)
    app.mainloop()