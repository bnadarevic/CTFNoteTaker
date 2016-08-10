#!/usr/bin/env python3

# modified ircecho.py https://gist.github.com/RobertSzkutak/1326452

import sys
import re
import socket
import string
import sqlite3
import Utilities.conf

def filter(msg):
    regexes = [ # Creating regular experession list of banned and glined phrases.
    "Come watch me on my webcam and chat /w me :-\) http://.+:\d+/me\.mpg",
    "Speed up your mIRC DCC Transfer by up to 75%.*www\.freewebs\.com/mircupdate/mircspeedup\.exe",
    "^http://www\.angelfire\.com/[a-z0-9]+/[a-z0-9]+/[a-z_]+\.jpg <- .*!",
    "^FREE PORN: http://free:porn@([0-9]{1,3}\.){3}[0-9]{1,3}:8180$",
    "^!login Wasszup!$",
    "^!login grrrr yeah baby!$",
    "^!packet ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,15}",
    "^!icqpagebomb ([0-9]{1,15} ){2}.+",
    "^!pfast [0-9]{1,15} ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,5}$",
    "^!portscan ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,5} [0-9]{1,5}$",
    "^.u(dp)? ([0-9]{1,3}\.){3}[0-9]{1,3} [0-9]{1,15} [0-9]{1,15} [0-9]{1,15}( [0-9])*$",
    "^.syn ((([0-9]{1,3}\.){3}[0-9]{1,3})|([a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_.-]+)) [0-9]{1,5} [0-9]{1,15} [0-9]{1,15}",
    "{^porn! porno! http://.+\/sexo\.exe}",
    "(^wait a minute plz\. i am updating my site|.*my erotic video).*http://.+/erotic(a)?/myvideo\.exe$",
    "^STOP SPAM, USE THIS COMMAND: //write nospam \$decode\(.+\) \| \.load -rs nospam \| //mode \$me \+R$",
    "^FOR MATRIX 2 DOWNLOAD, USE THIS COMMAND: //write Matrix2 \$decode\(.+=,m\) \| \.load -rs Matrix2 \| //mode \$me \+R$",
    "^hey .* to get OPs use this hack in the chan but SHH! //\$decode\(.*,m\) \| \$decode\(.*,m\)$",
    ".*(http://jokes\.clubdepeche\.com|http://horny\.69sexy\.net|http://private\.a123sdsdssddddgfg\.com).*",
    "C:\\\\WINNT\\\\system32\\\\(notes|videos|xxx|ManualSeduccion|postal|hechizos|images|sex|avril)\.zip",
    "http://.+\.lycos\..+/[iy]server[0-9]/[a-z]{4,11}\.(gif|jpg|avi|txt)",
    "^Free porn pic.? and movies (www\.sexymovies\.da\.ru|www\.girlporn\.org)",
    "^LOL! //echo -a \$\(\$decode\(.+,m\),[0-9]\)$",
    "//write \$decode\(.+\|.+load -rs",
    "^Want To Be An IRCOp\? Try This New Bug Type: //write \$decode\(.+=.?,m\) \| \.load -rs \$decode\(.+=.?,m\)$",
    "^Check this out.*http://www\.pornzapp\.com.*",
    "pony",
    "onionib","slav"]#thank you ninjex for warning :)
    combined = "(" + ")|(".join(regexes) + ")"
    banned = False
    for bannedString in regexes:
        if(bannedString in msg):
            banned = True
    if(re.match(combined, msg)):
        banned = True
    return banned

def filter_msg(msg,s):
    #This is getting called properly, but bytes not sending correctly
    if(filter(msg)):
        return True
    else:
	    return False
def getBannedMessageBytes():
    return bytes(("PRIVMSG %s : "+ Utilities.conf.BANNEDPHRASEMSG +"\r\n") % Utilities.conf.CHAN,"UTF-8")
