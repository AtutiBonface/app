import tkinter as tk

def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.attributes('-topmost', True)  # Ensure this window is always on top
    new_window.title('Always On Top Window')
    # Add widgets and configure your new window here

root = tk.Tk()

button = tk.Button(root, text='Open Window', command=open_new_window)
button.pack(pady=20)

root.mainloop()
