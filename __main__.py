#!/usr/bin/env python3


import sys
import re
import subprocess
import os
import string
import datetime

import keyboard

import nltk
from nltk.corpus import words

CSV_SEP = ","

USER_INPUT_ERROR = -2
UNKOWN_ERROR = -1
SUCCESS = 0
READ_FILE_ERROR = 1
WRITE_FILE_ERROR = 2
APPEND_FILE_ERROR = 4
DEADLOCK_NOT_FOUND_ERROR = 8 

class Deadlock():
    def __init__(self):
        self.tokens = list()
        self.lock = False
        return None
    
    def toggle(self, token=""):
        if self.lock:
            if token in self.tokens:
                self.lock = not self.lock
                self.tokens.remove(token)
                return token
            else:
                return token
        else:
            token = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            self.tokens.append(token)
            self.lock = not self.lock
            return token

class Debuglog():
    def __init__(self, debuglog_local="./debug.log"):
        self.debuglog_local = debuglog_local
        self.initDebuglog()
        self.deadlock = Deadlock()
        return None


    def log(self, txt, sep="\n"):
        try:
            while not self.deadlock.toggle(self.debuglog_local):
                continue
            fp = open(self.debuglog_local, 'a')
            c =  str(datetime.datetime.now()).split('.')[0].replace(' ', '_')
            fp.write(f"{c}{CSV_SEP}{txt}{sep}")
            fp.close()
            while not self.deadlock.toggle(self.debuglog_local):
                continue
            return SUCCESS
        except Exception as e:
            sys.stderr.write(e)
            return APPEND_FILE_ERROR

    def initDebuglog(self):
        return Utils.initFile(self.debuglog)


class Utils:
    def __init__(self):
        self.debuglog_local = "./debug.log"
        self.debuglog = Debuglog(self.debuglog_local)
        return None

    def initFile(file_local, mode='r'):
        if mode == 'r'
            try:
                fp = open(file_local, 'r')
                fp.close()
            except FileNotFoundError:
                try:
                    fp = open(file_local, 'w')
                    fp.write("")
                    fp.close()
                except Exception as e:
                    return handleError(e, WRITE_FILE_ERROR)
        elif mode == 'w'
        else:
            return handleError("Wrong file IO mode", USER_INPUT_ERROR)
        return SUCCESS

    def handleError(e, ret=UNKOWN_ERROR):
        sys.stderr.write(e)
        self.debuglog.debuglog(e)
        return ret


class RatTab:
    def __init__(self, custom=True):
        ntlk.download("words")
        self.custom = custom
        self.mode = ""
        self.clearWord()
        self.startDebuglog()
        os.seteuid(0)
        self.running = False

    def clearWord(self):
        self.word = ""
        return SUCCESS


    def initDictionary(self):
        try:
            fp = open(self.dictionary_local, 'r')
            self.dictionary = fp.readlines()
            fp.close()
        except FileNotFoundError:
            self.dictionary = list()
            continue
        try:
            initFile(self.dictionary)
        except Exception as e:
            return handleError(e)
        return SUCCESS

    def spellcheck(self):
        if len(self.word) > 1:
            self.word = re.sub(r"^[w]", "", self.word.lower())
            if self.word not in words.words():
                debug.log(f"Invalid Word: {self.word}")
            if self.word not in self.dictionary:
                self.dictionaryAdd(self.word)
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
    rattab = RatTab()
    sys.exit(rattab.runme()
