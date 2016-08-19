import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def adminQuit(conn,user):
    printChan(NICK + " is shutting down.")
    printMaster(user + " Shutdown the bot.")
    printBytes(bytes("QUIT : shutting down. \r\n","UTF-8"))
    conn.close()
    raise KeyboardInterrupt
