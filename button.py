import customtkinter as ctk

class ExampleApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")

        # Frame to hold the buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Create a button with a frame inside it
        self.create_button_with_frame("Button 1")
        self.create_button_with_frame("Button 2")

    def create_button_with_frame(self, text):
        # Create a button
        button = ctk.CTkButton(self.button_frame, text=text, width=300, height=100, command=lambda: self.on_button_click(text))
        button.pack(pady=10)

        # Create a frame inside the button
        inner_frame = ctk.CTkFrame(button, fg_color="lightblue", width=280, height=80)
        inner_frame.place(x=10, y=10)

        # Add some content to the frame to demonstrate
        label = ctk.CTkLabel(inner_frame, text="Frame inside button")
        label.pack(padx=10, pady=10)

        # Bind click event to the inner frame to propagate it to the button
        inner_frame.bind("<Button-1>", lambda event: self.propagate_click(event, button))
        label.bind("<Button-1>", lambda event: self.propagate_click(event, button))


        

    def propagate_click(self, event, button):
        button.invoke()
        
    def on_button_click(self, text):
        print(f"{text} clicked")

if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
