import sys
import re
import os
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *

def adminRestart(user):
    printMaster(user + " is restarting me")
    printChan("Restarting...")
    restartSocket()
