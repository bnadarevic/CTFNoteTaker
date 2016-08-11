import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from adminCommands.error import *

#Some check for user permission
def adminCmdParser(s,c,conn,user,line,cmd):
    Perm = True
    if(ADMINCOMMANDMODE =="MASTER"):
        if(user==MASTER):
            Perm = True
        else:
            Perm = False
    if(Perm == False):
        printChan("You don't have enough perms to use this command!")
        return
    if(cmd=="error"):
        throwErrorAdminCMD(s,c,conn,user,line)
    elif(cmd=="help"):
        adminHelp(s,user)

def adminHelp(s,user):
    printUser(s,"~error - Generates a sample error for testing purposes.",user)