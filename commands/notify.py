import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *

def startnotifycmd(user,line):

    if(len(line)>4):
        state=line[4]
        if(state.upper()=="ON" or state.upper()=="OFF"):
            notifymanage(user,state)
        else:
            printUser("parameters are ON or OFF",line[2])
    else:
        printUser("USAGE:.notify ON/OFF",line[2])

def notifymanage(user,state):
    c=getC()
    conn=getConn()
    if(userExists==False):
        try:
            c.execute("INSERT INTO users(user,state) VALUES((?),(?))",(user,state))
            conn.commit()
            printUser("User has been added",line[2])
        except:
            printUser("error has occured!!!",line[2])
    else:
        try:
            c.execute("UPDATE users SET state = (?) WHERE user = (?)",(state,user))
            conn.commit()
            if(state.upper()=="ON"):
                printUser("notifications have been turned on",line[2])
            else:
                printUser("notifications have been turned off",line[2])
        except:
            printUser("Error has occured!!!",line[2])
