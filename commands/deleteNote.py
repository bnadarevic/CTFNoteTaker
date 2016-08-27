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
                printUser("You didn't enter a valid number for the noteID",line[2])
        else:
            sendBannedMessage(user)
    else:
        printUser("Missing noteID",line[2])
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
                printUser("Deleting Note:",line[2])
                c.execute("SELECT contributor,note FROM note where noteID = (?)",(noteID,))
                format_output_multirow(c.fetchall())
                c.execute("DELETE FROM note WHERE noteID = (?)",(noteID,))
                conn.commit()
                printUser("deleted note",line[2])
            else:
                printUser("You did not create this note.")
        else:
            printUser("No note exists with noteID " + str(noteID),line[2])
    except sqlite3.IntegrityError:
        printUser("Strange error in deleting note",line[2])
        printMaster("Error " + str(traceback.format_exc()))
