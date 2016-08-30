import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *

def startcreatecmd(user,line):
    if(len(line)>5):
        if(filter_msg(line[4])==False and filter_msg(" ".join(line[5:]))==False):
            create(line[4],line[5:],user)
        else:
            sendBannedMessage()
    else:
        printUser("Please enter CTF and challenge name",user)

def create(CTF,challenge,user,fromCmd=True):
    try:
        c = getC()
        conn = getConn()
        if(fromCmd):
            challenge=" ".join(challenge)
        print(list(CTF))
        if(not ChalExists(CTF,challenge)):
            c.execute("INSERT INTO challenges(title,ctfID) VALUES((?),(?));",(challenge,getCTFIDByName(CTF)))
            conn.commit()
            printUser("added challenge %s to %s" % (challenge , CTF),user)
        else:
            printUser("Challenge already exists",user)
    except:
        printUser("CTF doesnt exist , if you are certain it does spam bot operator",user)
