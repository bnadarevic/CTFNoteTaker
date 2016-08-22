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
    verbose = False
    if("-v" in line):
        del line[line.index('-v')]
        verbose = True
    if("verbose" in line):
        del line[line.index('verbose')]
        verbose = True
    if(len(line) > 4):
        if(filter_msg(line[4])==False):
            deleteCTF(line[4],user,verbose)
            return True
        else:
            sendBannedMessage(user)
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
                c.execute("SELECT title FROM challenges WHERE challengeID =(?)", (rowstring,))
                #We need a format method for c.fetchone() for multiple columns 1 row.
                title = str(c.fetchone())[2:-3]
                printUser("Deleting the following notes from challenge " + title + ": ",user)
                c.execute("SELECT contributor,note FROM note WHERE challengeID = (?)",(rowstring,))
                format_output_multirow(c.fetchall(),user)

            c.execute("DELETE FROM note WHERE challengeID = (?) ",(rowstring,))

        c.execute("DELETE FROM challenges WHERE ctfID = (?);",(ctfID,))

        c.execute("DELETE FROM ctf WHERE ctfID = (?);",(ctfID,))

        conn.commit()
        printUser("deleted " + CTF + ", along with all of its corresponding challenges and notes.",user)
        printMaster(user + " deleted CTF: " + CTF + ", along with all of its corresponding challenges and notes.")
    except sqlite3.IntegrityError:
        printUser("Strange error in deleting CTF", user)
        printMaster("Error " + str(traceback.format_exc()))
