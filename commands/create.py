import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *

def startcreatecmd(line):
    if(len(line)>5):
        if(filter_msg(line[4])==False and filter_msg(" ".join(line[5:]))==False):
            create(line[4],line[5:])
        else:
            sendBannedMessage()
    else:
        printUser("Please enter CTF and challenge name",line[2])

def create(CTF,challenge,fromCmd=True):
    try:
        c = getC()
        conn = getConn()
        if(fromCmd):
            challenge=" ".join(challenge)
        print(list(CTF))
        if(not ChalExists(CTF,challenge)):
            c.execute("INSERT INTO challenges(title,ctfID) VALUES((?),(?));",(challenge,getCTFIDByName(CTF)))
            conn.commit()
            printUser("added challenge %s to %s" % (challenge , CTF),line[2])
        else:
            printUser("Challenge already exists",line[2])
    except:
        printUser("CTF doesnt exist , if you are certain it does spam bot operator",line[2])
