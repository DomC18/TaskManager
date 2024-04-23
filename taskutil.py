from Task import Task
import tkinter as tk
import globalvar
import constants
import time
import json
import os

def should_back(task_name:str, month:tk.StringVar, day:tk.StringVar, year:tk.StringVar) -> bool:
    task = globalvar.user_tasks.index(find_task(task_name))
    if month.get() == "" and (globalvar.user_tasks[task].deadline[0:2] == "00"):
        return False
    if day.get() == "" and (globalvar.user_tasks[task].deadline[3:5] == "00"):
        return False
    if year.get() == "" and (globalvar.user_tasks[task].deadline[6:10] == "0000"):
        return False
    return True

def edit_task(task_name:str, name_entry:tk.Entry, description_entry:tk.Entry, month:tk.StringVar, day:tk.StringVar, year:tk.StringVar, status:tk.StringVar, importance:tk.StringVar) -> bool:
    task = globalvar.user_tasks.index(find_task(task_name))
    new_date = ""
    if name_entry.get() != "":
        globalvar.user_tasks[task].name = name_entry.get()
    if description_entry.get() != "":
        globalvar.user_tasks[task].description = description_entry.get()
    if status.get() != "":
        globalvar.user_tasks[task].status = status.get()
    if importance.get() != "":
        globalvar.user_tasks[task].importance = importance.get()

    if month.get() != "":
        new_date = month.get()[-2:]
        if day.get() != "":
            new_date += "/"
            new_date += day.get()
            if year.get() != "":
                new_date += "/"
                new_date += year.get()
                globalvar.user_tasks[task].deadline = new_date
                return True
            else:
                return False
        else:
            return False
    elif (globalvar.user_tasks[task].deadline[0:2] != "00") and (globalvar.user_tasks[task].deadline[3:5] != "00") and (globalvar.user_tasks[task].deadline[6:10] != "0000"):
        return True
    else:
        return False
        
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

def sign_out(root:tk.Tk, init_func) -> None:
    save_tasks()
    root.destroy()
    init_func()

def name_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.name)

def deadline_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.get_date_differential())

def status_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.get_status_sort())

def importance_sort() -> None:
    globalvar.user_tasks.sort(key=lambda task : task.get_importance_sort())

def get_valid_years() -> list:
    valid_years = []
    current_year_raw = time.localtime()[0]
    for i in range(10):
        valid_years.append(str(current_year_raw+i))
    return valid_years