from listbox import Listbox
from loginutil import verify_existing
import tkinter as tk
import globalvar
import constants
import taskutil

task_list : Listbox
root : tk.Tk

def init() -> None:
    global root

    globalvar.user_tasks = []

    root = tk.Tk()
    root.config(bg="grey")
    root.title("Login")
    root.geometry("600x400+480+270")
    root.resizable(False, False)

    logo_label = tk.Label(root, text="TaskManager Login", font=("Arial", 40), bg="#f0f0f0", justify="center")
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    firstname_label = tk.Label(root, text="*First Name:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    firstname_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    firstname_entry = tk.Entry(root, font=("Arial", 25), justify="left")
    firstname_entry.grid(row=1, column=1, padx=10, pady=5)

    username_label = tk.Label(root, text="*Username:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    username_entry = tk.Entry(root, font=("Arial", 25), justify="left")
    username_entry.grid(row=2, column=1, padx=10, pady=5)

    password_label = tk.Label(root, text="*Password:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    password_entry = tk.Entry(root, show="*", font=("Arial", 25), justify="left")
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.Button(root, text="Login/Register", font=("Arial", 25), bg="#4CAF50", fg="white", width=15, justify="center", command=lambda r=root, f=firstname_entry, u=username_entry, p=password_entry, fl=firstname_label, ul=username_label, pl=password_label, func=init_task_interface : verify_existing(r,f,u,p,fl,ul,pl,func))
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    root.mainloop()


def init_task_interface() -> None:
    global task_list
    global root

    root = tk.Tk()
    root.config(bg="white")
    root.title("TaskManager")
    root.geometry("960x540+333+135")
    root.resizable(False, False)

    util_frame = tk.Frame(root, bg="white")
    util_frame.place(relx=0, rely=0, anchor="nw")
    profile_frame = tk.Frame(root, bg="white")
    profile_frame.place(relx=1, rely=0, anchor="ne")
    task_frame = tk.Frame(root)
    task_frame.place(relx=0.5, rely=1, anchor="s")

    task_list = Listbox(task_frame, root, 550, 450, "grey")
    task_list.list_index = 0
    for idx, task in enumerate(globalvar.user_tasks):
        if idx < task_list.list_index:
            continue
        if idx > task_list.list_index + 6:
            break
        task_list.insert(idx-task_list.list_index, task)
    task_list.pack()

    save_icon = tk.PhotoImage(file=constants.SAVEFILE)
    save_button = tk.Button(util_frame, image=save_icon, bd=0, bg="white", command=taskutil.save_tasks)
    save_button.grid(row=0, column=0)
    save_label = tk.Label(util_frame, text="Save", justify="center", font=("Times New Roman", 30), bg="white", fg="black")
    save_label.grid(row=0,column=1)
    filter_icon = tk.PhotoImage(file=constants.FILTERFILE)
    filter_button = tk.Button(util_frame, image=filter_icon, bd=0, bg="white")
    filter_button.configure(command=task_list.filter_interface)
    filter_button.grid(row=1, column=0)
    filter_label = tk.Label(util_frame, text="Filter", justify="center", font=("Times New Roman", 30), bg="white", fg="black")
    filter_label.grid(row=1, column=1)

    profile_label = tk.Label(profile_frame, text="Log Out", justify="center", font=("Times New Roman", 30), bg="white", fg="black")
    profile_label.grid(row=0, column=0)
    profile_icon = tk.PhotoImage(file=constants.PROFILEFILE)
    profile_button = tk.Button(profile_frame, image=profile_icon, bd=0, bg="white", command=lambda r=root, i=init : taskutil.sign_out(r, i))
    profile_button.grid(row=0, column=1)

    up_button = tk.Button(root, bd=0, text="↑", bg="white", fg="black", font=("Times New Roman", 30, "bold"))
    up_button.configure(command=task_list.move_up)
    up_button.place(relx=0.7875, rely=0.1675, anchor="nw")
    down_button = tk.Button(root, bd=0, text="↓", bg="white", fg="black", font=("Times New Roman", 30, "bold"))
    down_button.configure(command=task_list.move_down)
    down_button.place(relx=0.7875, rely=0.9875, anchor="sw")

    add_icon = tk.PhotoImage(file=constants.ADDFILE)
    add_button = tk.Button(root, image=add_icon, bg="white", bd=0)
    add_button.configure(command=task_list.add_task)
    add_button.place(relx=0.1, rely=0.5, anchor="center")
    add_label = tk.Label(root, text="Add Task", justify="center", font=("Times New Roman", 30), bg="white", fg="black")
    add_label.place(relx=0.1, rely=0.6, anchor="center")
    
    root.mainloop()