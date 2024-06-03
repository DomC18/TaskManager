from cal import Calendar
from listbox import Listbox
from loginutil import verify_existing
import tkinter as tk
import globalvar
import constants
import taskutil

calendar : Calendar
task_list : Listbox
root : tk.Tk

def init() -> None:
    global root

    globalvar.user_tasks = []

    root = tk.Tk()
    root.config(bg="red")
    root.title("Login")
    root.geometry("900x500+510+290")
    root.resizable(False, False)

    logo_label = tk.Label(root, text="TaskManager Login", font=("Arial", 60), bg="red", justify="center")
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    firstname_label = tk.Label(root, text="*First Name:", font=("Arial", 38), bg="red", justify="center")
    firstname_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    firstname_entry = tk.Entry(root, font=("Arial", 38), justify="left")
    firstname_entry.grid(row=1, column=1, padx=10, pady=5)

    username_label = tk.Label(root, text="*Username:", font=("Arial", 38), bg="red", justify="center")
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    username_entry = tk.Entry(root, font=("Arial", 38), justify="left")
    username_entry.grid(row=2, column=1, padx=10, pady=5)

    password_label = tk.Label(root, text="*Password:", font=("Arial", 38), bg="red", justify="center")
    password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    password_entry = tk.Entry(root, show="*", font=("Arial", 38), justify="left")
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.Button(root, text="Login/Register", font=("Arial", 38), bg="#4CAF50", fg="black", width=15, justify="center", command=lambda r=root, f=firstname_entry, u=username_entry, p=password_entry, fl=firstname_label, ul=username_label, pl=password_label, func=init_task_interface : verify_existing(r,f,u,p,fl,ul,pl,func))
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    def exit(event:tk.Event) -> None:
        root.destroy()

    root.bind("<Escape>", exit)
    root.mainloop()


def init_task_interface() -> None:
    global task_list, root, calendar

    root = tk.Tk()
    root.config(bg="light blue")
    root.title("TaskManager")
    root.geometry("1440x810+240+135")
    root.resizable(True, True)

    util_frame = tk.Frame(root, bg="light blue")
    util_frame.place(relx=0, rely=0, anchor="nw")
    search_frame = tk.Frame(root, bg="light blue")
    search_frame.place(relx=0.5, rely=0.0875, anchor="center")
    profile_frame = tk.Frame(root, bg="light blue")
    profile_frame.place(relx=1, rely=0, anchor="ne")
    task_frame = tk.Frame(root)
    task_frame.place(relx=0.5, rely=1, anchor="s")

    task_list = Listbox(task_frame, root, 826, 676, "grey")
    task_list.list_index = 0
    globalvar.filtered_tasks = globalvar.user_tasks
    for idx, task in enumerate(globalvar.filtered_tasks):
        if idx < task_list.list_index:
            continue
        if idx > task_list.list_index + 6:
            break
        task_list.insert(idx-task_list.list_index, task)
    task_list.pack()

    search_entry = tk.Entry(search_frame, bd=0, bg="#ffabab", fg="black", font=("Times New Roman", 35, "bold"), width=20)
    search_entry.grid(row=0, column=0, padx=10)
    search_icon = tk.PhotoImage(file=constants.SEARCHFILE)
    search_button = tk.Button(search_frame, image=search_icon, bd=0, bg="light blue", command=lambda e=search_entry, f=task_list.filter_insert : taskutil.search_tasks(e,f))
    search_button.grid(row=0, column=1)

    save_icon = tk.PhotoImage(file=constants.SAVEFILE)
    save_button = tk.Button(util_frame, image=save_icon, bd=0, bg="light blue", command=taskutil.save_tasks)
    save_button.grid(row=0, column=0)
    save_label = tk.Label(util_frame, text="Save", justify="center", font=("Times New Roman", 40), bg="light blue", fg="black")
    save_label.grid(row=0,column=1)
    filter_icon = tk.PhotoImage(file=constants.FILTERFILE)
    filter_button = tk.Button(util_frame, image=filter_icon, bd=0, bg="light blue")
    filter_button.configure(command=task_list.filter_interface)
    filter_button.grid(row=1, column=0)
    filter_label = tk.Label(util_frame, text="Filter", justify="center", font=("Times New Roman", 40), bg="light blue", fg="black")
    filter_label.grid(row=1, column=1)

    profile_label = tk.Label(profile_frame, text="Log Out", justify="center", font=("Times New Roman", 46), bg="light blue", fg="black")
    profile_label.grid(row=0, column=0)
    profile_icon = tk.PhotoImage(file=constants.PROFILEFILE)
    profile_button = tk.Button(profile_frame, image=profile_icon, bd=0, bg="light blue", command=lambda r=root, i=init : taskutil.sign_out(r, i))
    profile_button.grid(row=0, column=1)

    up_button = tk.Button(root, bd=0, text="↑", bg="light blue", fg="black", font=("Times New Roman", 46, "bold"))
    up_button.configure(command=task_list.move_up)
    up_button.place(relx=0.7875, rely=0.1675, anchor="nw")
    down_button = tk.Button(root, bd=0, text="↓", bg="light blue", fg="black", font=("Times New Roman", 46, "bold"))
    down_button.configure(command=task_list.move_down)
    down_button.place(relx=0.7875, rely=0.9875, anchor="sw")

    add_icon = tk.PhotoImage(file=constants.ADDFILE)
    add_button = tk.Button(root, image=add_icon, bg="light blue", bd=0)
    add_button.configure(command=task_list.add_task)
    add_button.place(relx=0.1, rely=0.5, anchor="center")
    add_label = tk.Label(root, text="Add Task", justify="center", font=("Times New Roman", 46), bg="light blue", fg="black")
    add_label.place(relx=0.1, rely=0.6, anchor="center")
    
    globalvar.add_button = add_button
    globalvar.add_label = add_label
    globalvar.up_button = up_button
    globalvar.down_button = down_button
    calendar = Calendar(root, 1440, 810, "light blue")
    calendar_icon = tk.PhotoImage(file=constants.CALENDARFILE)
    calendar_button = tk.Button(util_frame, image=calendar_icon, bd=0, bg="light blue")
    calendar_button.configure(command=lambda a=add_button, al=add_label, u=up_button, d=down_button : calendar.toggle_show(a,al,u,d))
    calendar_button.grid(row=2, column=0)
    calendar_label = tk.Label(util_frame, text="Calendar", justify="center", font=("Times New Roman", 40), bg="light blue", fg="black")
    calendar_label.grid(row=2, column=1)

    globalvar.cal = calendar

    def exit(event:tk.Event) -> None:
        root.destroy()

    root.bind("<Escape>", exit)
    root.mainloop()