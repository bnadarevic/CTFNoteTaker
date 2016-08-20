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
        printChan("Please enter a CTF name")

def startnew(CTF):
    try:
        c = getC()
        conn = getConn()
        if(not CTFExists(CTF)):
            c.execute("INSERT INTO ctf(name) VALUES((?))",(CTF,))
            conn.commit()
            printChan(CTF+" created!")
        else:
            printChan(CTF+" already Exists!")
    except sqlite3.IntegrityError:
        printChan(CTF+" already exists.")
