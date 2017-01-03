import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *

#printuser is print location
#user is user you store in db

def startnotifycmd(printuser,user,line):

    if(len(line)>4):
        state=line[4]
        if(state.upper()=="ON" or state.upper()=="OFF"):

            notifymanage(printuser,user,state)
        else:
            printUser("parameters are ON or OFF",printuser)
    else:
        printUser("USAGE:.notify ON/OFF",printuser)

def notifymanage(printuser,user,state):

    c=getC()
    conn=getConn()
    if(userExists(user)==False):
        try:
            c.execute("INSERT INTO users(user,state) VALUES((?),(?))",(user,state))
            conn.commit()
            printUser("User has been added",printuser)
        except:
            printUser("error has occured!!!",printuser)
    else:
        try:
            c.execute("UPDATE users SET state = (?) WHERE user = (?)",(state,user))
            conn.commit()
            if(state.upper()=="ON"):
                printUser("notifications have been turned on for {}".format(user),printuser)
            else:
                printUser("notifications have been turned off for {}".format(user),printuser)
        except:
            printUser("Error has occured!!!",user)
def notifylog(user,logoutTime):

    logging.getLogger("CTFNoteTaker.commands.notify.leave").info(user + " logged out")
    c=getC()
    conn=getConn()

    if(userExists(user)==False):
        return
    else:

        c.execute("SELECT state FROM users WHERE user=(?)",(user,))
        state=c.fetchone()[0]
        if(state.upper()=="ON"):
            c.execute("UPDATE users SET lastLogout=(?) WHERE user=(?)",(logoutTime,user))
            conn.commit()

        else:
            return

def notifyjoin(user):
    logging.getLogger("CTFNoteTaker.commands.notify.join").info(user + " logged in")
    c=getC()
    if(userExists(user)==False):
        return

    else:
        c.execute("SELECT state FROM users WHERE user=(?)",(user,))
        state=c.fetchone()[0]
        if(state.upper()=="OFF"):
            return
        else:
            c.execute("SELECT name,title,contributor,note FROM note INNER JOIN challenges ON note.challengeID = challenges.challengeID INNER JOIN ctf ON ctf.ctfID = challenges.ctfID WHERE timestamp>(SELECT lastLogout FROM users WHERE user=(?))",(user,))
            rows=c.fetchall()
            pretty_format_output(rows,user)
