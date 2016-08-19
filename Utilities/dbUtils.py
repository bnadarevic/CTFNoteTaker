#!/usr/bin/env python3

import sqlite3
import Utilities.connections
from Utilities.conf import *

def getC():
    return Utilities.connections.c

def getConn():
    return Utilities.connections.conn
