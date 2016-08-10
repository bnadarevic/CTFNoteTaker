import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.formatoutput import *

def startreadcmd(user,s,c,line):
    if(len(line)>5):
        read_note(s,c,line[4]," ".join(line[5:]))
    else:
        s.send(bytes("PRIVMSG %s :Please enter CTF and challenge.\r\n" %CHAN,"UTF-8"))
def read_note(s,c,CTF,challenge):
    c.execute("SELECT note FROM note WHERE challengeID=(SELECT challengeID FROM challenges WHERE title=(?) AND ctfID=(SELECT ctfID from ctf WHERE name=(?)))" , (challenge,CTF))
    rows=c.fetchall()
    format_output(rows,s)
        
        