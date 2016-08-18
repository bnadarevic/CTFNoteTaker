import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def deleteCTFCMD(s,c,conn,user,line):
    if(len(line) > 4):
        if(filter_msg(line[4],s)==False):
            startnew(line[4],s,conn,c)
            return True
        else:
            s.send(getBannedMessageBytes())
            return False
    else:
        s.send(bytes("PRIVMSG %s :Please enter a CTF name to delete.\r\n" % CHAN,"UTF-8"))

def startnew(CTF,s,conn,c):
    try:
        c.execute("DELETE FROM ctf WHERE name = "+CTF+";")
        conn.commit()
        s.send(bytes("PRIVMSG %s :%s deleted\r\n" % (CHAN,CTF),"UTF-8"))
    except sqlite3.IntegrityError:
        s.send(bytes("PRIVMSG %s :%s already exists\r\n" % (CHAN,CTF),"UTF-8"))
