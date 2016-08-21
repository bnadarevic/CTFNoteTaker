#!/usr/bin/env python3
from Utilities.conf import *

def check_pass(password):
    passfile=open("password","r").read()
    passfile=passfile.replace("\n","")
    if(password==passfile):
        return True
    else:
        return False

def userIsMaster(user):
    for mast in MASTER:
        if(mast.lower()==user.lower()):
            return True
    return False
