import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *
from commandParser import *

def adminSudo(user,line):
    #FORMAT: ~sudo user cmd params
    if(len(line) > 5):
        newUser = line[4]
        cmd = line[5]
        newLine = ["." + newUser + "!Not:Real:IP", line[1], NICK, ":." + cmd]
        for i in range(6,len(line)):
            newLine.append(line[i])
        logging.getLogger("CTFNoteTaker.adminCommands.sudo").info(str(newLine))
        sudo(user,newLine,cmd) #Prints to you.
    else:
        printUser("Cmd format: ~sudo <user> <cmd> <params>",user)
        printUser("Don't use a prefix for the cmd, only non admin commands are allowed. ",user)


#Need to add Useful print messages here.
def sudo(user,line,cmd):
    try:
        #EVENTUALLY Check if user table contains user already. If it does, don't do it.
        cmdParser(user,line,cmd)
    except sqlite3.IntegrityError:
        printUser("Strange error in deleting CTF", user)
        printMaster("Error " + str(traceback.format_exc()))
