import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *

def format_output(rows,user=CHAN):
    print("rows:"+str(rows))
    output=[]
    for i in rows:
        for j in i:
            output.append(str(j))
    print(output)
    if(output!=""):
        output=", ".join(output)
        printUser(output,user) #I want to init output just in case there is something we missed in spamfilter or so
    else:
        printUser("Its empty :(",user)

def format_output_multirow(rows,user=CHAN):
    for row in rows:
        toPrint = []
        for item in row:
            toPrint.append(str(item))
        printUser(toPrint,user)

def pretty_format_output(rows,user=CHAN):
    output=[]
    for i in rows:
        output.append(": ".join(str(j) for j in i))
    for i in output:
        printUser(i,user)
