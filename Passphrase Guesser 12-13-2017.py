version = "12/13/2017"
'''
Passphrase Guesser.py

Copyright (c) 2017 Jackson Belove
Beta software, use at your own risk
MIT License, free, open software for the Qtum Community

A program to enter passphrases from a text file to qtumd,
to attempt to recover mistyped passwords for an encrypted wallet.

Uses qtum-cli to send RPC queries to the qtumd server application
using the walletpassphrase command. Use the full path, relative
path or put the Python script in the same directory with qtumd.

Revisions

12/13/2017 Repurposed from Qtum Block Ripper 11-16-2017

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import subprocess
import os, sys                          # for file operations

passphrase_guess_name = "work.txt"      # name of password guess file
            
print("Passphrase Guesser", version)
numGuesses = 0            # number of guesses read from file
passphraseGuesses = []    # an array of passphrases

# Read in the passphrase guess file - - - - - - - - - - - - - - - - - - - - - - - - -

try:
    passphraseGuessFile = open(passphrase_guess_name, 'r')  # check for success, or exit
except:
    print("ERROR opening password guess file")
    print("The file", passphrase_guess_name, " must be in the same directory with this Python script")
    sys.exit()

for line in passphraseGuessFile:
    data = line
    # print("data", data)

    if data[0] != "#":                   # skip comments
        i = 0
        passphrase = ""
        
        while i < len(data):   # just grab the passphrase
            if data[i] != "\n":
                passphrase += data[i]
            else:
                break
            i += 1

        # print(passphrase)

        if passphrase == '\n':   # read to end of file
            break
            
        passphraseGuesses.append(passphrase)
        numGuesses += 1

passphraseGuessFile.close()

print("number of guesses", numGuesses)

# sys.exit()

guess = 0

while guess < numGuesses:

    print("guess", guess + 1, "of", numGuesses)
   
    params = "qtum-cli walletpassphrase " + '"' + passphraseGuesses[guess] + '" 120'

    # print(params)

    try:
        result = str(subprocess.check_output(params, shell = True))
        print("found it")

        try:
            result = str(subprocess.check_output("qtum-cli walletlock"))   # lock the wallet
            print("Wallet locked")             
        except:
            print("ERROR, no response from qtumd")
        break
    
    except:
        guess += 1 

if (guess >= numGuesses):
    print("passphrase not found")

sys.exit()

