import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.formatoutput import *

def adminDeleteCTF(s,c,conn,user,line):
    if(len(line) > 4):
        if(line[4].startswith("-v")):
            if(len(line)>5):
                if(filter_msg(line[5],s)==False):
                    deleteCTF(line[5],s,conn,c,user,True)
                    return True
                else:
                    s.send(getBannedMessageBytes())
                    return False
            else:
                printUser(s,"Please enter a CTF name to delete",user)
        else:
            if(filter_msg(line[4],s)==False):
                deleteCTF(line[4],s,conn,c,user)
                return True
            else:
                s.send(getBannedMessageBytes())
                return False
    else:
        printUser(s,"Please enter a CTF name to delete",user)
#Need to add Useful print messages here.
def deleteCTF(CTF,s,conn,c,user,verbose=False):
    try:
        #Yeah I know, Super basic Day 1 SQL injection vuln, but lazy atm. Will fix later.
        c.execute("SELECT \"ctfID\" FROM ctf where name = \'"+CTF+"\';")
        ctfID = str((c.fetchone()))[1:-2]

        c.execute("SELECT challengeID FROM challenges WHERE ctfID = "+ctfID+";")
        rows = c.fetchall()
        for row in rows:
            #row is in form (<number>,)
            rowString = (str(row))[1:-2]
            title = ""
            if(verbose):
                c.execute("SELECT title FROM challenges WHERE challengeID = "+rowString+";")
                #We need a format method for c.fetchone() for multiple columns 1 row.
                title = str(c.fetchone())
                printUser(s,"Deleting the following notes from challenge " + title + ": ",user)
                c.execute("SELECT contributor,note FROM note WHERE challengeID = "+rowString+";")
                format_output_multirow(s,c.fetchall(),user)

            c.execute("DELETE FROM note WHERE challengeID = "+rowString+";")
            if(verbose):
                printUser(s,"Notes deleted for challenge " + (title[2:-3]),user)

        c.execute("DELETE FROM challenges WHERE ctfID = "+ctfID+";")

        c.execute("DELETE FROM ctf WHERE name = \'"+CTF+"\';")

        conn.commit()
        printUser(s,"deleted " + ctf + ", along with all of its corresponding challenges and notes.",user)
    except sqlite3.IntegrityError:
        s.send(bytes("PRIVMSG %s :%s Strange error in deleting CTF\r\n" % (CHAN,CTF),"UTF-8"))
