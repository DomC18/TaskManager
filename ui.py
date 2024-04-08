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
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.list_frame = tk.Frame(self.canvas)
        self.bg_color = self.rgb_to_hex((240, 240, 240))

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.edit_icon = tk.PhotoImage(file=constants.EDITFILE)
        self.delete_icon = tk.PhotoImage(file=constants.DELETEFILE)

        self.button_images : dict = {}
        self.task_combos : dict = {}

        self.name_option = tk.Button()
        self.desc_option = tk.Button()
        self.deadline_option = tk.Button()
        self.status_option = tk.Button()
        self.importance_option = tk.Button()
        self.exit_option = tk.Button()

    def rgb_to_hex(self, rgb) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def insert(self, idx:int, task:taskutil.Task) -> None:
        y_multiplier = 0.01 + (idx*0.13)
        
        name_label = tk.Label(self.canvas, text=task.name, font=('Helvetica', 33))
        name_label.place(relx=0, rely=y_multiplier, anchor="nw")
        
        edit_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({edit_button:self.edit_icon})
        edit_button.configure(command= self.drop_down_edit)
        edit_button.configure(image=self.button_images[edit_button])
        edit_button.place(relx=0.825, rely=y_multiplier, anchor="ne")
        
        delete_button = tk.Button(self.canvas, bd=0, bg=self.bg_color)
        self.button_images.update({delete_button:self.delete_icon})
        delete_button.configure(command= lambda b=delete_button : self.delete(b))
        delete_button.configure(image=self.button_images[delete_button])
        delete_button.place(relx=0.95, rely=y_multiplier, anchor="ne")
        
        self.task_combos.update({task.name:[task.name, name_label, edit_button, delete_button]})
    
    def exit_edit(self) -> None:
        self.name_option.place_forget()
        self.desc_option.place_forget()
        self.deadline_option.place_forget()
        self.status_option.place_forget()
        self.importance_option.place_forget()
        self.exit_option.place_forget()

    def drop_down_edit(self) -> None:
        ...

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
                
        self.task_combos.pop(self.task_combos[name][0])
        globalvar.user_tasks.pop(globalvar.user_tasks.index(taskutil.find_task(name)))
        
        task_list.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            task_list.insert(idx, task)
        task_list.pack()
    

def init() -> None:
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

def init_task_interface() -> None:
    global task_list

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

    save_icon = tk.PhotoImage(file=constants.SAVEFILE)
    save_button = tk.Button(util_frame, image=save_icon, bd=0, bg="white", command=taskutil.save_tasks)
    save_button.grid(row=0, column=0)
    filter_icon = tk.PhotoImage(file=constants.FILTERFILE)
    filter_button = tk.Button(util_frame, image=filter_icon, bd=0, bg="white")
    filter_button.grid(row=0, column=1)
    profile_icon = tk.PhotoImage(file=constants.PROFILEFILE)
    profile_button = tk.Button(profile_frame, image=profile_icon, bd=0, bg="white", command=lambda r=root, i=init : taskutil.sign_out(r, i))
    profile_button.pack()

    task_list = CustomListbox(task_frame, 425, 425)
    for idx, task in enumerate(globalvar.user_tasks):
        task_list.insert(idx, task)
    task_list.pack()
    
    root.mainloop()

taskutil.load_tasks()
init_task_interface()