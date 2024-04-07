import tkinter as tk

class CustomListbox(tk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.list_frame = tk.Frame(self.canvas)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side="right", fill="y")

        # Configure the canvas to update scroll region
        self.list_frame.bind("<Configure>", self._on_frame_configure)

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def insert(self, index, item):
        item_frame = tk.Frame(self.list_frame)
        label = tk.Label(item_frame, text=item, font=('Helvetica', 14))
        label.pack(side="left", fill='x')
        
        # Add buttons
        button1 = tk.Button(item_frame, text="Button 1")
        button1.pack(side="left")
        
        button2 = tk.Button(item_frame, text="Button 2")
        button2.pack(side="left")
        
        item_frame.pack(fill="x")
        
root = tk.Tk()

# Create a CustomListbox widget
listbox = CustomListbox(root)
listbox.pack()

# Insert some items into the Listbox
for i in range(20):
    listbox.insert(tk.END, f"Item {i}")

root.mainloop()
