import tkinter as tk
import constants
import globalvar
import time

class Calendar():
    show_ctr:int = 0

    month_keycodes = {
        "1":"January",
        "2":"February",
        "3":"March",
        "4":"April",
        "5":"May",
        "6":"June",
        "7":"July",
        "8":"August",
        "9":"September",
        "10":"October",
        "11":"November",
        "12":"December"
    }

    def __init__(self, root=None, width=0, height=0, bg="white", **kwargs) -> None:
        self.bg = bg
        self.cal_frame = tk.Frame(root, width=width, height=height, bg=self.bg, **kwargs)

        self.calendar_icon = tk.PhotoImage(file=constants.CALENDARFILE)
        self.show_button = tk.Button(self.cal_frame, bd=0, bg="white", text="Back", fg="black", font=("Times New Roman", 30, "bold"))
        self.show_button.configure(command=lambda a=globalvar.add_button, al=globalvar.add_label, u=globalvar.up_button, d=globalvar.down_button : self.toggle_show(a,al,u,d))

        self.day = self.date_list_to_string(self.get_current_date())
        self.week:str
        self.month = self.get_current_month()
        self.group_var = tk.StringVar()
        self.group_var.set(self.month)
        self.group_select = tk.StringVar()
        self.group_select.set("Month")
        self.group_label = tk.Label(self.cal_frame, bg="red", fg="black", font=("Times New Roman", 30, "bold"), textvariable=self.group_var)
        self.group_option = tk.OptionMenu(self.cal_frame, self.group_select, "Day", "Week", "Month")
        self.group_option.configure(bg="white", fg="black", font=("Times New Roman", 30, "bold"))

    def get_current_month(self) -> str:
        return self.month_keycodes[str(self.get_current_date()[0])]

    def get_current_date(self) -> list:
        localtime = time.localtime()
        current_date = [localtime[1], localtime[2], localtime[0]]
        return current_date
    
    def date_list_to_string(self, date_list:list) -> str:
        return str(date_list[0]) + "/" + str(date_list[1]) + "/" + str(date_list[2])

    def get_group_label(self) -> str:
        if self.group_select.get() == "Day":
            ...
        elif self.group_select.get() == "Week":
            ...
        elif self.group_select.get() == "Month":
            ...

    def next(self) -> None:
        pass

    def prev(self) -> None:
        pass

    def show_day(self) -> None:
        pass

    def show_week(self) -> None:
        pass

    def show_month(self) -> None:
        pass

    def toggle_show(self, add_button:tk.Button, add_label:tk.Label, up_button:tk.Button, down_button:tk.Button) -> None:
        if self.show_ctr % 2 == 0:
            add_button.place_forget()
            add_label.place_forget()
            up_button.place_forget()
            down_button.place_forget()
            self.cal_frame.place(relx=0.5, rely=0.5, anchor="center")

            self.group_select.set("Month")
            self.show_button.place(relx=0, rely=0, anchor="nw")
            self.group_label.place(relx=0.5, rely=0, anchor="n")
            self.group_option.place(relx=1, rely=0, anchor="ne")
        else:
            self.cal_frame.place_forget()

            add_button.place(relx=0.1, rely=0.5, anchor="center")
            add_label.place(relx=0.1, rely=0.6, anchor="center")
            up_button.place(relx=0.7875, rely=0.1675, anchor="nw")
            down_button.place(relx=0.7875, rely=0.9875, anchor="sw")
        self.show_ctr += 1