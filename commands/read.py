import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.formatoutput import *

def startreadcmd(user,c,line):
    verbose = False
    if(len(line) > 4):
        if(line[4].startswith("-v") or line[4].startswith("verbose")):
            verbose = True
            del line[4]
    if(len(line)>5):
        read_note(c,line[4]," ".join(line[5:]),verbose)
    else:
        printChan("Please enter CTF and challenge.")
def read_note(c,CTF,challenge,verbose=False):
    selectquery = "contributor,note"
    if(verbose):
        selectquery = "noteID," + selectquery
    c.execute("SELECT " + selectquery + " FROM note WHERE challengeID=(SELECT challengeID FROM challenges WHERE title=(?) AND ctfID=(SELECT ctfID from ctf WHERE name=(?)))" , (challenge,CTF))
    rows=c.fetchall()
    pretty_format_output(rows)
