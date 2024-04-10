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

    status_keycodes = {
        "Not Started": ["NS", (0, 0, 0), "white", 0],
        "Delayed": ["D", (128, 0, 0), "black", 1],
        "Underway": ["U", (237, 41, 57), "black", 2],
        "Almost Completed": ["AC", (152, 251, 152), "black", 3],
        "Finished": ["F", (199, 234, 70), "black", 4]
    }

    importance_keycodes = {
        "Negligible": ["N", (199, 234, 70), "black", 4],
        "Trivial": ["T", (152, 251, 152), "black", 3],
        "Average": ["A", (237, 41, 57), "black", 2],
        "Significant": ["S", (128, 0, 0), "black", 1],
        "Critical": ["C", (0, 0, 0), "white", 0]
    }
    
    def __init__(self, name:str="newtask", description:str="description", deadline:str="deadline", status:str="Not Started", importance:str="Negligible") -> None:
        self.name = name
        self.description = description
        self.date_added = self.get_current_date()
        self.time_added = self.get_current_time()
        self.deadline = deadline
        self.status = status
        self.importance = importance
        
        self.elements = [self.name, self.description, self.deadline, self.status, self.importance]

    def get_current_date(self) -> str:
        localtime = time.localtime()
        list_of_date = [str(localtime[1]), str(localtime[2]), str(localtime[0])]
        return "".join(list_of_date)

    def get_current_time(self) -> str:
        localtime = time.localtime()
        list_of_times = [str(localtime[3]), str(localtime[4]), str(localtime[5])]
        return "".join(list_of_times)
    
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