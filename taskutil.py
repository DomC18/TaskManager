from task import Task
import tkinter as tk
import globalvar
import constants
import json
import os

def add_task(name_entry:tk.Entry, description_entry:tk.Entry, deadline_entry:tk.Entry, status_entry:tk.Entry, importance_entry:tk.Entry) -> None:
    globalvar.user_tasks.append(Task(name_entry.get(), description_entry.get(), deadline_entry.get(), int(status_entry.get()), int(importance_entry.get())))

def edit_task(name_entry:tk.Entry, description_entry:tk.Entry, deadline_entry:tk.Entry, status_entry:tk.Entry, importance_entry:tk.Entry) -> None:
    globalvar.user_tasks[0].name = name_entry.get()
    globalvar.user_tasks[0].description = description_entry.get()
    globalvar.user_tasks[0].deadline = deadline_entry.get()
    globalvar.user_tasks[0].status = int(status_entry.get())
    globalvar.user_tasks[0].importance = int(importance_entry.get())

def find_task(task_name:str) -> Task:
    for task in globalvar.user_tasks:
        if task.name == task_name:
            return task
    return None

def load_tasks() -> None:
    data:dict = {}
    file_dir = rf"{constants.USERDATADIR+globalvar.name}.json"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    for idx in range(len(data["tasks"])):
        globalvar.user_tasks.append(Task(data["tasks"][idx]["name"], 
                               data["tasks"][idx]["description"], 
                               data["tasks"][idx]["deadline"], 
                               data["tasks"][idx]["status"],
                               data["tasks"][idx]["importance"]
                            ))

def save_tasks() -> None:
    data:dict = {}
    file_dir = rf"{constants.USERDATADIR+globalvar.name}.json"

    data = {
        globalvar.name: {
            "username": globalvar.username,
            "password": globalvar.password
        }
    }
    task_data = {"tasks": []}
    for task in globalvar.user_tasks:
        task_data["tasks"].append(task.return_as_dict())
    data.update(task_data)

    try:
        os.remove(file_dir)
    except FileNotFoundError:
        return
    
    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)

def sign_out(root:tk.Tk, init) -> None:
    save_tasks()
    root.destroy()
    init()

def sorted_by_name() -> list[Task]:
    globalvar.user_tasks.sort(key=lambda task : task.name)
    return globalvar.user_tasks

def sorted_by_deadline() -> list[Task]:
    globalvar.user_tasks.sort(key=lambda task : task.deadline)
    return globalvar.user_tasks

def sorted_by_status() -> list[Task]:
    globalvar.user_tasks.sort(key=lambda task : task.status)
    return globalvar.user_tasks

def sorted_by_importance() -> list[Task]:
    globalvar.user_tasks.sort(key=lambda task : task.importance)
    return globalvar.user_tasks