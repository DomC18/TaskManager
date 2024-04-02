import time

class Task:
    date_added:str
    time_added:str

    name:str
    description:str
    deadline:str
    status:int
    importance:int
    
    elements:list = []

    status_keycodes = \
    {
        0: "Not Started",
        1: "Stuck",
        2: "In Progress",
        4: "Almost Complete",
        5: "Complete"
    }
    importance_keycodes = \
    {
        0: "Very Low Importance",
        1: "Low Importance",
        2: "Medium Importance",
        3: "High Importance",
        4: "Very High Importance"
    }
    
    def __init__(self, name:str="", description:str="", deadline:str="", status:int=0, importance:int=0) -> None:
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

    def get_status(self) -> str:
        return self.status_keycodes[self.status]

    def get_importance(self) -> str:
        return self.importance_keycodes[self.importance]

    def change_name(self, new_name:str) -> None:
        self.name = new_name
    
    def change_description(self, new_description:str) -> None:
        self.description = new_description

    def change_date_to_finish(self, new_deadline:str) -> None:
        self.deadline = new_deadline

    def change_importance(self, new_importance:int) -> None:
        self.importance = new_importance
    
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