from PIL import ImageTk, ImageFilter, Image, ImageGrab
from Task import Task
import tkinter as tk
import globalvar
import constants
import taskutil

class Listbox(tk.Frame):
    def __init__(self, master=None, root=tk.Tk, width=0, height=0, bg="white", **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, width=width, height=height, bg=bg)
        self.list_frame = tk.Frame(self.canvas)
        self.bg_color = self.rgb_to_hex((240, 240, 240))
        self.root = root

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")

        self.list_index:int

        self.edit_large_icon = tk.PhotoImage(file=constants.EDITLARGEFILE)
        self.edit_icon = tk.PhotoImage(file=constants.EDITFILE)
        self.delete_icon = tk.PhotoImage(file=constants.DELETEFILE)
        self.filter_large_icon = tk.PhotoImage(file=constants.FILTERLARGEFILE)

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
        self.edit_label:tk.Label
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
        self.status_entry:tk.OptionMenu
        self.status_var = tk.StringVar()
        self.importance_entry:tk.OptionMenu
        self.importance_var = tk.StringVar()

        self.month_entry:tk.OptionMenu
        self.day_entry:tk.OptionMenu
        self.year_entry:tk.OptionMenu
        self.month_label:tk.Label
        self.day_label:tk.Label
        self.year_label:tk.Label
        self.month_var = tk.StringVar()
        self.day_var = tk.StringVar()
        self.year_var = tk.StringVar()
        self.valid_years = taskutil.get_valid_years()

    def rgb_to_hex(self, rgb:tuple) -> str:
        return '#{:02x}{:02x}{:02x}'.format(*rgb)

    def insert(self, idx:int, task:taskutil.Task) -> None:
        y_multiplier = 0.015 + (idx*0.13)
        y_multiplier2 = 0.0785 + (idx*0.13)
        
        name_label = tk.Label(self.canvas, text=task.name[:13], font=('Helvetica', 33))
        name_label.place(relx=0.01, rely=y_multiplier, anchor="nw")
        
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
        self.screenshot_photo = ImageTk.PhotoImage(self.screenshot)
        self.screenshot_label = tk.Label(self.root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = ImageTk.PhotoImage(self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.Button(self.root, bg="white", fg="black", text="←", font=("Helvetica", 50, "bold"), relief="flat")
        self.back_button.configure(command=self.back_from_filter)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.filter_large = tk.Label(self.root, image=self.filter_large_icon, bd=0, bg=self.bg_color)
        self.filter_large.place(relx=0.125, rely=0.5, anchor="center")

        self.filter_name = tk.Button(self.root, text="Filter by Name", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
        self.filter_dead = tk.Button(self.root, text="Filter by Deadline", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
        self.filter_status = tk.Button(self.root, text="Filter by Status", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
        self.filter_importance = tk.Button(self.root, text="Filter by Importance", bg="white", fg="black", font=("Times New Roman", 33, "bold"))
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
        self.screenshot_photo = ImageTk.PhotoImage(self.screenshot)
        self.screenshot_label = tk.Label(self.root, image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()
        self.blurred_screenshot = self.screenshot.filter(ImageFilter.GaussianBlur(9))
        self.screenshot_photo = ImageTk.PhotoImage(self.blurred_screenshot)
        self.screenshot_label.configure(image=self.screenshot_photo)
        self.screenshot_label.image = self.screenshot_photo
        self.screenshot_label.pack()

        self.back_button = tk.Button(self.root, bg="white", fg="black", text="←", font=("Helvetica", 50, "bold"), relief="flat")
        self.back_button.configure(command=self.back_from_edit)
        self.back_button.place(relx=-0.005, rely=-0.055, anchor="nw")

        self.old_name = tk.Label(self.root, text=name[:17], bg="black", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_name.place(relx=0.25, rely=1/6, anchor="w")
        self.old_desc = tk.Label(self.root, text=taskutil.find_task(name).description, bg="black", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_desc.place(relx=0.25, rely=2/6, anchor="w")
        self.old_dead = tk.Label(self.root, text=((taskutil.find_task(name).deadline + "*") if (taskutil.find_task(name).deadline == "00/00/0000") else (taskutil.find_task(name).deadline)), bg="black", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_dead.place(relx=0.25, rely=3/6, anchor="w")
        self.old_status = tk.Label(self.root, text=taskutil.find_task(name).status, bg="black", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_status.place(relx=0.25, rely=4/6, anchor="w")
        self.old_importance = tk.Label(self.root, text=taskutil.find_task(name).importance, bg="black", fg="white", font=("Times New Roman", 40, "bold"))
        self.old_importance.place(relx=0.25, rely=5/6, anchor="w")
        self.name_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 40, "bold"), width=10)
        self.name_entry.place(relx=0.95, rely=1/6, anchor="e")
        self.desc_entry = tk.Entry(self.root, bg="black", fg="white", font=("Times New Roman", 40, "bold"), width=10)
        self.desc_entry.place(relx=0.95, rely=2/6, anchor="e")
        self.status_entry = tk.OptionMenu(self.root, self.status_var, "Not Started", "Delayed", "Underway", "Almost Completed", "Finished")
        self.status_entry.place(relx=0.95, rely=4/6, anchor="e")
        self.importance_entry = tk.OptionMenu(self.root, self.importance_var, "Minimal", "Trivial", "Average", "Significant", "Critical")
        self.importance_entry.place(relx=0.95, rely=5/6, anchor="e")

        self.year_entry = tk.OptionMenu(self.root, self.year_var, self.valid_years[0], self.valid_years[1], self.valid_years[2], self.valid_years[3], self.valid_years[4], self.valid_years[5], self.valid_years[6], self.valid_years[7], self.valid_years[8], self.valid_years[9])
        self.year_entry.place(relx=0.95, rely=3/6, anchor="e")
        self.month_entry = tk.OptionMenu(self.root, self.month_var, "January:01", "February:02", "March:03", "April:04", "May:05", "June:06", "July:07", "August:08", "September:09", "October:10", "November:11", "December:12")
        self.month_entry.place(relx=0.6675, rely=3/6, anchor="w")
        self.day_entry = tk.OptionMenu(self.root, self.day_var, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
        self.day_entry.place(relx=((0.9425+0.675)/2), rely=3/6, anchor="center")

        self.edit_large = tk.Button(self.root, image=self.edit_large_icon, bd=0, bg=self.bg_color)
        self.edit_large.configure(command=lambda n=self.curr_task_name, ne=self.name_entry, dese=self.desc_entry, se=self.status_var, ie=self.importance_var: self.edit_task(n, ne, dese, se, ie))
        self.edit_large.place(relx=0.125, rely=0.4, anchor="center")
        self.edit_label = tk.Label(self.root, text="Edit Task", justify="center", font=("Times New Roman", 35, "bold"), bg="white", fg="black")
        self.edit_label.place(relx=0.125, rely=0.575, anchor="center")
    
    def edit_task(self, name:str, name_entry:tk.Entry, desc_entry:tk.Entry, status_entry:tk.Entry, importance_entry:tk.Entry) -> None:
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

    def delete(self, delete_button:tk.Button) -> None:
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