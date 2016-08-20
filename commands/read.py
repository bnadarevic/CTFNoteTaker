import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *

def startreadcmd(user,line):
    verbose = False
    if(len(line) > 4):
        if(line[4].startswith("-v") or line[4].startswith("verbose")):
            verbose = True
            del line[4]
    if(len(line)>5):
        read_note(line[4]," ".join(line[5:]),verbose)
    else:
        printChan("Please enter CTF and challenge.")
def read_note(CTF,challenge,verbose=False):
    c = getC()
    selectquery = "contributor,note"
    if(not CTFExists(CTF)):
        printChan("CTF Doesn't Exist")
        return
    if(not ChalExists(CTF,challenge)):
        printChan("Challenge Doesn't exist")
        return
    chalID = getChalID(CTF,challenge)
    if(verbose):
        selectquery = "noteID," + selectquery
    c.execute("SELECT " + selectquery + " FROM note WHERE challengeID=(?)" , (chalID,))
    rows=c.fetchall()
    if(len(rows) > 0):
        pretty_format_output(rows)
    else:
        #In future have it detect if valid chal name was given.
        printChan("This challenge has no notes. Go work on it ;)")
