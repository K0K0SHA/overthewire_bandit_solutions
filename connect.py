#!/usr/bin/env python3
# filename: bandit-connect.py
# purpose: connects to bandit wargame by overthewire.org
# written by K0K0$H@ the legendary hacker
#########################################################################################################
# TODO: 
#	[X] 
#	change the password display function to use python native libs instead of os.system
#	Thus, it would make it easy to make the password be bold and colored
#	Also apply this change to notes files. This should help make program more portable.
##
#	[X] 
#	upload this project to GitHub
##
#	[ ] 
#	Separate notes into prompts and solutions, eg bandit16.prompt, bandit16.notes, bandit16.password
##
#	[X] 
#	Add an optional integer getopt so you can specify level eg ./connect.py 15 for level 15
##
#	[ ]
#	Rewrite with a def main()
##
#   [ ]
#   Add a --colorless option (ask GPT)
#########################################################################################################
# ISSUES (tested on Windows 10 Powershell):
#	[ ]
#	The code exceptions out instead of calling usage. There is no try-catch around runcode
#	

import os
import getopt
import sys

# HELPER CLASS FOR COLORED AND BOLD OUTPUT ON LINUX
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

# for Powershell compatibility, run in colorless mode
# to enable colorless mode, make color = colorless
# I wonder if this has any negative side effects
class colorless:
    PURPLE = ''
    CYAN = ''
    DARKCYAN = ''
    BLUE = ''
    GREEN = ''
    YELLOW = ''
    RED = ''
    BOLD = ''
    UNDERLINE = ''
    END = ''

if os.name == 'nt':
    color = colorless

# early global init
level = "0"
username = None

# runtime passed parameters for getopt
opts = ""
args = ""

def initialize(argv):
    try:
        opts, args = getopt.getopt(argv, "")
    except Exception as E:
        print(E)
        print("Usage: ./connect.py <integer>")
        sys.exit(2)

    number_str = args[0]
    lvl = str(number_str)
    print(f"Passed string: {number_str}")
    return lvl

try:
    level = initialize(sys.argv[1:])
    username = "bandit" + str(level)
except Exception as E:
    print(E)
    # If getopt() errors out, or isn't given args, initialize program by asking a user what level they want to play.
    print("An exception occured in getopt(). The program will ask which bandit level you'd like to play manually.")
    # the usernames for bandit are bandit0 - bandit30
    level = input("Bandit level, from 0 to 30: ") # watch out; no input sanitization here
    username = "bandit" + str(level)

## username is like bandit15 at this point in the script

#promptfile = username + ".prompt"
#print(color.UNDERLINE + "level prompt for " + username + ":" + color.END)
#with open(promptfile, 'r') as infile:
    #prompt = infile.read()
    #print(prompt)


# reads notes file # TODO make it read prompts and solutions separately

try:
    notesfile = username + ".notes"
    print(color.UNDERLINE + "notes for " + username + ":" + color.END)
    with open(notesfile, 'r') as infile:
        notes = infile.read()
    print(notes)
except Exception as E:
    print(E)
    print("Error getting notes for:")
    print(username)
    confirm = input("Press Y to create new notes file for " + username + "\n")
    if confirm == 'Y' or confirm == 'y':
        create_notes_cmd = "touch " + username + ".notes"
        print("executing: " + create_notes_cmd) # debug/verbosity        
        if os.system(create_notes_cmd):
            print("note file created:")
            print(username + ".notes")


# reads SSH private key (if any); this is called the identity
identity = username + ".privatekey"
#print(color.UNDERLINE + "SSH private key: ")
#print(color.BOLD + identity)

# reads password (if any)
passwordfile = username + ".password"
print(color.UNDERLINE + "password for " + username + ":" + color.END)
# attempt identity connect if there's no password file but there is an ssh key

try:
    with open(passwordfile, 'r') as infile:
        password = infile.read()
    print(color.BOLD + password + color.END)
except Exception as E:
    print("Error getting password file")
    print(E)


def standard_connect():
    url = "bandit" + level + "@bandit.labs.overthewire.org"
    port = "2220" 	# port needs to be a string and not an int for concatenation, so that os.system() can run cmdstr properly
    cmdstr = "ssh -p " + port + " " + url
    print("executing: " + cmdstr) # debug/verbosity
    os.system(cmdstr)

def privatekey_connect():
    print("No password file found, but identity file located:")
    print(identity)
    confirm = input("Press Y to confirm SSH connection with this key...\n")
    if confirm == 'Y' or confirm == 'y':
        url = "bandit" + level + "@bandit.labs.overthewire.org"
        port = "2220"   # port needs to be a string and not an int for concatenation, so that os.system() can run cmdstr properly
        cmdstr = "ssh -i " + identity + " " + "-p " + port + " " + url
        print("executing: " + cmdstr) # debug/verbosity
        os.system(cmdstr)

if not os.path.exists(passwordfile) and os.path.exists(identity):
    privatekey_connect()
else:
    standard_connect()