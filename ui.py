from PIL import Image
from cal import Calendar
from listbox import Listbox
from loginutil import verify_existing
import customtkinter as tk
import globalvar
import constants
import taskutil

calendar : Calendar
task_list : Listbox
root : tk.CTk

def init() -> None:
    global root

    globalvar.user_tasks = []

    root = tk.CTk()
    root.config(bg="grey")
    root.title("Login")
    root.geometry("600x400+480+270")
    root.resizable(False, False)

    logo_label = tk.CTkLabel(root, text="TaskManager Login", font=("Arial", 40), bg_color="#f0f0f0")
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    firstname_label = tk.CTkLabel(root, text="*First Name:", font=("Arial", 25), bg_color="#f0f0f0")
    firstname_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    firstname_entry = tk.CTkEntry(root, font=("Arial", 25))
    firstname_entry.grid(row=1, column=1, padx=10, pady=5)

    username_label = tk.CTkLabel(root, text="*Username:", font=("Arial", 25), bg_color="#f0f0f0")
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    username_entry = tk.CTkEntry(root, font=("Arial", 25))
    username_entry.grid(row=2, column=1, padx=10, pady=5)

    password_label = tk.CTkLabel(root, text="*Password:", font=("Arial", 25), bg_color="#f0f0f0")
    password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    password_entry = tk.CTkEntry(root, show="*", font=("Arial", 25))
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.CTkButton(root, text="Login/Register", font=("Arial", 25), bg_color="#4CAF50", fg_color="white", width=15, command=lambda r=root, f=firstname_entry, u=username_entry, p=password_entry, fl=firstname_label, ul=username_label, pl=password_label, func=init_task_interface : verify_existing(r,f,u,p,fl,ul,pl,func))
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    root.mainloop()


def init_task_interface() -> None:
    global task_list, root, calendar

    root = tk.CTk()
    root.config(bg="white")
    root.title("TaskManager")
    root.geometry("960x540+333+135")
    root.resizable(False, False)

    util_frame = tk.CTkFrame(root, bg_color="white")
    util_frame.place(relx=0, rely=0, anchor="nw")
    profile_frame = tk.CTkFrame(root, bg_color="white")
    profile_frame.place(relx=1, rely=0, anchor="ne")
    task_frame = tk.CTkFrame(root)
    task_frame.place(relx=0.5, rely=1, anchor="s")

    task_list = Listbox(task_frame, root, 550, 450)
    task_list.list_index = 0
    for idx, task in enumerate(globalvar.user_tasks):
        if idx < task_list.list_index:
            continue
        if idx > task_list.list_index + 6:
            break
        task_list.insert(idx-task_list.list_index, task)
    task_list.pack()

    save_icon = tk.CTkImage(light_image=Image.open(constants.SAVEFILE), dark_image=Image.open(constants.SAVEFILE))
    save_button = tk.CTkButton(util_frame, image=save_icon, border_width=0, bg_color="white", command=taskutil.save_tasks)
    save_button.grid(row=0, column=0)
    save_label = tk.CTkLabel(util_frame, text="Save", font=("Times New Roman", 30), bg_color="white", fg_color="black")
    save_label.grid(row=0,column=1)
    filter_icon = tk.CTkImage(light_image=Image.open(constants.FILTERFILE), dark_image=Image.open(constants.FILTERFILE))
    filter_button = tk.CTkButton(util_frame, image=filter_icon, border_width=0, bg_color="white")
    filter_button.configure(command=task_list.filter_interface)
    filter_button.grid(row=1, column=0)
    filter_label = tk.CTkLabel(util_frame, text="Filter", font=("Times New Roman", 30), bg_color="white", fg_color="black")
    filter_label.grid(row=1, column=1)

    profile_label = tk.CTkLabel(profile_frame, text="Log Out", font=("Times New Roman", 30), bg_color="white", fg_color="black")
    profile_label.grid(row=0, column=0)
    profile_icon = tk.CTkImage(light_image=Image.open(constants.PROFILEFILE), dark_image=Image.open(constants.PROFILEFILE))
    profile_button = tk.CTkButton(profile_frame, image=profile_icon, border_width=0, bg_color="white", command=lambda r=root, i=init : taskutil.sign_out(r, i))
    profile_button.grid(row=0, column=1)

    up_button = tk.CTkButton(root, border_width=0, text="↑", bg_color="white", fg_color="black", font=("Times New Roman", 30, "bold"))
    up_button.configure(command=task_list.move_up)
    up_button.place(relx=0.7875, rely=0.1675, anchor="nw")
    down_button = tk.CTkButton(root, border_width=0, text="↓", bg_color="white", fg_color="black", font=("Times New Roman", 30, "bold"))
    down_button.configure(command=task_list.move_down)
    down_button.place(relx=0.7875, rely=0.9875, anchor="sw")

    add_icon = tk.CTkImage(light_image=Image.open(constants.ADDFILE), dark_image=Image.open(constants.ADDFILE))
    add_button = tk.CTkButton(root, image=add_icon, bg_color="white", border_width=0)
    add_button.configure(command=task_list.add_task)
    add_button.place(relx=0.1, rely=0.5, anchor="center")
    add_label = tk.CTkLabel(root, text="Add Task", font=("Times New Roman", 30), bg_color="white", fg_color="black")
    add_label.place(relx=0.1, rely=0.6, anchor="center")
    
    globalvar.add_button = add_button
    globalvar.add_label = add_label
    globalvar.up_button = up_button
    globalvar.down_button = down_button
    calendar = Calendar(root, 960, 540, "white")
    calendar_icon = tk.CTkImage(light_image=Image.open(constants.CALENDARFILE), dark_image=Image.open(constants.CALENDARFILE))
    calendar_button = tk.CTkButton(util_frame, image=calendar_icon, border_width=0, bg_color="white")
    calendar_button.configure(command=lambda a=add_button, al=add_label, u=up_button, d=down_button : calendar.toggle_show(a,al,u,d))
    calendar_button.grid(row=2, column=0)
    calendar_label = tk.CTkLabel(util_frame, text="Calendar", font=("Times New Roman", 30), bg_color="white", fg_color="black")
    calendar_label.grid(row=2, column=1)

    globalvar.cal = calendar

    root.mainloop()