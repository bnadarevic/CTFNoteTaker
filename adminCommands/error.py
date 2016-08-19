import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from commands.create import *

def throwErrorAdminCMD(user,line):
    raise Exception("I raised an error! " + str(line) + "\r\n")
