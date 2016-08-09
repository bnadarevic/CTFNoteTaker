#!/usr/bin/env python3

# modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import sys
import re
import socket
import string
import sqlite3




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
        line = str.split(line)
        if(line[0] == "PING"):
            pingpong(line[1])
        elif(line[1]=="PRIVMSG"):
            cmd=line[3]
            cmd=cmd[1:]            
            if(cmd=="!help"):                
                help()
               
            elif(cmd=="!startnew"):                
                startnew(line[4])
                              
                             
            elif(cmd=="!listchal"):
                if(len(line)>4):
                    list_chals(line[4:])
                else:
                    help()
            
            elif(cmd=="!listctf"):
                list_CTFs()
                        
            elif(cmd=="!create"):
                if(len(line)>5):
                    
                    create(line[4],line[5:])
                else:
                    help()
                    
            elif(cmd=="!add"):
                #CTF,chal,contributor,comment
                if(len(line)>6):
                    user=line[0]
                    CTF=line[4]
                    pattern=re.compile("note:(.*)")
                    pattern2=re.compile("(.*?)note:")
                    note=re.findall(pattern," ".join(line[5:]))
                    note=" ".join(note)
                    challenge=re.findall(pattern2," ".join(line[5:]))
                    challenge=" ".join(challenge)
                    if(filter_msg(note)):
                        add_note(CTF,challenge,line[0],note)
                    
                else:
                    help()
            

            elif(cmd=="!read"):
                if(len(line)>5):
                    read_note(line[4]," ".join(line[5:]))
                else:
                    help()
            
            elif(cmd=="!quit"):
                if(len(line)>4):
                    quit(line[4])
                else:
                    help()

                    
                    
def filter_msg(msg):
    
    regexes = [ # Creating regular experession list of banned and glined phrases.
    "Come watch me on my webcam and chat /w me :-\) http://.+:\d+/me\.mpg",
    "Speed up your mIRC DCC Transfer by up to 75%.*www\.freewebs\.com/mircupdate/mircspeedup\.exe",
    "^http://www\.angelfire\.com/[a-z0-9]+/[a-z0-9]+/[a-z_]+\.jpg <- .*!",
    "^FREE PORN: http://free:porn@([0-9]{1,3}\.){3}[0-9]{1,3}:8180$",
    "^!login Wasszup!$",
    "^!login grrrr yeah baby!$",
    "^!packet ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,15}",
    "^!icqpagebomb ([0-9]{1,15} ){2}.+",
    "^!pfast [0-9]{1,15} ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,5}$",
    "^!portscan ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,5} [0-9]{1,5}$",
    "^.u(dp)? ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,15} [0-9]{1,15} [0-9]{1,15}( [0-9])*$",
    "^.syn ((([0-9]{1,3}\.){3}[0-9]{1,3})|([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_.-]+)) [0-9]{1,5} [0-9]{1,15} [0-9]{1,15}",
    "{^porn! porno! http://.+\/sexo\.exe}",
    "(^wait a minute plz\. i am updating my site|.*my erotic video).*http://.+/erotic(a)?/myvideo\.exe$",
    "^STOP SPAM, USE THIS COMMAND: //write nospam \$decode\(.+\) \| \.load -rs nospam \| //mode \$me \+R$",
    "^FOR MATRIX 2 DOWNLOAD, USE THIS COMMAND: //write Matrix2 \$decode\(.+=,m\) \| \.load -rs Matrix2 \| //mode \$me \+R$",
    "^hey .* to get OPs use this hack in the chan but SHH! //\$decode\(.*,m\) \| \$decode\(.*,m\)$",
    ".*(http://jokes\.clubdepeche\.com|http://horny\.69sexy\.net|http://private\.a123sdsdssddddgfg\.com).*",
    "C:\\\\WINNT\\\\system32\\\\(notes|videos|xxx|ManualSeduccion|postal|hechizos|images|sex|avril)\.zip",
    "http://.+\.lycos\..+/[iy]server[0-9]/[a-z]{4,11}\.(gif|jpg|avi|txt)",
    "^Free porn pic.? and movies (www\.sexymovies\.da\.ru|www\.girlporn\.org)",
    "^LOL! //echo -a \$\(\$decode\(.+,m\),[0-9]\)$",
    "//write \$decode\(.+\|.+load -rs",
    "^Want To Be An IRCOp\? Try This New Bug Type: //write \$decode\(.+=.?,m\) \| \.load -rs \$decode\(.+=.?,m\)$",
    "^Check this out.*http://www\.pornzapp\.com.*",
    "pony",
    "onionib","slav"]#thank you ninjex for warning :)
    combined = "(" + ")|(".join(regexes) + ")"
    if re.match(combined, msg):
        s.send(bytes("PRIVMSG %s :you used banned phrase" % CHAN, "UTF-8"))
        return True
    



