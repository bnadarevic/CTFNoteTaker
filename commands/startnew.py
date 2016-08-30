import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *

#lines, usr, socket
def startnewcmd(line,user):
    if(len(line) > 4):
        if(filter_msg(line[4])==False):
            startnew(line[4].strip(),user)
            return True
        else:
            sendBannedMessage()
            return False
    else:
        printUser("Please enter a CTF name",user)

def startnew(CTF,user):
    try:
        c = getC()
        conn = getConn()
        if(not CTFExists(CTF)):
            c.execute("INSERT INTO ctf(name) VALUES((?))",(CTF,))
            conn.commit()
            printUser(CTF+" created!",user)
        else:
            printUser(CTF+" already Exists!",user)
    except sqlite3.IntegrityError:
        printUser(CTF+" already exists.",user)
