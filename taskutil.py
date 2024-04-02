from task import Task
import tkinter as tk
import globalvar
import constants
import json
import os

user_tasks:list[Task] = []

def add_task(name_entry:tk.Entry, description_entry:tk.Entry, deadline_entry:tk.Entry, status_entry:tk.Entry, importance_entry:tk.Entry) -> None:
    user_tasks.append(Task(name_entry.get(), description_entry.get(), deadline_entry.get(), int(status_entry.get()), int(importance_entry.get())))

def edit_task(name_entry:tk.Entry, description_entry:tk.Entry, deadline_entry:tk.Entry, status_entry:tk.Entry, importance_entry:tk.Entry) -> None:
    user_tasks[0].name = name_entry.get()
    user_tasks[0].description = description_entry.get()
    user_tasks[0].deadline = deadline_entry.get()
    user_tasks[0].status = int(status_entry.get())
    user_tasks[0].importance = int(importance_entry.get())

def delete_task(task_name:str) -> None:
    user_tasks.remove(task_name)

def load_tasks() -> list[Task]:
    data:dict = {}
    file_dir = rf"{constants.USERDATADIR+globalvar.name}.json"

    try:
        with open(file_dir, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return
    
    for idx in range(len(data["tasks"])):
        user_tasks.append(Task(data["tasks"][idx]["name"], 
                               data["tasks"][idx]["description"], 
                               data["tasks"][idx]["deadline"], 
                               data["tasks"][idx]["status"],
                               data["tasks"][idx]["importance"]
                            ))

    return user_tasks

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
    for task in user_tasks:
        task_data["tasks"].append(task.return_as_dict())
    data.update(task_data)

    os.remove(file_dir)
    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)


def sorted_by_name() -> list[Task]:
    user_tasks.sort(key=lambda task : task.name)
    return user_tasks

def sorted_by_deadline() -> list[Task]:
    user_tasks.sort(key=lambda task : task.deadline)
    return user_tasks

def sorted_by_status() -> list[Task]:
    user_tasks.sort(key=lambda task : task.status)
    return user_tasks

def sorted_by_importance() -> list[Task]:
    user_tasks.sort(key=lambda task : task.importance)
    return user_tasks