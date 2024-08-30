import sys
import threading
import pystray
from PIL import Image
import customtkinter as ctk
from app_utils import Images

class MainApplication(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("My CustomTkinter App")
        self.geometry("300x200")

        # Create a button in the main window
        self.button = ctk.CTkButton(self, text="Hello, CustomTkinter!", command=self.button_click)
        self.button.pack(pady=20)

        # Initialize the system tray icon
        self.icon = None
        self.setup_tray_icon()

    def button_click(self):
        print("Button clicked!")

    def create_image(self):
        image = Images()
        return image.logo

    def setup_tray_icon(self):
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Exit", self.exit_app)
        )
        self.icon = pystray.Icon("app_name", image, "My CustomTkinter App", menu)
        self.icon.run_detached()

    def show_window(self, icon, item):
        self.after(0, self._show_window)

    def _show_window(self):
        self.deiconify()
        self.lift()
        self.focus_force()
        self.update()

    def exit_app(self, icon, item):
        icon.stop()
        self.quit()

    def run(self):
        self.protocol("WM_DELETE_WINDOW", self.withdraw_window)
        self.mainloop()

    def withdraw_window(self):
        self.withdraw()
        if sys.platform.startswith('linux'):
            self.icon.update_menu()

if __name__ == "__main__":
    ctk.set_appearance_mode('System')
    ctk.set_default_color_theme('blue')
    app = MainApplication()
    app.run()