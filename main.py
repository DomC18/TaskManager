import constants
import util
import ui
import os

user_list = []
user_tasks = []


with open(constants.USERLISTFILE) as f:
    user_list = f.read()
user_list = user_list.split("\n")[:-1]


def main() -> None:
    ui.init_login_interface()
    ui.init_task_interface()


main()