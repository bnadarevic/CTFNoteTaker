import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def adminQuit(s,conn,user):
    printChan(s, NICK + " is shutting down.")
    printMaster(s, user + " Shutdown the bot.")
    s.send(bytes("QUIT : shutting down. \r\n","UTF-8"))
    conn.close()
    raise KeyboardInterrupt
