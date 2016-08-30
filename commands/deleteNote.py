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
                printUser("You didn't enter a valid number for the noteID",user)
        else:
            sendBannedMessage(user)
    else:
        printUser("Missing noteID",user)
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
                printUser("Deleting Note:",user)
                c.execute("SELECT contributor,note FROM note where noteID = (?)",(noteID,))
                format_output_multirow(c.fetchall())
                c.execute("DELETE FROM note WHERE noteID = (?)",(noteID,))
                conn.commit()
                printUser("deleted note",user)
            else:
                printUser("You did not create this note.")
        else:
            printUser("No note exists with noteID " + str(noteID),user)
    except sqlite3.IntegrityError:
        printUser("Strange error in deleting note",user)
        printMaster("Error " + str(traceback.format_exc()))
