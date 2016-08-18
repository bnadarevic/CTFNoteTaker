import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.permissionUtils import *
from adminCommands.error import *
from adminCommands.quit import *


#Some check for user permission
def adminCmdParser(s,c,conn,user,line,cmd):
    Perm = False
    print(line)
    if("MASTER" in ADMINCOMMANDMODE.upper()):
        if(Perm == False):
            if(userIsMaster(user)):
                Perm = True
    if("PASSWORD" in ADMINCOMMANDMODE.upper()):
        if(Perm == False):
            if(len(line) > 4):
                if(check_pass(line[4].strip())):
                    Perm = True
                    del line[4]
            else:
                printUser("You must enter the password.")
                return
    if(Perm == False):
        printUser(s,"You don't have enough perms to use this command!")
        return
    if(cmd=="error"):
        throwErrorAdminCMD(s,c,conn,user,line)
    elif(cmd=="help"):
        adminHelp(s,user)
    elif(cmd=="quit"):
        adminQuit(s,conn,user)

def userIsMaster(user):
    for mast in MASTER:
        if(mast.lower()==user.lower()):
            return True
    return False

def adminHelp(s,user):
    printUser(s,"~error - Generates a sample error for testing purposes.",user)
    printUser(s,"~quit - Shuts me down :(",user)
