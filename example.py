import tkinter as tk

root = tk.Tk()
root.title("Tasks Layout")

# Create frames for the left and right sections
left_frame = tk.Frame(root, width=200, height=400)
left_frame.grid(row=0, column=0, padx=10, pady=5)

right_frame = tk.Frame(root)
right_frame.grid(row=0, column=1, padx=10, pady=5)

# Adding elements to the left frame (similar to the image)
label1 = tk.Label(left_frame, text="Task 1", bg="red", fg="white")
label1.pack(fill=tk.BOTH)

label2 = tk.Label(left_frame, text="Task 2", bg="yellow", fg="black")
label2.pack(fill=tk.BOTH)

label3 = tk.Label(left_frame, text="Task 3", bg="white", fg="black")
label3.pack(fill=tk.BOTH)

# Adding elements to the right frame (icons or buttons as needed)
button1 = tk.Button(right_frame, text="+")
button1.grid(row=0, column=0)

button2 = tk.Button(right_frame, text="-")
button2.grid(row=0, column=1)

root.mainloop()