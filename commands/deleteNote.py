import sys
import re
import socket
import string
import sqlite3
from Utilities.conf import *
from Utilities.StringUtils import *
from Utilities.dbUtils import *
from commands.formatoutput import *

def startDeleteNoteCmd(user,line):
    if(len(line) > 4):
        if(filter_msg(line[4]) == False):
            try:
                noteID = int(line[4])
                deleteNoteREG(noteID,user)
            except ValueError:
                printUser("You didn't enter a valid number for the noteID")
        else:
            sendBannedMessage(user)
    else:
        printUser("Missing noteID")
#Need to add Useful print messages here.
def deleteNoteREG(noteID,user):
    try:
        c = getC()
        conn = getConn()
        if(noteExists(noteID)):
            c.execute("SELECT contributor,note FROM note where noteID = (?)",(noteID,))
            row = c.fetchone()
            contributor = row[0]
            if(user.strip()==contributor.strip()):
                printChan("Deleting Note:")
                c.execute("SELECT contributor,note FROM note where noteID = (?)",(noteID,))
                format_output_multirow(c.fetchall())
                c.execute("DELETE FROM note WHERE noteID = (?)",(noteID,))
                conn.commit()
                printChan("deleted note")
            else:
                printChan("You did not create this note.")
        else:
            printChan("No note exists with noteID " + str(noteID))
    except sqlite3.IntegrityError:
        printChan("Strange error in deleting note")
        printMaster("Error " + str(traceback.format_exc()))
