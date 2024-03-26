import tkinter as tk

def init_login_interface() -> None:
    root = tk.Tk()
    root.config(bg="blue")

    widget = tk.Label(root, text="hello")
    widget.place(relx=0.5, rely=0.5)

    root.mainloop()

def init_task_interface() -> None:
    root = tk.Tk()
    root.config(bg="red")

    root.mainloop()