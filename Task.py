import time

class Task:
    date_added:str
    time_added:str

    name:str
    description:str
    deadline:str
    status:str
    importance:str
    
    elements:list = []

    days_completed_keycodes = {
        1:0,
        2:31,
        3:(31+29 if time.localtime()[0] % 4 == 0 else 31+28),
        4:(31+29+31 if time.localtime()[0] % 4 == 0 else 31+28+31),
        5:(31+29+31+30 if time.localtime()[0] % 4 == 0 else 31+28+31+30),
        6:(31+29+31+30+31 if time.localtime()[0] % 4 == 0 else 31+28+31+30+31),
        7:(31+29+31+30+31+30 if time.localtime()[0] % 4 == 0 else 31+28+31+30+31+30),
        8:(31+29+31+30+31+30+31 if time.localtime()[0] % 4 == 0 else 31+28+31+30+31+30+31),
        9:(31+29+31+30+31+30+31+31 if time.localtime()[0] % 4 == 0 else 31+28+31+30+31+30+31+31),
        10:(31+29+31+30+31+30+31+31+30 if time.localtime()[0] % 4 == 0 else 31+28+31+30+31+30+31+31+30),
        11:(31+29+31+30+31+30+31+31+30+31 if time.localtime()[0] % 4 == 0 else 31+28+31+30+31+30+31+31+30+31),
        12:(31+29+31+30+31+30+31+31+30+31+30 if time.localtime()[0] % 4 == 0 else 31+28+31+30+31+30+31+31+30+31+30)
    }

    status_keycodes = {
        "Not Started": ["NS", (0, 0, 0), "white", 0],
        "Delayed": ["D", (128, 0, 0), "black", 1],
        "Underway": ["U", (237, 41, 57), "black", 2],
        "Almost Completed": ["AC", (152, 251, 152), "black", 3],
        "Finished": ["F", (199, 234, 70), "black", 4]
    }

    importance_keycodes = {
        "Minimal": ["M", (199, 234, 70), "black", 4],
        "Trivial": ["T", (152, 251, 152), "black", 3],
        "Average": ["A", (237, 41, 57), "black", 2],
        "Significant": ["S", (128, 0, 0), "black", 1],
        "Critical": ["C", (0, 0, 0), "white", 0]
    }
    
    def get_current_date(self) -> list:
        localtime = time.localtime()
        current_date = [localtime[1], localtime[2], localtime[0]]
        return current_date
    
    def date_list_to_string(self, date_list:list) -> str:
        new_month:str = ""

        if date_list[0] < 10:
            new_month = "0" + str(date_list[0])
        
        return new_month + "/" + str(date_list[1]) + "/" + str(date_list[2])

    def __init__(self, name:str="newtask", description:str="description", deadline:str="00/00/0000", status:str="Not Started", importance:str="Minimal") -> None:
        self.name = name
        self.description = description
        self.status = status
        self.importance = importance

        if deadline == "00/00/0000":
            self.deadline = self.date_list_to_string(self.get_current_date())
        else:
            self.deadline = deadline
        
        self.elements = [self.name, self.description, self.deadline, self.status, self.importance]

    def get_date_differential(self) -> int:
        curr_date = self.get_current_date()
        curr_month = curr_date[0]
        curr_day = curr_date[1]
        curr_year = curr_date[2]
        task_date = self.get_task_date()
        task_month = task_date[0]
        task_day = task_date[1]
        task_year = task_date[2]
        return (task_year*365-curr_year*365) + \
               (self.days_completed_keycodes[task_month]-self.days_completed_keycodes[curr_month]) + \
               (task_day - curr_day)
    
    def get_task_date(self) -> list:
        task_date = [int(self.deadline[0:2]), int(self.deadline[3:5]), int(self.deadline[6:10])]
        return task_date

    def get_status_short(self) -> str:
        return self.status_keycodes[self.status][0]

    def get_importance_short(self) -> str:
        return self.importance_keycodes[self.importance][0]

    def get_status_color(self) -> tuple:
        return self.status_keycodes[self.status][1]

    def get_importance_color(self) -> tuple:
        return self.importance_keycodes[self.importance][1]

    def get_status_font(self) -> str:
        return self.status_keycodes[self.status][2]

    def get_importance_font(self) -> str:
        return self.importance_keycodes[self.importance][2]

    def get_status_sort(self) -> int:
        return self.status_keycodes[self.status][3]

    def get_importance_sort(self) -> int:
        return self.importance_keycodes[self.importance][3]
    
    def __eq__(self, other) -> bool:
        return self.elements == other.elements

    def __repr__(self) -> str:
        return "{Name: " + self.name + ", Description: " + self.description + ", Date to Finish: " + self.deadline + ", Status: " + str(self.status) + ", Importance: " + str(self.importance) + "}"
    
    def __str__(self) -> str:
        return "{Name: " + self.name + ", Description: " + self.description + ", Date to Finish: " + self.deadline + ", Status: " + str(self.status) + ", Importance: " + str(self.importance) + "}"
    
    def return_as_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "deadline": self.deadline,
            "status": self.status,
            "importance": self.importance
        }