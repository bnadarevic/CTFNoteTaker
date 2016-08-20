import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *

def adminDeleteCTF(user,line):
    if(len(line) > 4):
        if(line[4].startswith("-v") or line[4].startswith("verbose")):
            if(len(line)>5):
                if(filter_msg(line[5])==False):
                    deleteCTF(line[5],user,True)
                    return True
                else:
                    sendBannedMessage()
                    return False
            else:
                printUser("Please enter a CTF name to delete",user)
        else:
            if(filter_msg(line[4])==False):
                deleteCTF(line[4],user)
                return True
            else:
                sendBannedMessage()
                return False
    else:
        printUser("Please enter a CTF name to delete",user)
#Need to add Useful print messages here.
def deleteCTF(CTF,user,verbose=False):
    try:
        c = getC()
        conn = getConn()
        c.execute("SELECT \"ctfID\" FROM ctf where name = (?);",(CTF,))
        ctfID = getCTFIDByName(CTF)

        c.execute("SELECT challengeID FROM challenges WHERE ctfID = (?);",(ctfID,))
        rows = c.fetchall()
        for row in rows:
            #row is in form (<number>,)
            rowString = (str(row))[1:-2]
            title = ""
            if(verbose):
                c.execute("SELECT title FROM challenges WHERE challengeID = "+rowString+";")
                #We need a format method for c.fetchone() for multiple columns 1 row.
                title = str(c.fetchone())[2:-3]
                printUser("Deleting the following notes from challenge " + title + ": ",user)
                c.execute("SELECT contributor,note FROM note WHERE challengeID = "+rowString+";")
                format_output_multirow(c.fetchall(),user)

            c.execute("DELETE FROM note WHERE challengeID = "+rowString+";")
            if(verbose):
                printUser("Notes deleted for challenge " + (title[2:-3]),user)

        c.execute("DELETE FROM challenges WHERE ctfID = (?);",(ctfID,))

        c.execute("DELETE FROM ctf WHERE ctfID = (?);",(ctfID,))

        conn.commit()
        printUser("deleted " + CTF + ", along with all of its corresponding challenges and notes.",user)
    except sqlite3.IntegrityError:
        printUser("Strange error in deleting CTF", user)
