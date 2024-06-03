from Task import Task
import tkinter as tk

name = ""
username = ""
password = ""
curr_date = Task().date_list_to_string(Task().get_current_date())

user_tasks:list[Task] = []
filtered_tasks:list[Task] = []

cal = None
add_button:tk.Button
add_label:tk.Label
up_button:tk.Button
down_button:tk.Button