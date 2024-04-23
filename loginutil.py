import tkinter as tk
import constants
import globalvar
import json
import taskutil

def verify_existing(root:tk.Tk, first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, first_label:tk.Label, user_label:tk.Label, password_label:tk.Label, task_func) -> None:
    data:dict = {}
    name = first_entry.get()

    name_invalid = first_entry.get() == ""
    username_invalid = user_entry.get() == ""
    password_invalid = password_entry.get() == ""

    if (name_invalid or username_invalid or password_invalid):
        if name_invalid:
            first_label.configure(fg="red")
        else: 
            first_label.configure(fg="black")

        if username_invalid:
            user_label.configure(fg="red")
        else: 
            user_label.configure(fg="black")

        if password_invalid:
            password_label.configure(fg="red")
        else: 
            password_label.configure(fg="black")
    
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
        root.destroy()
        taskutil.load_tasks()
        task_func()

def register_new(root:tk.Tk, first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, first_label:tk.Label, user_label:tk.Label, password_label:tk.Label, task_func) -> None:
    data:dict = {}
    name = first_entry.get()
    username = user_entry.get()
    password = password_entry.get()

    name_invalid = name == ""
    username_invalid = username == ""
    password_invalid = password == ""

    if (name_invalid or username_invalid or password_invalid):
        if name_invalid:
            first_label.configure(fg="red")
        else: 
            first_label.configure(fg="black")

        if username_invalid:
            user_label.configure(fg="red")
        else: 
            user_label.configure(fg="black")

        if password_invalid:
            password_label.configure(fg="red")
        else: 
            password_label.configure(fg="black")

        return
    
    file_dir = constants.USERDATADIR + name + ".json"

    try:
        open(file_dir, "r")
        return True
    except FileNotFoundError:
        pass

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