import tkinter as tk
import globalvar
import constants
import taskutil
import json

def verify_existing(first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, root:tk.Tk) -> None:
    data:dict = {}

    name = first_entry.get()
    file_dir = constants.USERDATADIR + name + ".json"
    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
        
    username = data[name]["username"]
    password = data[name]["password"]

    globalvar.name = name
    globalvar.username = username
    globalvar.password = password

    if username == user_entry.get() and password == password_entry.get():
        print("Login Successful")
        root.destroy()
        init_task_interface()


def register_new(first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, root:tk.Tk) -> None:
    data:dict = {}
    name = first_entry.get()
    username = user_entry.get()
    password = password_entry.get()
    if (name == "" or username == "" or password == ""):
        return
    
    file_dir = constants.USERDATADIR + name + ".json"

    try:
        open(file_dir, "r")
        return True
    except FileNotFoundError:
        print("Creating new account...")

    data = {
        name: {
            "username": username,
            "password": password
        }
    }

    globalvar.name = name
    globalvar.username = username
    globalvar.password = password

    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)

    print("Account created successfully.")
    root.destroy()
    init_task_interface()





def init() -> None:
    root = tk.Tk()
    root.config(bg="grey")
    root.geometry("560x480+480+270")
    root.resizable(False, False)

    logo_label = tk.Label(root, text="TaskManager Login", font=("Arial", 40), bg="#f0f0f0", justify="center")
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    firstname_label = tk.Label(root, text="First Name:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    firstname_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    firstname_entry = tk.Entry(root, font=("Arial", 25), justify="left")
    firstname_entry.grid(row=1, column=1, padx=10, pady=5)

    username_label = tk.Label(root, text="Username:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    username_entry = tk.Entry(root, font=("Arial", 25), justify="left")
    username_entry.grid(row=2, column=1, padx=10, pady=5)

    password_label = tk.Label(root, text="Password:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    password_entry = tk.Entry(root, show="*", font=("Arial", 25), justify="left")
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.Button(root, text="Login", font=("Arial", 25), bg="#4CAF50", fg="white", width=15, justify="center", command=lambda f=firstname_entry, u=username_entry, p=password_entry, r=root : verify_existing(f,u,p,r))
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    register_label = tk.Button(root, text="Don't have an account? Register here.", font=("Arial", 20), bg="#f0f0f0", justify="center", command=lambda f=firstname_entry, u=username_entry, p=password_entry, r=root : register_new(f,u,p,r))
    register_label.grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()

def init_task_interface() -> None:
    root = tk.Tk()
    root.config(bg="grey")
    root.geometry("960x540+333+135")
    root.resizable(False, False)

    
    
    root.mainloop()