import sys
import re
import os
import os.path
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *

def adminImportCTF(user,line):
    if(len(line) > 4):
        if(filter_msg(line[4])==False):
            if(is_directory_traversal(line[4])):
                sendBannedMessage(user)
                printMaster(user + " attempted Directory Traversal.")
                return False
            importCTF(user,line[4])
            return True
        else:
            sendBannedMessage(user)
            return False
    else:
        printUser("Please enter filename to import ")

#Need to add Useful print messages here.
def importCTF(user,filename):
    filepath = "exports/" + filename + ".exp"
    os.path.isfile(filepath)
    c = getC()
    conn = getConn()
    CTFsAdded = 0
    with open(filepath, "r") as f:
        ctfID = -1
        chalID = -1
        for line in f:
            if(line.startswith("CTF:")):
                CTF = line[4:-1]
                if(not CTFExists(CTF)):
                    c.execute("INSERT INTO ctf(name) VALUES((?))",(CTF,))
                    conn.commit()
                    ctfID = getCTFIDByName(CTF)
                    CTFsAdded+=1
                else:
                    printUser("CTF " + CTF + " already exists, aborting importing this CTF.",user)
                    ctfID = -1
            if(line.startswith("CHAL:")):
                if(ctfID > -1):
                    chal = line[5:-1]
                    c.execute("INSERT INTO challenges(title,ctfID) VALUES((?),(?));",(chal,ctfID))
                    conn.commit()
                    chalID = getChalID("",chal,ctfID)
            if(line.startswith("NOTE:")):
                if(ctfID > -1):
                    note = line[5:-1]
                    noteArr = note.split(",")
                    c.execute("INSERT INTO note (contributor,note,challengeID) VALUES((?),(?),(?))",(noteArr[0],noteArr[1],chalID))
                    conn.commit()

    if(CTFsAdded > 0):
        printUser(str(CTFsAdded) + " CTF's have been added.",user)
        printUser( filename + " has been imported",user)
    else:
        printUser("No CTF's have been imported",user)
