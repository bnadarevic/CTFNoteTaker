import sys
import re
import os
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *
from datetime import datetime

def adminExportCTF(user,line):
    if(len(line) > 5):
        if(filter_msg(line[4])==False and filter_msg(line[5])==False):
            if(is_directory_traversal(line[5])):
                sendBannedMessage(user)
                printMaster(user + " attempted Directory Traversal.")
                return False
            exportCTF(line[4],user,line[5])
            return True
        else:
            sendBannedMessage(user)
            return False
    else:
        if(len(line) > 4):
            if(filter_msg(line[4])==False):
                exportCTF(line[4],user)
                return True
            else:
                sendBannedMessage(user)
                return False
        else:
            printUser("Please enter a CTF name to export",user)
#Need to add Useful print messages here.
def exportCTF(CTF,user,filename=""):
    if(filename==""):
        time = str(datetime.now()).split(".")[0].replace(" ","_")
        filename = CTF+"_"+time

    filepath = "exports/" + filename + ".exp"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    ctfID = getCTFIDByName(CTF)
    c = getC()
    conn = getConn()
    with open(filepath, "w") as f:
        f.write("CTF:"+CTF + '\n')
        c.execute("SELECT challengeID,title FROM challenges WHERE ctfID = (?);",(ctfID,))
        challenges = c.fetchall()
        for challenge in challenges:
            f.write("CHAL:"+challenge[1]+"\n")
            c.execute("SELECT contributor,note FROM note WHERE challengeID = (?);",(challenge[0],))
            notes = c.fetchall()
            for note in notes:
                f.write("NOTE:"+note[0]+","+note[1]+"\n")
    printUser("CTF " + CTF + " exported with name " + filename,user)
