#!/usr/bin/env python3

# modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import sys
import re
import socket
import string
import sqlite3
import traceback
import Utilities.connections
from Utilities.StringUtils import *
from Utilities.conf import *
from commandParser import *
from adminCommandParser import *

def handle():
    print("GETTING BUFFER\n")
    global readbuffer
    ircmsg=Utilities.connections.s.recv(RECVBLOCKSIZE)
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
                cmdParser(user,line,cmd[len(COMMANDPREFIX):])
            elif(cmd.startswith(ADMINCOMMANDPREFIX)):
                adminCmdParser(user,line,cmd[len(ADMINCOMMANDPREFIX):])

def pingpong(pong):
    Utilities.connections.s.send(bytes("PONG %s\r\n" % pong,"UTF-8"))
    print("PONG\n")

readbuffer=""
Utilities.connections.init()
Utilities.connections.s.connect((HOST, PORT))
handle()
printBytes(bytes("NICK %s\r\n" % NICK, "UTF-8"))
printBytes(bytes("USER %s %s Wolf :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
handle()
printBytes(bytes("JOIN %s\r\n" % CHAN,"UTF-8"))
handle()
printMaster("Hello Master")

while(1):
    try:
        handle()
    except:
        if("Keyboard" in str(sys.exc_info()[0])):
            printChan(NICK + " is shutting down.")
            closeSocket()
            break
        print("BZZZZZZZZZZZZZZZTTTTT *******    ERROR   *** " + str(traceback.format_exc()))
        printChan("An internal error occured!")
        printMaster("Error " + str(traceback.format_exc()))
