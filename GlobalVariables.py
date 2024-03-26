import Constants

user_list = []
user_jsons = []
user_tasks = []

with open(Constants.USERLISTFILE) as f:
    user_list = f.read()
user_list = user_list.split("\n")[:-1]
for name in user_list:
    user_jsons.append(Constants.USERDATADIR + name.casefold().capitalize() + "Data\\" + name.casefold().capitalize() + ".json")