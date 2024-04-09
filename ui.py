from PIL import ImageTk, ImageFilter, Image, ImageGrab
from Task import Task
import pygame as pyg
import tkinter as tk
import globalvar
import constants
import taskutil
import json

def verify_existing(first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, root:tk.Tk) -> None:
    data:dict = {}

    name = first_entry.get()
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
        print("Login Successful")
        root.destroy()
        taskutil.load_tasks()
        init_task_interface()


def register_new(first_entry:tk.Entry, user_entry:tk.Entry, password_entry:tk.Entry, root:tk.Tk) -> None:
    data:dict = {}
    name = first_entry.get()
    username = user_entry.get()
    password = password_entry.get()
    if (name == "" or username == "" or password == ""):
        return
    
    file_dir = constants.USERDATADIR + name + ".json"

    try:
        open(file_dir, "r")
        return True
    except FileNotFoundError:
        print("Creating new account...")

    data = {
        name: {
            "username": username,
            "password": password
        }
    }

    globalvar.name = name
    globalvar.username = username
    globalvar.password = password

    with open(file_dir, "w") as file:
        json.dump(data, file, indent=4)

    print("Account created successfully.")
    root.destroy()
    init_task_interface()




class CustomListbox(tk.Frame):
    def __init__(self, master=None, width=0, height=0, **kwargs) -> None:
        global root

        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.list_frame = tk.Frame(self.canvas)
        self.bg_color = self.rgb_to_hex((240, 240, 240))

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_index:int

        self.edit_large_icon = tk.PhotoImage(file=constants.EDITLARGEFILE)
        self.edit_icon = tk.PhotoImage(file=constants.EDITFILE)
        self.delete_icon = tk.PhotoImage(file=constants.DELETEFILE)
        self.filter_large_icon = tk.PhotoImage(file=constants.FILTERLARGEFILE)
        self.info_icon = tk.PhotoImage(file=constants.INFOFILE)

        self.button_images : dict = {}
        self.task_combos : dict = {}

        self.name_option = tk.Button()
        self.desc_option = tk.Button()
        self.deadline_option = tk.Button()
        self.status_option = tk.Button()
        self.importance_option = tk.Button()
        self.exit_option = tk.Button()

        self.curr_task_name:str
        self.x:int
        self.y:int
        self.w:int
        self.h:int
        self.blurred_screenshot:Image
        self.screenshot:Image
        self.screenshot_photo:ImageTk.PhotoImage
        self.screenshot_label:tk.Label
        self.edit_large:tk.Button
        self.back_button:tk.Button

        self.filter_name:tk.Button
        self.filter_dead:tk.Button
        self.filter_status:tk.Button
        self.filter_importance:tk.Button

        self.old_name:tk.Label
        self.old_desc:tk.Label
        self.old_dead:tk.Label
        self.old_status:tk.Label
        self.old_importance:tk.Label
        self.name_entry:tk.Entry
        self.desc_entry:tk.Entry
        self.dead_entry:tk.Entry
        self.status_entry:tk.OptionMenu
        self.status_var = tk.StringVar()
        self.importance_entry:tk.OptionMenu
        self.importance_var = tk.StringVar()

    def rgb_to_hex(self, rgb) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def insert(self, idx:int, task:taskutil.Task) -> None:
        y_multiplier = 0.01 + (idx*0.13)
        y_multiplier2 = 0.075 + (idx*0.13)
        
        name_label = tk.Label(self.canvas, text=task.name[:13], font=('Helvetica', 33))
        name_label.place(relx=0, rely=y_multiplier, anchor="nw")
        
        edit_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({edit_button:self.edit_icon})
        edit_button.configure(command=lambda n=task.name : self.edit_task_interface(n))
        edit_button.configure(image=self.button_images[edit_button])
        edit_button.place(relx=0.875, rely=y_multiplier, anchor="ne")
        
        delete_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({delete_button:self.delete_icon})
        delete_button.configure(command=lambda b=delete_button : self.delete(b))
        delete_button.configure(image=self.button_images[delete_button])
        delete_button.place(relx=0.975, rely=y_multiplier, anchor="ne")

        status_indicator = tk.Label(self.canvas, bg=self.rgb_to_hex(task.get_status_color()), text=task.get_status_short(), font=("Times New Roman", 40, "bold"), fg=task.get_status_font())
        status_indicator.place(relx=0.575, rely=y_multiplier2, anchor="center")
        importance_indicator = tk.Label(self.canvas, bg=self.rgb_to_hex(task.get_importance_color()), text=task.get_importance_short(), font=("Times New Roman", 40, "bold"), fg=task.get_importance_font())
        importance_indicator.place(relx=0.7, rely=y_multiplier2, anchor="center")
        
        self.task_combos.update({task.name:[task.name, name_label, edit_button, delete_button, status_indicator, importance_indicator]})
    
    def move_down(self) -> None:
        if self.list_index+8 > len(globalvar.user_tasks):
            return

        self.list_index += 1
        task_names = self.task_combos.keys()

        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
        task_list.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < task_list.list_index:
                continue
            if idx > task_list.list_index + 6:
                break
            task_list.insert(idx-self.list_index, task)
        task_list.pack()

    def move_up(self) -> None:
        if self.list_index <= 0:
            return
        
        self.list_index -= 1
        task_names = self.task_combos.keys()

        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
        task_list.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < task_list.list_index:
                continue
            if idx > task_list.list_index + 6:
                break
            task_list.insert(idx-self.list_index, task)
        task_list.pack()

    def add_task(self) -> None:
        globalvar.user_tasks.insert(0, Task())

        self.list_index = 0
        task_names = self.task_combos.keys()
        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
        task_list.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < task_list.list_index:
                continue
            if idx > task_list.list_index + 6:
                break
            task_list.insert(idx-self.list_index, task)
        task_list.pack()

    def filter_interface(self) -> None:
        global root

        self.x = root.winfo_rootx()
        self.y = root.winfo_rooty()
        self.w = root.winfo_width()
        self.h = root.winfo_height()
        self.screenshot = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.w, self.y+self.h))
        self.screenshot_photo = ImageTk.PhotoImage(self.screenshot)
        self.screenshot_label = tk.Label(root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = ImageTk.PhotoImage(self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.Button(root, bg="white", fg="black", text="←", font=("Helvetica", 50, "bold"), relief="flat")
        self.back_button.configure(command=self.back_from_filter)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.filter_large = tk.Label(root, image=self.filter_large_icon, bd=0, bg=self.bg_color)
        self.filter_large.place(relx=0.125, rely=0.5, anchor="center")

        self.filter_name = tk.Button(root, text="Filter by Name", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
        self.filter_dead = tk.Button(root, text="Filter by Deadline", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
        self.filter_status = tk.Button(root, text="Filter by Status", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
        self.filter_importance = tk.Button(root, text="Filter by Importance", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
        self.filter_name.configure(command=self.name_sort)
        self.filter_dead.configure(command=self.dead_sort)
        self.filter_status.configure(command=self.status_sort)
        self.filter_importance.configure(command=self.importance_sort)
        self.filter_name.place(relx=0.5, rely=1/5, anchor="center")
        self.filter_dead.place(relx=0.5, rely=2/5, anchor="center")
        self.filter_status.place(relx=0.5, rely=3/5, anchor="center")
        self.filter_importance.place(relx=0.5, rely=4/5, anchor="center")

    def name_sort(self) -> None:
        taskutil.name_sort()
        self.back_from_filter()
    
    def dead_sort(self) -> None:
        taskutil.deadline_sort()
        self.back_from_filter()
    
    def status_sort(self) -> None:
        taskutil.status_sort()
        self.back_from_filter()
    
    def importance_sort(self) -> None:
        taskutil.importance_sort()
        self.back_from_filter()

    def back_from_filter(self) -> None:
        self.back_button.destroy()
        self.screenshot_label.destroy()
        self.filter_large.destroy()
        self.filter_name.destroy()
        self.filter_dead.destroy()
        self.filter_status.destroy()
        self.filter_importance.destroy()

        task_names = self.task_combos.keys()

        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
        task_list.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < task_list.list_index:
                continue
            if idx > task_list.list_index + 6:
                break
            task_list.insert(idx-self.list_index, task)
        task_list.pack()

    def edit_task_interface(self, name) -> None:
        global root

        self.curr_task_name = name

        self.x = root.winfo_rootx()
        self.y = root.winfo_rooty()
        self.w = root.winfo_width()
        self.h = root.winfo_height()
        self.screenshot = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.w, self.y+self.h))
        self.screenshot_photo = ImageTk.PhotoImage(self.screenshot)
        self.screenshot_label = tk.Label(root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = ImageTk.PhotoImage(self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.Button(root, bg="white", fg="black", text="←", font=("Helvetica", 50, "bold"), relief="flat")
        self.back_button.configure(command=self.back_from_edit)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.old_name = tk.Label(root, text=name, bg="grey", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_name.place(relx=0.25, rely=1/6, anchor="w")
        self.old_desc = tk.Label(root, text=taskutil.find_task(name).description, bg="grey", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_desc.place(relx=0.25, rely=2/6, anchor="w")
        self.old_dead = tk.Label(root, text=taskutil.find_task(name).deadline, bg="grey", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_dead.place(relx=0.25, rely=3/6, anchor="w")
        self.old_status = tk.Label(root, text=taskutil.find_task(name).status, bg="grey", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_status.place(relx=0.25, rely=4/6, anchor="w")
        self.old_importance = tk.Label(root, text=taskutil.find_task(name).importance, bg="grey", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_importance.place(relx=0.25, rely=5/6, anchor="w")
        self.name_entry = tk.Entry(root, bg="grey", fg="white", font=("Times New Roman", 40, "bold"), width=10)
        self.name_entry.place(relx=0.95, rely=1/6, anchor="e")
        self.desc_entry = tk.Entry(root, bg="grey", fg="white", font=("Times New Roman", 40, "bold"), width=10)
        self.desc_entry.place(relx=0.95, rely=2/6, anchor="e")
        self.dead_entry = tk.Entry(root, bg="grey", fg="white", font=("Times New Roman", 40, "bold"), width=10)
        self.dead_entry.place(relx=0.95, rely=3/6, anchor="e")
        self.status_entry = tk.OptionMenu(root, self.status_var, "Not Started", "Delayed", "Underway", "Almost Completed", "Finished")
        self.status_entry.place(relx=0.95, rely=4/6, anchor="e")
        self.importance_entry = tk.OptionMenu(root, self.importance_var, "Minimal", "Trivial", "Average", "Significant", "Critical")
        self.importance_entry.place(relx=0.95, rely=5/6, anchor="e")

        self.edit_large = tk.Button(root, image=self.edit_large_icon, bd=0, bg=self.bg_color)
        self.edit_large.configure(command=lambda n=self.curr_task_name, ne=self.name_entry, dese=self.desc_entry, dede=self.dead_entry, se=self.status_var, ie=self.importance_var: self.edit_task(n, ne, dese, dede, se, ie))
        self.edit_large.place(relx=0.125, rely=0.5, anchor="center")
    
    def edit_task(self, name:str, name_entry:tk.Entry, desc_entry:tk.Entry, dead_entry:tk.Entry, status_entry:tk.Entry, importance_entry:tk.Entry) -> None:
        taskutil.edit_task(name, name_entry, desc_entry, dead_entry, status_entry, importance_entry)
        self.back_from_edit()

        task_names = self.task_combos.keys()

        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
        task_list.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < task_list.list_index:
                continue
            if idx > task_list.list_index + 6:
                break
            task_list.insert(idx-self.list_index, task)
        task_list.pack()

    def back_from_edit(self) -> None:
        self.back_button.destroy()
        self.screenshot_label.destroy()
        self.edit_large.destroy()
        self.old_name.destroy()
        self.old_desc.destroy()
        self.old_dead.destroy()
        self.old_status.destroy()
        self.old_importance.destroy()
        self.name_entry.destroy()
        self.desc_entry.destroy()
        self.dead_entry.destroy()
        self.status_entry.destroy()
        self.importance_entry.destroy()

    def delete(self, delete_button:tk.Button) -> None:
        global task_list

        task_names = self.task_combos.keys()
        task_combos = self.task_combos.values()
        
        for combo in task_combos:
            if combo[3] == delete_button:
                name = combo[0]
        
        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
                
        self.task_combos.pop(self.task_combos[name][0])
        globalvar.user_tasks.pop(globalvar.user_tasks.index(taskutil.find_task(name)))
        
        task_list.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < task_list.list_index:
                continue
            if idx > task_list.list_index + 6:
                break
            task_list.insert(idx-self.list_index, task)
        task_list.pack()
    

def init() -> None:
    global root

    root = tk.Tk()
    root.config(bg="grey")
    root.geometry("560x480+480+270")
    root.resizable(False, False)

    logo_label = tk.Label(root, text="TaskManager Login", font=("Arial", 40), bg="#f0f0f0", justify="center")
    logo_label.grid(row=0, column=0, columnspan=2, pady=20)

    firstname_label = tk.Label(root, text="First Name:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    firstname_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

    firstname_entry = tk.Entry(root, font=("Arial", 25), justify="left")
    firstname_entry.grid(row=1, column=1, padx=10, pady=5)

    username_label = tk.Label(root, text="Username:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    username_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

    username_entry = tk.Entry(root, font=("Arial", 25), justify="left")
    username_entry.grid(row=2, column=1, padx=10, pady=5)

    password_label = tk.Label(root, text="Password:", font=("Arial", 25), bg="#f0f0f0", justify="center")
    password_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

    password_entry = tk.Entry(root, show="*", font=("Arial", 25), justify="left")
    password_entry.grid(row=3, column=1, padx=10, pady=5)

    login_button = tk.Button(root, text="Login", font=("Arial", 25), bg="#4CAF50", fg="white", width=15, justify="center", command=lambda f=firstname_entry, u=username_entry, p=password_entry, r=root : verify_existing(f,u,p,r))
    login_button.grid(row=4, column=0, columnspan=2, pady=20)

    register_label = tk.Button(root, text="Don't have an account? Register here.", font=("Arial", 20), bg="#f0f0f0", justify="center", command=lambda f=firstname_entry, u=username_entry, p=password_entry, r=root : register_new(f,u,p,r))
    register_label.grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()

task_list : CustomListbox
root : tk.Tk

def init_task_interface() -> None:
    global task_list
    global root

    root = tk.Tk()
    root.config(bg="white")
    root.geometry("960x540+333+135")
    root.resizable(False, False)

    util_frame = tk.Frame(root)
    util_frame.place(relx=0, rely=0, anchor="nw")
    profile_frame = tk.Frame(root)
    profile_frame.place(relx=1, rely=0, anchor="ne")
    task_frame = tk.Frame(root, height=500)
    task_frame.place(relx=0.5, rely=1, anchor="s")

    task_list = CustomListbox(task_frame, 550, 450)
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
    filter_icon = tk.PhotoImage(file=constants.FILTERFILE)
    filter_button = tk.Button(util_frame, image=filter_icon, bd=0, bg="white")
    filter_button.configure(command=task_list.filter_interface)
    filter_button.grid(row=0, column=1)
    profile_icon = tk.PhotoImage(file=constants.PROFILEFILE)
    profile_button = tk.Button(profile_frame, image=profile_icon, bd=0, bg="white", command=lambda r=root, i=init : taskutil.sign_out(r, i))
    profile_button.pack()
    up_button = tk.Button(root, text="↑", bg="white", fg="black", font=("Times New Roman", 30, "bold"))
    up_button.configure(command=task_list.move_up)
    up_button.place(relx=0.7875, rely=0.1675, anchor="nw")
    down_button = tk.Button(root, text="↓", bg="white", fg="black", font=("Times New Roman", 30, "bold"))
    down_button.configure(command=task_list.move_down)
    down_button.place(relx=0.7875, rely=0.9875, anchor="sw")
    add_icon = tk.PhotoImage(file=constants.ADDFILE)
    add_button = tk.Button(root, image=add_icon, bg="white", bd=0)
    add_button.configure(command=task_list.add_task)
    add_button.place(relx=0.1, rely=0.5, anchor="center")

    
    root.mainloop()

taskutil.load_tasks()
init_task_interface()