#!/usr/bin/env python3

# modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import sys
import re
import socket
import string
import sqlite3
from Utilities.StringUtils import *
from Utilities.conf import *
from Utilities.permissionUtils import *
from commands.startnew import *
from commands.listchals import *
from commands.listctfs import *
from commands.create import *
from commands.add import *
from commands.read import *
from commands.deleteNote import *
from commands.notify import *

def cmdParser(user,line,cmd):
    if(line[len(line)-1].lower() == "public"):
        user = CHAN
        del line[len(line)-1]
    else:
        if(line[2].lower() == CHAN.lower()):
            user = CHAN
    cmd = cmd.lower()



    if(cmd=="help"):
        help(user)

    elif(cmd=="startnew"):
        startnewcmd(line,user)


    elif(cmd=="listchal"):
        list_chals(user,line)


    elif(cmd=="listctf"):
        list_CTFs(user,line)

    elif(cmd=="create"):
        startcreatecmd(user,line)
    elif(cmd=="add"):
        startaddcmd(user,line)
    elif(cmd.startswith("add(")):
        startaddcmdparams(user,line)

    elif(cmd=="read"):
        startreadcmd(user,line)

    elif(cmd=="joinfail"):#pm to bot if it connects but doesnt join channel
        join_chan_if_it_fails()

    elif(cmd=="deletenote"):#pm to bot if it connects but doesnt join channel
        startDeleteNoteCmd(user,line)

    elif(cmd=="notify"):
        startnotifycmd(user,getUser(line),line)

def help(user=CHAN):
    printUser(".help [public], .startnew <CTF> , .listchal <CTF> , .listctf , .create <CTF> <chalname> , .add <CTF> <chalname> <note>, or .add(CTF,Challenge,Note) .read [-v] <CTF> <chalname> ",user)
    printUser("Do not use whitespace in CTF name(you can use it in challenge name)", user)
    printUser("Prefix your note with \"note:\" (without quotes)", user)
    print("HELP\n")

def join_chan_if_it_fails():
    #patch because it doesnt join each time
    printBytes(bytes("JOIN %s\r\n" % CHAN,"UTF-8"))
