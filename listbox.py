from PIL import ImageTk, ImageFilter, Image, ImageGrab
from Task import Task
import customtkinter as tk
import globalvar
import constants
import taskutil

class Listbox(tk.CTkFrame):
    def __init__(self, master=None, root=tk.CTk, width=0, height=0, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.canvas = tk.CTkCanvas(self, width=width, height=height)
        self.list_frame = tk.CTkFrame(self.canvas)
        self.bg_color = self.rgb_to_hex((240, 240, 240))
        self.root = root

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_index:int

        self.edit_large_icon = tk.CTkImage(light_image=Image.open(constants.EDITLARGEFILE), dark_image=Image.open(constants.EDITLARGEFILE))
        self.edit_icon = tk.CTkImage(light_image=Image.open(constants.EDITFILE), dark_image=Image.open(constants.EDITFILE))
        self.delete_icon = tk.CTkImage(light_image=Image.open(constants.DELETEFILE), dark_image=Image.open(constants.DELETEFILE))
        self.filter_large_icon = tk.CTkImage(light_image=Image.open(constants.FILTERLARGEFILE), dark_image=Image.open(constants.FILTERLARGEFILE))

        self.button_images : dict = {}
        self.task_combos : dict = {}

        self.curr_task_name:str
        self.x:int
        self.y:int
        self.w:int
        self.h:int
        self.blurred_screenshot:Image
        self.screenshot:Image
        self.screenshot_photo:ImageTk.PhotoImage
        self.screenshot_label:tk.CTkLabel
        self.edit_large:tk.CTkButton
        self.edit_label:tk.CTkLabel
        self.back_button:tk.CTkButton

        self.filter_name:tk.CTkButton
        self.filter_dead:tk.CTkButton
        self.filter_status:tk.CTkButton
        self.filter_importance:tk.CTkButton

        self.old_name:tk.CTkLabel
        self.old_desc:tk.CTkLabel
        self.old_dead:tk.CTkLabel
        self.old_status:tk.CTkLabel
        self.old_importance:tk.CTkLabel
        self.name_entry:tk.CTkEntry
        self.desc_entry:tk.CTkEntry
        self.status_entry:tk.CTkOptionMenu
        self.status_var = tk.Variable()
        self.importance_entry:tk.CTkOptionMenu
        self.importance_var = tk.Variable()

        self.month_entry:tk.CTkOptionMenu
        self.day_entry:tk.CTkOptionMenu
        self.year_entry:tk.CTkOptionMenu
        self.month_label:tk.CTkLabel
        self.day_label:tk.CTkLabel
        self.year_label:tk.CTkLabel
        self.month_var = tk.Variable()
        self.day_var = tk.Variable()
        self.year_var = tk.Variable()
        self.valid_years = taskutil.get_valid_years()

    def rgb_to_hex(self, rgb:tuple) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def insert(self, idx:int, task:taskutil.Task) -> None:
        y_multiplier = 0.015 + (idx*0.13)
        y_multiplier2 = 0.0785 + (idx*0.13)
        
        name_label = tk.CTkLabel(self.canvas, text=task.name[:13], font=('Helvetica', 33))
        name_label.place(relx=0.01, rely=y_multiplier, anchor="nw")
        
        edit_button = tk.CTkButton(self.canvas, border_width=0, bg_color=self.bg_color)
        self.button_images.update({edit_button:self.edit_icon})
        edit_button.configure(command=lambda n=task.name : self.edit_task_interface(n))
        edit_button.configure(image=self.button_images[edit_button])
        edit_button.place(relx=0.875, rely=y_multiplier, anchor="ne")
        
        delete_button = tk.CTkButton(self.canvas, border_width=0, bg_color=self.bg_color)
        self.button_images.update({delete_button:self.delete_icon})
        delete_button.configure(command=lambda b=delete_button : self.delete(b))
        delete_button.configure(image=self.button_images[delete_button])
        delete_button.place(relx=0.975, rely=y_multiplier, anchor="ne")

        status_indicator = tk.CTkLabel(self.canvas, bg_color=self.rgb_to_hex(task.get_status_color()), text=task.get_status_short(), font=("Times New Roman", 40, "bold"), fg_color=task.get_status_font())
        status_indicator.place(relx=0.575, rely=y_multiplier2, anchor="center")
        importance_indicator = tk.CTkLabel(self.canvas, bg_color=self.rgb_to_hex(task.get_importance_color()), text=task.get_importance_short(), font=("Times New Roman", 40, "bold"), fg_color=task.get_importance_font())
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
        self.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, task)
        self.pack()

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
        self.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, task)
        self.pack()

    def add_task(self) -> None:
        if taskutil.amount_task("newtask") == 1:
            return
            
        globalvar.user_tasks.insert(0, Task())

        self.list_index = 0
        task_names = self.task_combos.keys()
        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
        self.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, task)
        self.pack()

        taskutil.save_tasks()

    def filter_interface(self) -> None:
        self.x = self.root.winfo_rootx()
        self.y = self.root.winfo_rooty()
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        self.screenshot = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.w, self.y+self.h))
        self.screenshot_photo = tk.CTkImage(light_image=self.screenshot, dark_image=self.screenshot)
        self.screenshot_label = tk.CTkLabel(self.root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = ImageTk.PhotoImage(self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.CTkButton(self.root, bg_color="white", fg_color="black", text="←", font=("Helvetica", 50, "bold"))
        self.back_button.configure(command=self.back_from_filter)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.filter_large = tk.CTkLabel(self.root, image=self.filter_large_icon, border_width=0, bg_color=self.bg_color)
        self.filter_large.place(relx=0.125, rely=0.5, anchor="center")

        self.filter_name = tk.CTkButton(self.root, text="Filter by Name", bg_color="white", fg_color="black", font=("Times New Roman", 33, "bold"))
        self.filter_dead = tk.CTkButton(self.root, text="Filter by Deadline", bg_color="white", fg_color="black", font=("Times New Roman", 33, "bold"))
        self.filter_status = tk.CTkButton(self.root, text="Filter by Status", bg_color="white", fg_color="black", font=("Times New Roman", 33, "bold"))
        self.filter_importance = tk.CTkButton(self.root, text="Filter by Importance", bg_color="white", fg_color="black", font=("Times New Roman", 33, "bold"))
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
        self.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, task)
        self.pack()

    def edit_task_interface(self, name:str) -> None:
        self.curr_task_name = name

        self.x = self.root.winfo_rootx()
        self.y = self.root.winfo_rooty()
        self.w = self.root.winfo_width()
        self.h = self.root.winfo_height()
        self.screenshot = ImageGrab.grab(bbox=(self.x, self.y, self.x+self.w, self.y+self.h))
        self.screenshot_photo = tk.CTkImage(light_image=self.screenshot, dark_image=self.screenshot)
        self.screenshot_label = tk.CTkLabel(self.root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = tk.CTkImage(light_image=self.blurred_screenshot, dark_image=self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.CTkButton(self.root, bg_color="white", fg_color="black", text="←", font=("Helvetica", 50, "bold"))
        self.back_button.configure(command=self.back_from_edit)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.old_name = tk.CTkLabel(self.root, text=name[:17], bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.old_name.place(relx=0.25, rely=1/6, anchor="w")
        self.old_desc = tk.CTkLabel(self.root, text=taskutil.find_task(name).description, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.old_desc.place(relx=0.25, rely=2/6, anchor="w")
        self.old_dead = tk.CTkLabel(self.root, text=((taskutil.find_task(name).deadline + "*") if (taskutil.find_task(name).deadline == "00/00/0000") else (taskutil.find_task(name).deadline)), bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.old_dead.place(relx=0.25, rely=3/6, anchor="w")
        self.old_status = tk.CTkLabel(self.root, text=taskutil.find_task(name).status, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.old_status.place(relx=0.25, rely=4/6, anchor="w")
        self.old_importance = tk.CTkLabel(self.root, text=taskutil.find_task(name).importance, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.old_importance.place(relx=0.25, rely=5/6, anchor="w")
        self.name_entry = tk.CTkEntry(self.root, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"), width=10)
        self.name_entry.place(relx=0.95, rely=1/6, anchor="e")
        self.desc_entry = tk.CTkEntry(self.root, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"), width=10)
        self.desc_entry.place(relx=0.95, rely=2/6, anchor="e")
        self.status_entry = tk.CTkOptionMenu(self.root, variable=self.status_var, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.status_entry.place(relx=0.95, rely=4/6, anchor="e")
        self.importance_entry = tk.CTkOptionMenu(self.root, variable=self.importance_var, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.importance_entry.place(relx=0.95, rely=5/6, anchor="e")

        self.year_entry = tk.CTkOptionMenu(self.root, variable=self.year_var, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.year_entry.place(relx=0.95, rely=3/6, anchor="e")
        self.month_entry = tk.CTkOptionMenu(self.root, variable=self.month_var, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.month_entry.place(relx=0.6675, rely=3/6, anchor="w")
        self.day_entry = tk.CTkOptionMenu(self.root, variable=self.day_var, bg_color="black", fg_color="white", font=("Times New Roman", 40, "bold"))
        self.day_entry.place(relx=((0.9425+0.675)/2), rely=3/6, anchor="center")

        self.edit_large = tk.CTkButton(self.root, image=self.edit_large_icon, border_width=0, bg_color=self.bg_color)
        self.edit_large.configure(command=lambda n=self.curr_task_name, ne=self.name_entry, dese=self.desc_entry, se=self.status_var, ie=self.importance_var: self.edit_task(n, ne, dese, se, ie))
        self.edit_large.place(relx=0.125, rely=0.4, anchor="center")
        self.edit_label = tk.CTkLabel(self.root, text="Edit Task", justify="center", font=("Times New Roman", 35, "bold"), bg_color="white", fg_color="black")
        self.edit_label.place(relx=0.125, rely=0.575, anchor="center")
    
    def edit_task(self, name:str, name_entry:tk.CTkEntry, desc_entry:tk.CTkEntry, status_entry:tk.CTkEntry, importance_entry:tk.CTkEntry) -> None:
        if not taskutil.edit_task(name, name_entry, desc_entry, self.month_var, self.day_var, self.year_var, status_entry, importance_entry):
            return
        self.back_from_edit()

        task_names = self.task_combos.keys()

        for task_name in task_names:
            self.task_combos[task_name][1].destroy()
            self.task_combos[task_name][2].destroy()
            self.task_combos[task_name][3].destroy()
            self.task_combos[task_name][4].destroy()
            self.task_combos[task_name][5].destroy()
        self.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, task)
        self.pack()

    def back_from_edit(self) -> None:
        self.back_button.destroy()
        self.screenshot_label.destroy()
        self.edit_large.destroy()
        self.edit_label.destroy()
        self.old_name.destroy()
        self.old_desc.destroy()
        self.old_dead.destroy()
        self.old_status.destroy()
        self.old_importance.destroy()
        self.name_entry.destroy()
        self.desc_entry.destroy()
        self.month_entry.destroy()
        self.day_entry.destroy()
        self.year_entry.destroy()
        self.status_entry.destroy()
        self.importance_entry.destroy()

        self.month_var.set("")
        self.day_var.set("")
        self.year_var.set("")
        self.status_var.set("")
        self.importance_var.set("")

    def delete(self, delete_button:tk.CTkButton) -> None:
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
        
        self.place_forget()
        for idx, task in enumerate(globalvar.user_tasks):
            if idx < self.list_index:
                continue
            if idx > self.list_index + 6:
                break
            self.insert(idx-self.list_index, task)
        self.pack()