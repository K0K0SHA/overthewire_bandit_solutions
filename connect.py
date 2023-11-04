#!/usr/bin/env python3
# filename: bandit-connect.py
# purpose: connects to bandit wargame by overthewire.org
# written by K0K0$H@ the legendary hacker
###################################################################################################
# TODO: 
#	[X] 
#	change the password display function to use python native libs instead of os.system
#	Thus, it would make it easy to make the password be bold and colored
#	Also apply this change to notes files. This should help make program more portable.
##
#	[ ] 
#	upload this project to GitHub
##
#	[ ] 
#	Separate notes into prompts and solutions
##
#	[ ] 
#	Add an optional integer getopt so you can specify level eg ./connect.py 15 for level 15
##
#	[ ]
#	Rewrite with a def main()

import os
import getopt
import sys

# HELPER CLASS FOR COLORED AND BOLD OUTPUT
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# early global init
level = "0"
username = None

# runtime passed parameters for getopt
opts = ""
args = ""

def initialize(argv):
    try:
        opts, args = getopt.getopt(argv, "")
    except getopt.GetoptError:
        print("Usage: ./connect.py <integer>")
        sys.exit(2)

    if len(args) > 1:
        print("Usage: ./connect.py <integer>")
        sys.exit(2)

    number_str = args[0]
    lvl = str(number_str)
    # Your logic using the 'number_str' string goes here
    print(f"Passed string: {number_str}")
    return lvl

level = initialize(sys.argv[1:])

# TODO IMPORTANT: ENSURE THIS IS DONE ONLY IF getopt() returns None
# If getopt() gets None, initialize program by asking a user what level they want to play.
# the usernames for bandit are bandit0 - bandit30
if level == "":
    level = input("Bandit level, from 0 to 30: ") # watch out; no input sanitization here

username = "bandit" + str(level)

# reads notes file # TODO make it read prompts and solutions separately
notesfile = username + ".notes"
print(color.UNDERLINE + "notes for " + username + ":" + color.END)
with open(notesfile, 'r') as infile:
    notes = infile.read()
print(notes)

# reads password (if any)
passwordfile = username + ".password"
print(color.UNDERLINE + "password for " + username + ":" + color.END)
with open(passwordfile, 'r') as infile:
    password = infile.read()
print(color.BOLD + password + color.END)

url = "bandit" + level + "@bandit.labs.overthewire.org"
port = "2220" 	# port needs to be a string and not an int for concatenation, so that os.system() can run cmdstr properly
cmdstr = "ssh -p " + port + " " + url

print("executing: " + cmdstr) # debug/verbosity
os.system(cmdstr)
