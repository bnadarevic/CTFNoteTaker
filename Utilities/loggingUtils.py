import logging
from Utilities.conf import *


def setupLogging():
    global isLogging
    isLogging = False
    if(LOGGING=="ON"):
        isLogging = True
    else:
        print("LOGGING IS DISABLED")
