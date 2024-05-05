from datetime import datetime, timedelta
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

    def __init__(self, root:tk.Tk=None, width=0, height=0, bg="white", **kwargs) -> None:
        self.cal_frame = tk.Frame(root, width=width, height=height, bg=bg, **kwargs)
        self.root = root
        self.bg = bg

        self.calendar_icon = tk.PhotoImage(file=constants.CALENDARFILE)
        self.show_button = tk.Button(self.cal_frame, bd=0, bg="white", text="Back", fg="black", font=("Times New Roman", 30, "bold"))
        self.show_button.configure(command=lambda a=globalvar.add_button, al=globalvar.add_label, u=globalvar.up_button, d=globalvar.down_button : self.toggle_show(a,al,u,d))

        self.next_button = tk.Button(self.cal_frame, bd=0, bg="white", text="Next", fg="black", font=("Times New Roman", 30, "bold"))
        self.next_button.configure(command=self.next)
        self.prev_button = tk.Button(self.cal_frame, bd=0, bg="white", text="Previous", fg="black", font=("Times New Roman", 30, "bold"))
        self.prev_button.configure(command=self.prev)
        self.curr_day = self.get_this_date()
        self.curr_week = self.get_this_week()
        self.curr_month = self.month_keycodes[str(self.curr_day.month)]
        self.week_values = self.get_this_week_dates()
        self.month_values = self.get_this_month_dates()
        self.group_display = tk.StringVar()
        self.group_display.set(self.curr_month)
        self.group_select = tk.StringVar()
        self.group_select.set("Month")
        self.group_label = tk.Label(self.cal_frame, bg="red", fg="black", font=("Times New Roman", 30, "bold"), textvariable=self.group_display)
        self.group_option = tk.OptionMenu(self.cal_frame, self.group_select, "Day", "Week", "Month")
        self.group_option.configure(bg="white", fg="black", font=("Times New Roman", 30, "bold"))

        self.month_days_keycodes = {
            1:31,
            2:29 if self.curr_day.year % 4 == 0 else 28,
            3:31,
            4:30,
            5:31,
            6:30,
            7:31,
            8:31,
            9:30,
            10:31,
            11:30,
            12:31
        }

    def get_this_week_dates(self, day=datetime.today()) -> list[str]:
        start_of_week = day - timedelta(days=day.weekday())
        week_dates_formatted = []

        for i in range(7):
            formatted_date = (start_of_week + timedelta(days=i)).strftime("%m/%d/%Y")
            week_dates_formatted.append(formatted_date)

        return week_dates_formatted

    def get_this_month_dates(self, day=datetime.today()) -> list[str]:
        first_day_of_month = day.replace(day=1)
        start_of_week = first_day_of_month - timedelta(days=first_day_of_month.weekday())

        if day.month == 12:
            last_day_of_month = day.replace(day=31)
        else:
            last_day_of_month = day.replace(month=day.month + 1, day=1) - timedelta(days=1)

        start_of_month_range = start_of_week - timedelta(days=1)
        end_of_month_range = last_day_of_month + timedelta(days=1)

        month_dates_formatted = []

        current_date = start_of_month_range
        while current_date <= end_of_month_range:
            formatted_date = current_date.strftime("%m/%d/%y")
            month_dates_formatted.append(formatted_date)
            current_date += timedelta(days=1)

        return month_dates_formatted
    
    def get_this_date(self) -> datetime:
        localtime = time.localtime()
        current_date = [localtime[1], localtime[2], localtime[0]]
        return datetime(current_date[2], current_date[0], current_date[1])

    def get_this_week(self, day=datetime.today()) -> str:
        return self.get_this_week_dates(day)[0][0:5] + "-" + self.get_this_week_dates(day)[-1][0:5]

    def get_this_month(self) -> str:
        return self.month_keycodes[str(self.get_this_date()[0])]
    
    def date_list_to_string(self, date:datetime) -> str:
        return str(date.month) + "/" + str(date.day) + "/" + str(date.year)

    def update_group_label(self):
        self.month_days_keycodes[2] = 29 if self.curr_day.year % 4 == 0 else 28
        if self.group_select.get() == "Day":
            self.group_display.set(self.date_list_to_string(self.curr_day))
        elif self.group_select.get() == "Week":
            self.group_display.set(self.get_this_week(self.curr_day) + " " + str(self.curr_day.year))
        elif self.group_select.get() == "Month":
            self.group_display.set(self.month_keycodes[str(self.curr_day.month)] + " " + str(self.curr_day.year))
        self.root.after(200, self.update_group_label)

    def next(self) -> None:
        if self.group_select.get() == "Day":
            if self.curr_day.month == 12 and self.curr_day.day == 31:
                self.curr_day = datetime(month=1, year=self.curr_day.year + 1, day=1)
            elif self.curr_day.month != 12 and self.curr_day.day == self.month_days_keycodes[self.curr_day.month]:
                self.curr_day = datetime(month=self.curr_day.month + 1, day=1, year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day + 1, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Week":
            day_offset = self.curr_day.day + 7
            if day_offset > self.month_days_keycodes[self.curr_day.month]:
                if self.curr_day.month == 12:
                    self.curr_day = datetime(month=1, year=self.curr_day.year + 1, day=day_offset-self.month_days_keycodes[self.curr_day.month])
                elif self.curr_day.month != 12:
                    self.curr_day = datetime(month=self.curr_day.month + 1, day=day_offset-self.month_days_keycodes[self.curr_day.month], year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day + 7, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Month":
            if self.curr_day.month < 12:
                self.curr_day = datetime(day=self.curr_day.day, month=self.curr_day.month + 1, year=self.curr_day.year)
            elif self.curr_day.month == 12:
                self.curr_day = datetime(day=self.curr_day.day, month=1, year=self.curr_day.year + 1)

    def prev(self) -> None:
        if self.group_select.get() == "Day":
            if self.curr_day.month == 1 and self.curr_day.day == 1:
                self.curr_day = datetime(month=12, year=self.curr_day.year - 1, day=31)
            elif self.curr_day.month != 1 and self.curr_day.day == 1:
                self.curr_day = datetime(month=self.curr_day.month - 1, day=self.month_days_keycodes[self.curr_day.month-1], year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day - 1, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Week":
            day_offset = self.curr_day.day - 7
            if day_offset <= 0:
                if self.curr_day.month == 1:
                    self.curr_day = datetime(month=12, year=self.curr_day.year - 1, day=self.month_days_keycodes[12]+day_offset)
                elif self.curr_day.month != 1:
                    self.curr_day = datetime(month=self.curr_day.month - 1, day=self.month_days_keycodes[self.curr_day.month-1]+day_offset, year=self.curr_day.year)
            else:
                self.curr_day = datetime(day=self.curr_day.day - 7, year=self.curr_day.year, month=self.curr_day.month)
        elif self.group_select.get() == "Month":
            if self.curr_day.month > 1:
                self.curr_day = datetime(day=self.curr_day.day, month=self.curr_day.month - 1, year=self.curr_day.year)
            elif self.curr_day.month == 1:
                self.curr_day = datetime(day=self.curr_day.day, month=12, year=self.curr_day.year - 1)
        
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
            self.prev_button.place(relx=0.25, rely=0, anchor="n")
            self.group_label.place(relx=0.5, rely=0, anchor="n")
            self.next_button.place(relx=0.75, rely=0, anchor="n")
            self.group_option.place(relx=1, rely=0, anchor="ne")
            self.root.after(200, self.update_group_label)
        else:
            self.curr_day = self.get_this_date()
            self.cal_frame.place_forget()

            add_button.place(relx=0.1, rely=0.5, anchor="center")
            add_label.place(relx=0.1, rely=0.6, anchor="center")
            up_button.place(relx=0.7875, rely=0.1675, anchor="nw")
            down_button.place(relx=0.7875, rely=0.9875, anchor="sw")
        self.show_ctr += 1