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
            printChan("parameters are ON or OFF")
    else:
        printChan("USAGE:.notify ON/OFF")
        
def notifymanage(user,state):
    c=getC()
    conn=getConn()
    if(userExists==False):
        try:
            c.execute("INSERT INTO users(user,state) VALUES((?),(?))",(user,state))
            conn.commit()
            printChan("User has been added")
        except:
            printChan("error has occured!!!")
    else:
        try:
            c.execute("UPDATE users SET state = (?) WHERE user = (?)",(state,user))
            conn.commit()
            if(state.upper()=="ON"):
                printChan("notifications have been turned on")
            else:
                printChan("notifications have been turned off")
        except:
            printChan("Error has occured!!!")
            
                
                
        
        
        
        