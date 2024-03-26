def add_task(current_tasks:list, task_name:str) -> None:
    current_tasks.append(task_name)

def edit_task(task_name:str) -> None:
    pass

def delete_task(current_tasks:list, task_name:str) -> str:
    return current_tasks.remove(task_name)