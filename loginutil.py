import customtkinter as tk
import constants
import globalvar
import json
import taskutil

def verify_existing(root:tk.CTk, first_entry:tk.CTkEntry, user_entry:tk.CTkEntry, password_entry:tk.CTkEntry, first_label:tk.CTkLabel, user_label:tk.CTkLabel, password_label:tk.CTkLabel, task_func) -> None:
    data:dict = {}
    name = first_entry.get()

    name_invalid = first_entry.get() == ""
    username_invalid = user_entry.get() == ""
    password_invalid = password_entry.get() == ""

    if (name_invalid or username_invalid or password_invalid):
        if name_invalid:
            first_label.configure(fg_color="red")
        else: 
            first_label.configure(fg_color="black")

        if username_invalid:
            user_label.configure(fg_color="red")
        else: 
            user_label.configure(fg_color="black")

        if password_invalid:
            password_label.configure(fg_color="red")
        else: 
            password_label.configure(fg_color="black")
    
    file_dir = constants.USERDATADIR + name + ".json"
    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        register_new(root, first_entry, user_entry, password_entry, task_func)
        return
        
    username = data[name]["username"]
    password = data[name]["password"]

    globalvar.name = name
    globalvar.username = username
    globalvar.password = password

    if username == user_entry.get() and password == password_entry.get():
        root.destroy()
        taskutil.load_tasks()
        task_func()

def register_new(root:tk.CTk, first_entry:tk.CTkEntry, user_entry:tk.CTkEntry, password_entry:tk.CTkEntry, task_func) -> None:
    name = first_entry.get()

    if name == "":
        return

    username = user_entry.get()
    password = password_entry.get()

    file_dir = constants.USERDATADIR + name + ".json"

    user_data = {
        name: {
            "username": username,
            "password": password
        },
        "tasks": [
            
        ]
    }

    globalvar.name = name
    globalvar.username = username
    globalvar.password = password

    with open(file_dir, "w") as file:
        json.dump(user_data, file, indent=4)

    root.destroy()
    task_func()