import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.create import *
from itertools import islice

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

def startaddcmdparams(s,c,conn,user,line):
    line = formatLineToMethodStyle(line)
    #Now I need to resplit by , and ignore \,
    printChan(s,line)
    for line2 in line:
        if(filter_msg(line2,s)==True):
            s.send(getBannedMessageBytes())
            return
    if(filter_msg(user,s)):
        s.send(getBannedMessageBytes())
        return
    if(len(line) > 3):
        note = line[2]
        for i in islice(line, 3, None):
            note += ", " + i
        line[2] = note

    add_note(line[0],line[1],user,line[2],c,conn,s)

def add_note(CTF,challenge,contributor,comment,c,conn,s,firstRun=True):
    print(CTF+"\n"+challenge+"\n"+contributor+"\n"+comment+"\n")
    challenge=challenge.strip() #trailing whitespace bug fix
    try:
        c.execute("INSERT INTO note (contributor,note,challengeID) VALUES((?),(?),(SELECT challengeID FROM challenges WHERE title=(?) AND ctfID=(SELECT ctfID FROM ctf WHERE name=(?))))",(contributor,comment,challenge,CTF))
        conn.commit()
        s.send(bytes("PRIVMSG %s :Note added\r\n" % CHAN,"UTF-8"))
    except:
        if(firstRun):
            create(s,c,conn,CTF,challenge,False)
            add_note(CTF,challenge,contributor,comment,c,conn,s,False)
