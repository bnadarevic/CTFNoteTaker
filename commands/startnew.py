import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

#lines, usr, socket
def startnewcmd(line,user,socket,connection, c):
    if(len(line) > 4):
        if(filter_msg(line[4],socket)==False):
            startnew(line[4],socket,connection,c)
            return True
        else:
            socket.send(getBannedMessageBytes())
            return False
    else:
        socket.send(bytes("PRIVMSG %s :Please enter a CTF name after.\r\n" % CHAN,"UTF-8"))

def startnew(CTF,s,conn,c):
    try:
        c.execute("INSERT INTO ctf(name) VALUES((?))",(CTF,))
        conn.commit()
        s.send(bytes("PRIVMSG %s :%s created\r\n" % (CHAN,CTF),"UTF-8"))
    except sqlite3.IntegrityError:
        s.send(bytes("PRIVMSG %s :%s already exists\r\n" % (CHAN,CTF),"UTF-8"))