def format_output(rows):
    output=[]
    for i in rows:
        for j in i:
            output.append(j)
    output=" , ".join(output)
    s.send(bytes("PRIVMSG %s :output:%s\r\n" % (CHAN,output),"UTF-8"))

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
    
def help():
    s.send(bytes("PRIVMSG %s :!help , !startnew <CTF> , !listchal <CTF> , !listctf , !create <CTF> <chalname> , !add <CTF> <chalname> <note>, !read <CTF> <chalname> , !quit <pass>\r\n" % CHAN,"UTF-8"))
    s.send(bytes("PRIVMSG %s :Do not use whitespace in CTF name(you can use it in challenge name)\r\n" % CHAN,"UTF-8"))
    s.send(bytes("PRIVMSG %s :Prefix your note with \"note:\" (without quotes)\r\n" % CHAN,"UTF-8"))
    print("HELP\n")
def startnew(CTF):
    
    c.execute("INSERT INTO ctf(name) VALUES((?))",(CTF,))
    conn.commit()
    s.send(bytes("PRIVMSG %s :%s created\r\n" % (CHAN,CTF),"UTF-8"))
def list_CTFs():
    c.execute("SELECT name FROM ctf")
    rows=c.fetchall()
    format_output(rows)
    
    
def list_chals(CTF):
    #"SELECT title FROM challenge, ctf WHERE ctf.ctfID = challenge.ctfID and ctf.name = (?);
    CTF=CTF[0]
    print(CTF)
    c.execute("SELECT title FROM challenges WHERE ctfID=(SELECT ctfID FROM ctf WHERE name=(?))",(CTF,))
    rows=c.fetchall()
    format_output(rows)
    
                         
def create(CTF,challenge):
    try:
        challenge=" ".join(challenge)
        c.execute("INSERT INTO challenges(title,ctfID) VALUES((?),(SELECT ctfID FROM ctf WHERE name=(?)))",(challenge,CTF))
        conn.commit()
        s.send(bytes("PRIVMSG %s :added %s to %s\r\n" % (CHAN , challenge , CTF),"UTF-8"))
    except:
        s.send(bytes("PRIVMSG %s :CTF doesnt exist , if you are certain it does spam NETWORKsecurity\r\n" % CHAN,"UTF-8"))

def add_note(CTF,challenge,contributor,comment):
    print(CTF+"\n"+challenge+"\n"+contributor+"\n"+comment+"\n")
    challenge=challenge.rstrip() #trailing whitespace bug fix
    try:
        c.execute("INSERT INTO note (contributor,note,challengeID) VALUES((?),(?),(SELECT challengeID FROM challenges WHERE title=(?) AND ctfID=(SELECT ctfID FROM ctf WHERE name=(?))))",(contributor,comment,challenge,CTF))
        conn.commit()
        s.send(bytes("PRIVMSG %s :Note added\r\n" % CHAN,"UTF-8"))
    except:
        s.send(bytes("PRIVMSG %s :Error: CTF or challenge doesnt exist(at least I hope thats error and that nsm didnt completly screw me up)\r\n","UTF-8"))
        #its going to be ok
    
def read_note(CTF,challenge):
    c.execute("SELECT note FROM note WHERE challengeID=(SELECT challengeID FROM challenges WHERE title=(?) AND ctfID=(SELECT ctfID from ctf WHERE name=(?)))" , (challenge,CTF))
    rows=c.fetchall()
    format_output(rows)
    
    
                               
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
    
HOST = "irc.hackthissite.org"
PORT = 6667
CHAN="#ctf"
NICK = "CTFNoteTaker"
IDENT = "CTF_"
REALNAME = "Hal Glados"
MASTER = "NETWORKsecurity"
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
    
