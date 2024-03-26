import GlobalVariables
import Task

def add_task(task_name:str, task_description:str="") -> None:
    GlobalVariables.user_tasks.append(Task())

def edit_task(task_name:str) -> None:
    pass

def delete_task(task_name:str) -> str:
    return GlobalVariables.user_tasks.remove(task_name)