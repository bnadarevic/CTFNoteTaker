import logging
from logging.config import fileConfig
from Utilities.conf import *


def setupLogging():
    global isLogging
    isLogging = False
    if(LOGGING.upper().strip()=="ON"):
        isLogging = True
        fileConfig('Utilities/logging.conf')
        logger = logging.getLogger("CTFNoteTaker")

        logger.info("Program started")
    else:
        logging.basicConfig(format='%(message)s', level=logging.DEBUG)
        print("LOGGING IS DISABLED")
