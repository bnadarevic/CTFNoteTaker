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
            if(cmd==".help"):
                help(user)

            elif(cmd==".startnew"):
                startnewcmd(line,user,s,conn,c)

 
            elif(cmd==".listchal"):                
                list_chals(line,s,c)
               

            elif(cmd==".listctf"):
                list_CTFs(c,s)

            elif(cmd==".create"):
                startcreatecmd(s,line,c,conn)
                    

            elif(cmd==".add"):
                startaddcmd(s,c,conn,user,line)
                

            elif(cmd==".read"):
                
                startreadcmd(user,s,c,lines)
                
            elif(cmd==".joinfail"):#pm to bot if it connects but doesnt join channel
                join_chan_if_it_fails()
                
                
            elif(cmd==".quit"):
                if(len(line)>4):
                    quit(line[4])
                else:
                    help_chan()


def is_first_run():
    firstRunFile = open("firstRun.conf","r")
    data=firstRunFile.read()
    data=data.rstrip()
    if(data=="yes"):
        c.execute("CREATE TABLE ctf(ctfID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL)")
        c.execute("CREATE TABLE challenges(challengeID INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,problemtext TEXT,ctfID INT NOT NULL,FOREIGN KEY(ctfID) REFERENCES ctf(ctfID)ON DELETE CASCADE)")
        c.execute("CREATE TABLE note(noteID INTEGER PRIMARY KEY AUTOINCREMENT,contributor TEXT NOT NULL,note TEXT NOT NULL,challengeID INT NOT NULL,FOREIGN KEY(challengeID) REFERENCES challenge(challengeID)ON DELETE CASCADE)")
        conn.commit()
        firstRunFile.close()
        firstRunFile = open("firstRun.conf","w")
        firstRunFile.write("no")
        firstRunFile.close()
        return True
    else:
        return False





def check_pass(password):
    passfile=open("password","r").read()
    passfile=passfile.replace("\n","")
    if(password==passfile):
        return True
    else:
        return False

def pingpong(pong):
    s.send(bytes("PONG %s\r\n" % pong,"UTF-8"))
    print("PONG\n")

def help_chan():
    printChan(s,".help , .startnew <CTF> , .listchal <CTF> , .listctf , .create <CTF> <chalname> , .add <CTF> <chalname> <note>, .read <CTF> <chalname> , .quit <pass>")
    s.send(bytes("PRIVMSG %s :Do not use whitespace in CTF name(you can use it in challenge name)\r\n" % CHAN,"UTF-8"))
    s.send(bytes("PRIVMSG %s :Prefix your note with \"note:\" (without quotes)\r\n" % CHAN,"UTF-8"))
    print("HELP\n")

def help(user):
    printUser(s,".help , .startnew <CTF> , .listchal <CTF> , .listctf , .create <CTF> <chalname> , .add <CTF> <chalname> <note>, .read <CTF> <chalname> , .quit <pass>",user)
    printUser(s,"Do not use whitespace in CTF name(you can use it in challenge name)", user)
    printUser(s,"Prefix your note with \"note:\" (without quotes)", user)
    print("HELP\n")






def create(CTF,challenge):
    try:
        challenge=" ".join(challenge)
        c.execute("INSERT INTO challenges(title,ctfID) VALUES((?),(SELECT ctfID FROM ctf WHERE name=(?)))",(challenge,CTF))
        conn.commit()
        s.send(bytes("PRIVMSG %s :added challenge %s to %s\r\n" % (CHAN , challenge , CTF),"UTF-8"))
    except:
        s.send(bytes("PRIVMSG %s :CTF doesnt exist , if you are certain it does spam NETWORKsecurity\r\n" % CHAN,"UTF-8"))




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
    handle()
