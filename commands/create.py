import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def startcreatecmd(line,connection, c):
    if(len(line)>5):
        if(filter_msg(line[4])==False and filter_msg(" ".join(line[5:]))==False):
            create(c,connection,line[4],line[5:])
        else:
            sendBannedMessage()
    else:
        printChan("Please enter CTF and challenge name")

def create(c,conn,CTF,challenge,fromCmd=True):
    try:
        if(fromCmd):
            challenge=" ".join(challenge)
        print(list(CTF))
        c.execute("INSERT INTO challenges(title,ctfID) VALUES((?),(SELECT ctfID FROM ctf WHERE name=(?)))",(challenge,CTF))
        conn.commit()
        printChan("added challenge %s to %s" % (challenge , CTF))
    except:
        printChan("CTF doesnt exist , if you are certain it does spam NETWORKsecurity")
