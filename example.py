import tkinter as tk

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Create a listbox for tasks
        self.task_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
        self.task_listbox.pack(padx=10, pady=10)

        # Add sample tasks
        tasks = ["Buy groceries", "Finish report", "Exercise", "Read book"]
        for task in tasks:
            self.task_listbox.insert(tk.END, task)

        # Create colored tags
        self.tag_colors = {
            "Personal": "blue",
            "Work": "green",
            "Health": "red",
            "Misc": "purple"
        }

        # Add tags to tasks
        for i, task in enumerate(tasks):
            tag = list(self.tag_colors.keys())[i % len(self.tag_colors)]
            self.task_listbox.itemconfig(i, bg=self.tag_colors[tag])

        # Add utility icons (e.g., delete, edit)
        # delete_icon = tk.PhotoImage(file="delete_icon.png")
        # edit_icon = tk.PhotoImage(file="edit_icon.png")

        self.delete_button = tk.Button(root, command=self.delete_task)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(root, command=self.edit_task)
        self.edit_button.pack(side=tk.LEFT, padx=5)

    def delete_task(self):
        selected_task = self.task_listbox.get(self.task_listbox.curselection())
        self.task_listbox.delete(self.task_listbox.curselection())
        print(f"Deleted task: {selected_task}")

    def edit_task(self):
        selected_task = self.task_listbox.get(self.task_listbox.curselection())
        print(f"Editing task: {selected_task}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
