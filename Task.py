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
        "Not Started": ["NS", (0, 0, 0)],
        "Delayed": ["D", (128, 0, 0)],
        "Underway": ["U", (237, 41, 57)],
        "Almost Completed": ["AC", (152, 251, 152)],
        "Finished": ["F", (199, 234, 70)]
    }

    importance_keycodes = {
        "Negligible": ["N", (199, 234, 70)],
        "Minimal": ["M", (152, 251, 152)],
        "Average": ["A", (237, 41, 57)],
        "Significant": ["S", (128, 0, 0)],
        "Critical": ["C", (0, 0, 0)]
    }
    
    def __init__(self, name:str="NewTask", description:str="", deadline:str="", status:str="Not Started", importance:str="Negligible") -> None:
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