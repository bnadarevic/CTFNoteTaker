import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def format_output(s,rows):
    print("rows:"+str(rows))
    output=[]
    for i in rows:
        for j in i:
            output.append(j)
    print(output)
    if(output!=""):
        output=", ".join(output)
        printChan(s,output) #I want to init output just in case there is something we missed in spamfilter or so
    else:
        printChan(s,"Its empty :(")
def pretty_format_output(s,rows):
    output=[]
    for i in rows:
        output.append(": ".join(str(j) for j in i))
    for i in output:
        printChan(s,i)
    
