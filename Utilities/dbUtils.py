#!/usr/bin/env python3

import sqlite3
import Utilities.connections
from Utilities.conf import *
from Utilities.StringUtils import *

#get Cursor
def getC():
    return Utilities.connections.c

def getConn():
    return Utilities.connections.conn

def getCTFIDByName(CTFName):
    Utilities.connections.c.execute("SELECT ctfID FROM ctf WHERE lower(name)=(?);",(CTFName.lower(),))
    return Utilities.connections.c.fetchone()[0]

def CTFExists(CTFName):
    Utilities.connections.c.execute("SELECT count(*) FROM ctf WHERE lower(name)=(?);",(CTFName.lower(),))
    count = Utilities.connections.c.fetchone()[0]
    if(count == 0):
        return False
    else:
        return True

def getChalID(CTF,chal,ctfID = None):
    if(ctfID is None):
        ctfID = getCTFIDByName(CTF)
    Utilities.connections.c.execute("SELECT challengeID FROM challenges WHERE lower(title)=(?) AND ctfID=(?);" , (str(chal.lower()),ctfID))
    return Utilities.connections.c.fetchone()[0]

def ChalExists(CTFName,chal):
    ctfID = getCTFIDByName(CTFName)
    Utilities.connections.c.execute("SELECT count(*) FROM challenges WHERE ctfID=(?) AND lower(title)=(?);",(ctfID,str(chal.lower())))
    count = Utilities.connections.c.fetchone()[0]
    if(count == 0):
        return False
    else:
        return True

def noteExists(noteID):
    Utilities.connections.c.execute("SELECT count(*) FROM note WHERE noteID=(?);",(noteID,))
    count = Utilities.connections.c.fetchone()[0]
    if(count == 0):
        return False
    else:
        return True
