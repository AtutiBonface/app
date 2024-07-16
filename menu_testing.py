import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter Custom Menu Example")
        self.geometry("400x300")

        self.menu_open = False

        # Create a button to open the custom menu
        self.more_button = tk.Button(self, text="More", command=self.toggle_menu)
        self.more_button.place(x=150, y=50)  # Position the button where you want

        # Create the custom menu frame (initially hidden)
        self.custom_menu = tk.Frame(self, width=200, height=100, bg="white")
        self.custom_menu.pack_propagate(False)

        # Add some example menu items
        menu_item1 = tk.Button(self.custom_menu, text="Option 1", command=self.option1)
        menu_item1.pack(fill="both", expand=True, pady=2)

        menu_item2 = tk.Button(self.custom_menu, text="Option 2", command=self.option2)
        menu_item2.pack(fill="both", expand=True, pady=2)

        # Bind events
        self.bind("<Button-1>", self.on_click_outside)

    def toggle_menu(self):
        if self.menu_open:
            self.close_menu()
        else:
            self.open_menu()

    def open_menu(self):
        x = self.more_button.winfo_rootx()
        y = self.more_button.winfo_rooty() - self.custom_menu.winfo_height()
        self.custom_menu.place(x=x, y=y)
        self.menu_open = True

    def close_menu(self):
        self.custom_menu.place_forget()
        self.menu_open = False

    def on_click_outside(self, event):
        if self.menu_open and event.widget != self.more_button and event.widget != self.custom_menu:
            self.close_menu()

    def option1(self):
        print("Option 1 selected")

    def option2(self):
        print("Option 2 selected")

if __name__ == "__main__":
    app = App()
    app.mainloop()
