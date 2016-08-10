import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def format_output(s,rows):
    output=[]
    for i in rows:
        for j in i:
            output.append(j)
    output=" , ".join(output)
    printChan(s,"output: " + output)
