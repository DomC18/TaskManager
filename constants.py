import os

TASKMANAGERDIR = os.path.realpath(__file__)[:-12]
USERDATADIR = TASKMANAGERDIR + "UserData\\"
USERLISTFILE = USERDATADIR + "UserList.txt"
ICONDIR = TASKMANAGERDIR + "Icons\\"
DELETEFILE = ICONDIR + "delete.png"
EDITFILE = ICONDIR + "edit.png"
FILTERFILE = ICONDIR + "filter.png"
PROFILEFILE = ICONDIR + "profile.png"
SAVEFILE = ICONDIR + "save.png"