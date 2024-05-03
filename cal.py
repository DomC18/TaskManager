from PIL import Image
import customtkinter as tk
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

    def __init__(self, root=None, width=0, height=0, bg_color="white", **kwargs) -> None:
        self.bg = bg_color
        self.cal_frame = tk.CTkFrame(root, width=width, height=height, bg_color=self.bg, **kwargs)

        self.calendar_icon = tk.CTkImage(light_image=Image.open(constants.CALENDARFILE), dark_image=Image.open(constants.CALENDARFILE))
        self.show_button = tk.CTkButton(self.cal_frame, border_width=0, bg_color="white", text="Back", fg_color="black", font=("Times New Roman", 30, "bold"))
        self.show_button.configure(command=lambda a=globalvar.add_button, al=globalvar.add_label, u=globalvar.up_button, d=globalvar.down_button : self.toggle_show(a,al,u,d))

        self.day = self.date_list_to_string(self.get_current_date())
        self.week:str
        self.month = self.get_current_month()
        self.group_var = tk.Variable()
        self.group_var.set(self.month)
        self.group_select = tk.Variable()
        self.group_select.set("Month")
        self.group_label = tk.CTkLabel(self.cal_frame, bg_color="red", fg_color="black", font=("Times New Roman", 30, "bold"), text=self.group_var.get())
        self.group_option = tk.CTkOptionMenu(self.cal_frame, variable=self.group_select, bg_color="red", fg_color="black", font=("Times New Roman", 30, "bold"))
        self.group_option.configure(bg_color="white", fg_color="black", font=("Times New Roman", 30, "bold"))

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

    def toggle_show(self, add_button:tk.CTkButton, add_label:tk.CTkLabel, up_button:tk.CTkButton, down_button:tk.CTkButton) -> None:
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