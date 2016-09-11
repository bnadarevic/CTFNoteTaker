import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *

def list_CTFs(user,line):
    c = getC()
    c.execute("SELECT name FROM ctf")
    rows=c.fetchall()
	if(len(rows)>0):
        format_output(rows,user)
    else:
        printUser("0 CTF's in database, you can create one with .startnew!",user)
