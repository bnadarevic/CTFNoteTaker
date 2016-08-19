import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.formatoutput import *
from Utilities.dbUtils import *

def list_chals(line):
    if(len(line)>4):
        c = getC()
        #"SELECT title FROM challenge, ctf WHERE ctf.ctfID = challenge.ctfID and ctf.name = (?);
        CTF=line[4:]
        CTF=CTF[0]
        print(CTF)
        c.execute("SELECT title FROM challenges WHERE ctfID=(SELECT ctfID FROM ctf WHERE name=(?));",(CTF,))
        rows=c.fetchall()
        if(len(rows) > 1):
            format_output(rows)
        else:
            printChan("Enter a valid CTF name.")
    else:
        printChan("Please enter CTF name.")
