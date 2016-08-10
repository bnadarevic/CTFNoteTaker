import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def startaddcmd(s,c,conn,user,line):
    if(len(line)>6):
        
        CTF=line[4]
        pattern=re.compile("note:(.*)")
        pattern2=re.compile("(.*?)note:")
        note=re.findall(pattern," ".join(line[5:]))
        note=" ".join(note)
        if(note==""):
            s.send(bytes("PRIVMSG %s :prefix your note with note:\r\n" % CHAN,"UTF-8"))
            return
            
        challenge=re.findall(pattern2," ".join(line[5:]))
        challenge=" ".join(challenge)
        if(filter_msg(note,s)==False):
            if(filter_msg(user,s)==False): #if we plan to print users
                add_note(CTF,challenge,user,note,c,conn,s)
        else:
            s.send(getBannedMessageBytes())
    else:
        s.send(bytes("PRIVMSG %s :Please enter CTF , challenge and prefix your note with note:\r\n" % CHAN,"UTF-8"))
def add_note(CTF,challenge,contributor,comment,c,conn,s):
    print(CTF+"\n"+challenge+"\n"+contributor+"\n"+comment+"\n")
    challenge=challenge.rstrip() #trailing whitespace bug fix
    try:
        c.execute("INSERT INTO note (contributor,note,challengeID) VALUES((?),(?),(SELECT challengeID FROM challenges WHERE title=(?) AND ctfID=(SELECT ctfID FROM ctf WHERE name=(?))))",(contributor,comment,challenge,CTF))
        conn.commit()
        s.send(bytes("PRIVMSG %s :Note added\r\n" % CHAN,"UTF-8"))
    except:
        s.send(bytes("PRIVMSG %s :Error: CTF or challenge doesnt exist(at least I hope thats error and that nsm didnt completly screw me up)\r\n","UTF-8"))
        #its going to be ok

                    