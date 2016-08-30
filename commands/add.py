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
    print(line)
    if(len(line)>6):

        CTF=line[4]
        pattern=re.compile("note:(.*)")
        pattern2=re.compile("(.*?)note:")
        note=re.findall(pattern," ".join(line[5:]))
        note=" ".join(note)
        if(note==""):
            printUser("prefix your note with note:",user)
            return

        challenge=re.findall(pattern2," ".join(line[5:]))
        challenge=" ".join(challenge)
        if(filter_msg(note)==False):
            if(filter_msg(user)==False): #if we plan to print users
                add_note(user,CTF,challenge,getUser(line),note)
        else:
            sendBannedMessage()
    else:
        printUser("Please enter CTF , challenge and prefix your note with note:",line[2])

def startaddcmdparams(user,line):
    potentialline=formatLineToMethodStyle(line)
    contributor = getUser(line)
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

    add_note(user,line[0],line[1],contributor,line[2])

def add_note(printingUser,CTF,challenge,contributor,comment,firstRun=True):
    c = getC()
    conn = getConn()
    print(CTF+"\n"+challenge+"\n"+contributor+"\n"+comment+"\n")
    challenge=challenge.strip() #trailing whitespace bug fix
    if(not CTFExists(CTF)):
        printUser("CTF Does not exist",printingUser)
        return
    if(ChalExists(CTF,challenge)):
        ctfID = getCTFIDByName(CTF)
        chalID = getChalID(CTF,challenge,ctfID)
        c.execute("INSERT INTO note (contributor,note,challengeID) VALUES((?),(?),(?))",(contributor,comment,chalID))
        conn.commit()
        printUser("Note added",printingUser)
    else:
        if(firstRun):
            create(CTF,challenge, printingUser, False)
            add_note(printingUser,CTF,challenge,contributor,comment,False)
        else:
            printUser("Strange error occured, notify NETWORKSecurity or Valar_Dragon with the command used.")
