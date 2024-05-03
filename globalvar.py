from Task import Task
import customtkinter as tk

name = ""
username = ""
password = ""
curr_date = Task().date_list_to_string(Task().get_current_date())

user_tasks = []

cal = None
add_button:tk.CTkButton
add_label:tk.CTkLabel
up_button:tk.CTkButton
down_button:tk.CTkButton