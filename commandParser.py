#!/usr/bin/env python3

# modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import sys
import re
import socket
import string
import sqlite3
from Utilities.StringUtils import *
from Utilities.conf import *
from commands.startnew import *
from commands.listchals import *
from commands.listctfs import *
from commands.create import *
from commands.add import *
from commands.read import *

def cmdParser(s,c,conn,user,line,cmd):
    if(cmd==".help"):
        if(len(line)>4):
            if(line[4]=="public"):
                help_chan(s)
            else:
                help(s,user)
        else:
            help(s,user)

    elif(cmd==".startnew"):
        startnewcmd(line,user,s,conn,c)


    elif(cmd==".listchal"):
        list_chals(line,s,c)


    elif(cmd==".listctf"):
        list_CTFs(c,s)

    elif(cmd==".create"):
        startcreatecmd(s,line,conn,c)


    elif(cmd==".add"):
        startaddcmd(s,c,conn,user,line)


    elif(cmd==".read"):
        startreadcmd(user,s,c,line)

    elif(cmd==".joinfail"):#pm to bot if it connects but doesnt join channel
        join_chan_if_it_fails()

    elif(cmd==".quit"):
        if(len(line)>4):
            quit(line[4])
        else:
            help_chan(s)


def check_pass(password):
    passfile=open("password","r").read()
    passfile=passfile.replace("\n","")
    if(password==passfile):
        return True
    else:
        return False

def help_chan(s):
    printChan(s,".help , .startnew <CTF> , .listchal <CTF> , .listctf , .create <CTF> <chalname> , .add <CTF> <chalname> <note>, .read <CTF> <chalname> , .quit <pass>")
    s.send(bytes("PRIVMSG %s :Do not use whitespace in CTF name(you can use it in challenge name)\r\n" % CHAN,"UTF-8"))
    s.send(bytes("PRIVMSG %s :Prefix your note with \"note:\" (without quotes)\r\n" % CHAN,"UTF-8"))
    print("HELP\n")

def help(s,user):
    printUser(s,".help , .startnew <CTF> , .listchal <CTF> , .listctf , .create <CTF> <chalname> , .add <CTF> <chalname> <note>, .read <CTF> <chalname> , .quit <pass>",user)
    printUser(s,"Do not use whitespace in CTF name(you can use it in challenge name)", user)
    printUser(s,"Prefix your note with \"note:\" (without quotes)", user)
    print("HELP\n")

def join_chan_if_it_fails():
    #patch because it doesnt join each time
    s.send(bytes("JOIN %s\r\n" % CHAN,"UTF-8"))

def quit(password):

    if(check_pass(password)):
        s.send(bytes("QUIT :\r\n","UTF-8"))

        conn.close()
        sys.exit()
    else:
        print("FAILED QUIT\n")
