import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def adminDeleteCTF(s,c,conn,user,line):
    if(len(line) > 4):
        if(filter_msg(line[4],s)==False):
            deleteCTF(line[4],s,conn,c)
            return True
        else:
            s.send(getBannedMessageBytes())
            return False
    else:
        printChan("Please enter a CTF name to delete.")
#Need to add Useful print messages here.
def deleteCTF(CTF,s,conn,c):
    printChan(s,CTF)
    try:
        c.execute("SELECT \"ctfID\" FROM ctf where name = \'"+CTF+"\';")
        ctfID = str((c.fetchone()))[1:-2]

        c.execute("SELECT challengeID FROM challenges WHERE ctfID = "+ctfID+";")
        for row in c.fetchall():
            rowString = (str(row))[1:-2]
            c.execute("DELETE FROM note WHERE challengeID = "+rowString+";")

        c.execute("DELETE FROM challenges WHERE ctfID = "+ctfID+";")

        c.execute("DELETE FROM ctf WHERE name = \'"+CTF+"\';")

        conn.commit()
        s.send(bytes("PRIVMSG %s :%s deleted, and all its corresponding challenges and notes.\r\n" % (CHAN,CTF),"UTF-8"))
    except sqlite3.IntegrityError:
        s.send(bytes("PRIVMSG %s :%s Strange error in deleting CTF\r\n" % (CHAN,CTF),"UTF-8"))
