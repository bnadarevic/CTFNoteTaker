#!/usr/bin/env python3

# modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import sys
import re
import socket
import string
import sqlite3
import logging
import traceback
import time
import Utilities.connections
from Utilities.StringUtils import *
from Utilities.conf import *
from Utilities.loggingUtils import *
from commandParser import *
from adminCommandParser import *

def handle(logLine = False):
    print("GETTING BUFFER\n")
    global readbuffer
    ircmsg=Utilities.connections.s.recv(RECVBLOCKSIZE)
    readbuffer = readbuffer+ircmsg.decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop()
    for line in temp:
        #print(line)
        line = str.rstrip(line)
        line = str.split(line)#Space delimitted by default.
        if(logLine or (LOGGING.lower() == "off")):
            #Perhaps make a formatter for these.
            logger.debug(line)
            print(line)
        if(line[0] == "PING"):
            pingpong(line[1])
        if(line[1]=="QUIT" or line[1]=="PART"):
            
            
            logoutTime=int(time.time())
            notifylog(getUser(line),logoutTime)
            
        if(line[1]=="JOIN"):
            user=getUser(line) 
            notifyjoin(user)
            
            
        elif(line[1]=="PRIVMSG"):
            cmd=line[3]
            cmd=cmd[1:]
            user=getUser(line)
            if(cmd.startswith(COMMANDPREFIX)):
                logger.info(str(line))
                cmdParser(user,line,cmd[len(COMMANDPREFIX):])
            elif(cmd.startswith(ADMINCOMMANDPREFIX)):
                logger.info(str(line))
                adminCmdParser(user,line,cmd[len(ADMINCOMMANDPREFIX):])

def pingpong(pong):
    printBytes(bytes("PONG %s\r\n" % pong,"UTF-8"))
    logger.debug("PONG")
    print("PONG\n")

setupLogging()
logger = logging.getLogger("CTFNoteTaker.main")
readbuffer=""
Utilities.connections.init()
handle(True)
printBytes(bytes("NICK %s\r\n" % NICK, "UTF-8"))
printBytes(bytes("USER %s %s Wolf :%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
handle(True)
printBytes(bytes("JOIN %s\r\n" % CHAN,"UTF-8"))
handle(True)
printMaster("Hello Master")
for x in range(0, 10):
    handle(True)

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
        logger.exception("ERROR:")
