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
            startnew(line[4].strip())
            return True
        else:
            sendBannedMessage()
            return False
    else:
        printUser("Please enter a CTF name",line[2])

def startnew(CTF):
    try:
        c = getC()
        conn = getConn()
        if(not CTFExists(CTF)):
            c.execute("INSERT INTO ctf(name) VALUES((?))",(CTF,))
            conn.commit()
            printUser(CTF+" created!",line[2])
        else:
            printUser(CTF+" already Exists!",line[2])
    except sqlite3.IntegrityError:
        printUser(CTF+" already exists.",line[2])
