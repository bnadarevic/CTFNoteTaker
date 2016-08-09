#!/usr/bin/env python3

# slightly modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import time
import re
import socket
import string



def handle():
  print("GETTING BUFFER\n")
  global readbuffer
  ircmsg=s.recv(1024)
  readbuffer = readbuffer+ircmsg.decode("UTF-8")
  temp = str.split(readbuffer, "\n")
  readbuffer=temp.pop()
  for line in temp:
    line = str.rstrip(line)
    line = str.split(line)
    if(line[0] == "PING"):
      pingpong(line[1])
    elif(line[1]=="PRIVMSG"):
      cmd=line[3]
      cmd=cmd[1:]
      if(cmd=="!help"):        
        help()
      elif(cmd=="!create"):
        create(line[3:])
      

def pingpong(pong):    
   s.send(bytes("PONG %s\r\n" % pong,"UTF-8"))
   print("PONG\n")
  
def help():
  global CHAN
  s.send(bytes("PRIVMSG %s :!help , !list , !create <chalname> ,!add <chalname> <note>,!read <chalname>\r\n" % CHAN,"UTF-8"))
  print("HELP\n")
  
def create(filename):
   global CHAN
   s.send(bytes("PRIVMSG %s :'%s' created" % (CHAN,filename),"UTF-8"))
  #=open(filename+".txt","a")  
  
  
HOST = "irc.freenode.net"
PORT = 6667
CHAN="#CHANGETHIS"
NICK = "CHANGETHIS"
IDENT = "CHANGETHIS"
REALNAME = "CHANGETHIS"
MASTER = "CHANGETHIS"
readbuffer=""
challist=[]
s=socket.socket( )
s.connect((HOST, PORT))
handle()
s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s:%s\r\n" % (IDENT, HOST, REALNAME), "UTF-8"))
handle()
s.send(bytes("JOIN %s" %CHAN,"UTF-8"))
s.send(bytes("PRIVMSG %s :Hello Master\r\n" % MASTER, "UTF-8"))

while(1):  
  handle()
  