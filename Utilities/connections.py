import sys
import ssl
import re
import socket
import string
import sqlite3
import traceback
import logging
from Utilities.conf import *

logger = logging.getLogger("CTFNoteTaker")

def first_run():
    schema = ""
    with open('schema', 'r') as schema_file:
        schema = schema_file.read()
    for line in schema.split(';'):
        c.execute(line)
    conn.commit()
    logger.info("Generated Tables for first run")
    firstRunFile = open("firstRun.conf","w+")
    firstRunFile.write("no")
    firstRunFile.close()

def init():
    sqlite_file = "database.sqlite"
    firstRun = False
    try:
        with open(sqlite_file) as file:
            pass
    except IOError as e: #Either file doesn't exist, or no read perms 
        firstRun = True

    global conn
    conn = sqlite3.connect(sqlite_file)
    global c
    c=conn.cursor()
    if(firstRun):
        first_run()
        c.close()
        conn.close()
        conn = sqlite3.connect(sqlite_file)
        c=conn.cursor()

    global unwrappedSocket
    global s
    unwrappedSocket = socket.socket()
    if(SSL):
        s = ssl.wrap_socket(unwrappedSocket)
    else:
        s = unwrappedSocket
    s.connect((HOST,PORT))
