import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def startcreatecmd(s,line,connection, c):
    if(len(line)>5):
        if(filter_msg(line[4],s)==False and filter_msg(" ".join(line[5:]),s)==False):
            create(line[4],line[5:])
        else:
            s.send(bytes("PRIVMSG %s:Please enter CTF and challenge name\r\n" %CHAN,"UTF-8"))
    else:
        s.send(getBannedMessageBytes())
	
	
	
	
def create(CTF,challenge):
    try:
        challenge=" ".join(challenge)
        c.execute("INSERT INTO challenges(title,ctfID) VALUES((?),(SELECT ctfID FROM ctf WHERE name=(?)))",(challenge,CTF))
        conn.commit()
        s.send(bytes("PRIVMSG %s :added challenge %s to %s\r\n" % (CHAN , challenge , CTF),"UTF-8"))
    except:
        s.send(bytes("PRIVMSG %s :CTF doesnt exist , if you are certain it does spam NETWORKsecurity\r\n" % CHAN,"UTF-8"))