from Task import Task
import tkinter as tk
import globalvar
import constants
import json
import os

def edit_task(task_name:str, name_entry:tk.Entry, description_entry:tk.Entry, deadline_entry:tk.Entry, status:tk.StringVar, importance:tk.StringVar) -> None:
    task = globalvar.user_tasks.index(find_task(task_name))
    if name_entry.get() != "":
        globalvar.user_tasks[task].name = name_entry.get()
    if description_entry.get() != "":
        globalvar.user_tasks[task].description = description_entry.get()
    if deadline_entry.get() != "":
        globalvar.user_tasks[task].deadline = deadline_entry.get()
    if status.get() != "":
        globalvar.user_tasks[task].status = status.get()
    if importance.get() != "":
        globalvar.user_tasks[task].importance = importance.get()

def amount_task(task_name:str) -> int:
    task_num = 0
    for task in globalvar.user_tasks:
        if task.name == task_name:
            task_num += 1
    return task_num

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

def name_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.name)

def deadline_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.deadline)

def status_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.get_status_sort())

def importance_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.get_importance_sort())
