import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *

def adminDeleteChal(user,line):
    verbose = False
    if("-v" in line):
        del line[line.index('-v')]
        verbose = True
    if("verbose" in line):
        del line[line.index('verbose')]
        verbose = True
    if(len(line) > 5):
        if(filter_msg(line[4]) == False and filter_msg(line[5]) == False):
            if(ChalExists(line[4],line[5])):
                deleteChal(line[4],line[5],user,verbose)
            else:
                printUser("Challenge does not exist.")
        else:
            sendBannedMessage(user)
    else:
        printUser("Missing parameters",user)
#Need to add Useful print messages here.
def deleteChal(CTF,challenge,user,verbose=False):
    try:
        c = getC()
        conn = getConn()
        chalID = getChalID(CTF,challenge)
        if(verbose):
            #We need a better format method for c.fetchone() for multiple columns 1 row.
            printUser("Deleting the following notes: ")
            c.execute("SELECT contributor,note FROM note WHERE challengeID = (?);",(chalID,))
            format_output_multirow(c.fetchall(),user)

        c.execute("DELETE FROM note WHERE challengeID = (?);",(chalID,))
        c.execute("DELETE FROM challenges WHERE challengeID = (?);",(chalID,))

        conn.commit()
        printUser("deleted challenge: " + challenge + " from CTF " + CTF + ", along with all of its notes.",user)
    except sqlite3.IntegrityError:
        printUser("Strange error in deleting challenge", user)
        printMaster("Error " + str(traceback.format_exc()))
