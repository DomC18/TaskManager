from task import Task
import globalvariables as globalvariables

def add_task(task_name:str, task_description:str="") -> None:
    globalvariables.user_tasks.append(Task(task_name, task_description))

def edit_task(task_name:str) -> None:
    pass

def delete_task(task_name:str) -> str:
    return globalvariables.user_tasks.remove(task_name)