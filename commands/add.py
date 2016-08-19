import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.create import *
from itertools import islice

def startaddcmd(user,line):
    if(len(line)>6):

        CTF=line[4]
        pattern=re.compile("note:(.*)")
        pattern2=re.compile("(.*?)note:")
        note=re.findall(pattern," ".join(line[5:]))
        note=" ".join(note)
        if(note==""):
            sendChan("prefix your note with note:")
            return

        challenge=re.findall(pattern2," ".join(line[5:]))
        challenge=" ".join(challenge)
        if(filter_msg(note)==False):
            if(filter_msg(user)==False): #if we plan to print users
                add_note(CTF,challenge,user,note)
        else:
            sendBannedMessage()
    else:
        printChan("Please enter CTF , challenge and prefix your note with note:")

def startaddcmdparams(user,line):
    potentialline=formatLineToMethodStyle(line)
    if(potentialline!=False):
        line=potentialline
    else:
        return
    #Now I need to resplit by , and ignore \,
    for line2 in line:
        if(filter_msg(line2)==True):
            sendBannedMessage()
            return
    if(filter_msg(user)):
        sendBannedMessage()
        return
    if(len(line) > 3):
        note = line[2]
        for i in islice(line, 3, None):
            note += ", " + i
        line[2] = note

    add_note(line[0],line[1],user,line[2])

def add_note(CTF,challenge,contributor,comment,firstRun=True):
    c = getC()
    conn = getConn()
    print(CTF+"\n"+challenge+"\n"+contributor+"\n"+comment+"\n")
    challenge=challenge.strip() #trailing whitespace bug fix
    try:
        c.execute("INSERT INTO note (contributor,note,challengeID) VALUES((?),(?),(SELECT challengeID FROM challenges WHERE title=(?) AND ctfID=(SELECT ctfID FROM ctf WHERE name=(?))))",(contributor,comment,challenge,CTF))
        conn.commit()
        printChan("Note added")
    except:
        if(firstRun):
            create(CTF,challenge,False)
            add_note(CTF,challenge,contributor,comment,False)
