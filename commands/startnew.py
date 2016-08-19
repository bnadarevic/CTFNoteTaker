import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

#lines, usr, socket
def startnewcmd(line,user,connection, c):
    if(len(line) > 4):
        if(filter_msg(line[4])==False):
            startnew(line[4],connection,c)
            return True
        else:
            sendBannedMessage()
            return False
    else:
        printChan("Please enter a CTF name after.")

def startnew(CTF,conn,c):
    try:
        c.execute("INSERT INTO ctf(name) VALUES((?))",(CTF,))
        conn.commit()
        printChan(CTF+" created!")
    except sqlite3.IntegrityError:
        printChan(CTF+" already exists.")
