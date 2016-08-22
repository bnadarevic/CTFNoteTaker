import sys
import re
import socket
import string
import sqlite3
import traceback

def is_first_run():
    firstRunFile = open("firstRun.conf","r")
    data=firstRunFile.read()
    data=data.rstrip()
    if(data=="yes" or data==""):

        c.execute("CREATE TABLE ctf(ctfID INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT UNIQUE)")
        c.execute("CREATE TABLE challenges(challengeID INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,problemtext TEXT,ctfID INT NOT NULL,FOREIGN KEY(ctfID) REFERENCES ctf(ctfID)ON DELETE CASCADE)")
        c.execute("CREATE TABLE note(noteID INTEGER PRIMARY KEY AUTOINCREMENT,contributor TEXT NOT NULL,note TEXT NOT NULL,timestamp INTEGER(4) NOT NULL DEFAULT (strftime('%s','now')),challengeID INT NOT NULL,FOREIGN KEY(challengeID) REFERENCES challenge(challengeID)ON DELETE CASCADE)")
        conn.commit()
        firstRunFile.close()
        firstRunFile = open("firstRun.conf","w+")
        firstRunFile.write("no")
        firstRunFile.close()
        return True
    else:
        return False

def init():
    sqlite_file = "database.sqlite"
    global conn
    conn = sqlite3.connect(sqlite_file)
    global c
    c=conn.cursor()
    if(is_first_run()):
        c.close()
        conn.close()
        conn = sqlite3.connect(sqlite_file)
        c=conn.cursor()

    global s
    s=socket.socket()
