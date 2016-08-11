#!/usr/bin/env python3

# modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import sys
import os
import re
import socket
import string
import sqlite3
import traceback
from Utilities.StringUtils import *
from Utilities.conf import *
from commandParser import *
from adminCommandParser import *

def handle():
    print("GETTING BUFFER\n")
    global readbuffer
    ircmsg=s.recv(1024)
    readbuffer = readbuffer+ircmsg.decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop()
    for line in temp:
        print(line)
        line = str.rstrip(line)
        line = str.split(line)#Space delimitted by default.
        if(line[0] == "PING"):
            pingpong(line[1])
        elif(line[1]=="PRIVMSG"):
            cmd=line[3]
            cmd=cmd[1:]
            user=(line[0])[1:line[0].index("!")]
            if(cmd.startswith(COMMANDPREFIX)):
                cmdParser(s,c,conn,user,line,cmd[len(COMMANDPREFIX):])
            elif(cmd.startswith(ADMINCOMMANDPREFIX)):
                adminCmdParser(s,c,conn,user,line,cmd[len(ADMINCOMMANDPREFIX):])


def is_first_run():
    firstRunFile = open("firstRun.conf","r")
    data=firstRunFile.read()
    data=data.rstrip()
    if(data=="yes" or data=="" or (not os.path.isfile("firstRun.conf"))):
        c.execute("CREATE TABLE ctf(ctfID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL)")
        c.execute("CREATE TABLE challenges(challengeID INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,problemtext TEXT,ctfID INT NOT NULL,FOREIGN KEY(ctfID) REFERENCES ctf(ctfID)ON DELETE CASCADE)")
        c.execute("CREATE TABLE note(noteID INTEGER PRIMARY KEY AUTOINCREMENT,contributor TEXT NOT NULL,note TEXT NOT NULL,challengeID INT NOT NULL,FOREIGN KEY(challengeID) REFERENCES challenge(challengeID)ON DELETE CASCADE)")
        conn.commit()
        firstRunFile.close()
        firstRunFile = open("firstRun.conf","w+")
        firstRunFile.write("no")
        firstRunFile.close()
        return True
    else:
        return False

def pingpong(pong):
    s.send(bytes("PONG %s\r\n" % pong,"UTF-8"))
    print("PONG\n")

sqlite_file = "database.sqlite"
conn = sqlite3.connect(sqlite_file)
c=conn.cursor()
if(is_first_run()):
    c.close()
    conn.close()
    conn = sqlite3.connect(sqlite_file)
    c=conn.cursor()

readbuffer=""

s=socket.socket()
s.connect((HOST, PORT))
handle()
s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s Wolf :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
handle()
s.send(bytes("JOIN %s\r\n" % CHAN,"UTF-8"))
s.send(bytes("PRIVMSG %s :Hello Master\r\n" % MASTER, "UTF-8"))

while(1):
    try:
        handle()
    except:
        print("BZZZZZZZZZZZZZZZTTTTT *******    ERROR   *** " + str(traceback.format_exc()))
        if("Keyboard" in str(sys.exc_info()[0])):
            printChan(s, NICK + " is shutting down.")
            break
        printChan(s,"An internal error occured!")
        printUser(s,"Error " + str(sys.exc_info()[0]),MASTER)
