import time

class Task:
    date_added:str
    time_added:str

    name:str
    description:str
    date_to_finish:str
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
    
    def __init__(self, name:str="", description:str="", date_to_finish:str="", status:int=0, importance:int=0) -> None:
        self.name = name
        self.description = description
        self.date_added = self.get_current_date()
        self.time_added = self.get_current_time()
        self.date_to_finish = date_to_finish
        self.status = status
        self.importance = importance
        
        self.elements = [self.name, self.description, self.date_to_finish, self.status, self.importance]

    def get_current_date(self) -> str:
        localtime = time.localtime()
        list_of_date = [localtime[1], localtime[2], localtime[0]]
        return "".join(list_of_date)

    def get_current_time(self) -> str:
        localtime = time.localtime()
        list_of_times = [localtime[3], localtime[4], localtime[5]]
        return "".join(list_of_times)

    def get_status(self) -> str:
        return self.status_keycodes[self.status]

    def get_importance(self) -> str:
        return self.importance_keycodes[self.importance]

    def change_name(self, new_name:str) -> None:
        self.name = new_name
    
    def change_description(self, new_description:str) -> None:
        self.description = new_description

    def change_date_to_finish(self, new_date_to_finish:str) -> None:
        self.date_to_finish = new_date_to_finish

    def change_importance(self, new_importance:int) -> None:
        self.importance = new_importance
    
    def __eq__(self, other) -> bool:
        return self.elements == other.elements

    def __repr__(self) -> str:
        return f"Name: {self.name}, Description: {self.description}, Date to Finish: {self.date_to_finish}, Status: {self.status}, Importance: {self.importance}"
    
    def __str__(self) -> str:
        return f"Name: {self.name}, Description: {self.description}, Date to Finish: {self.date_to_finish}, Status: {self.status}, Importance: {self.importance}"