import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.formatoutput import *

def list_chals(line ,socket ,c):
    if(len(line)>4):
        #"SELECT title FROM challenge, ctf WHERE ctf.ctfID = challenge.ctfID and ctf.name = (?);
        CTF=line[4:]
        CTF=CTF[0]
        print(CTF)
        c.execute("SELECT title FROM challenges WHERE ctfID=(SELECT ctfID FROM ctf WHERE name=(?))",(CTF,))
        rows=c.fetchall()
        format_output(socket,rows)
    else:
        s.send(bytes("PRIVMSG %s :Please enter CTF name.\r\n" %CHAN ,"UTF-8"))
