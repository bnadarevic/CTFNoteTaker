import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.formatoutput import *

def list_CTFs(s,c):
    c.execute("SELECT name FROM ctf")
    rows=c.fetchall()
    format_output(rows)