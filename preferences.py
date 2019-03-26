#!/usr/bin/python3

import os
import sys
import json


class preferences():
    def __init__(self, file):
        if not os.path.exists(file):
            f = open(file, "w+")
            f.close
        self.filename = file
        f = open(file, "r")
        data = f.read()
        f.close()
        try:
            self.pref_dict = json.loads(data)
        except json.decoder.JSONDecodeError:
            self.pref_dict = {"general":{}}

    def make_default(self, *args, **kwargs):
        #print(args, len(args))
        #print(kwargs)
        #makes user subdict if not exist
        user = self.find_user(args)

        if not user in self.pref_dict :
            self.pref_dict[user] = {}

        for key, value in kwargs.items():
            #adds key, value to user subdict
            if not key in self.pref_dict[user]:
                self.pref_dict[user][key] = value

        self.write_json()

        return True

    def change_pref(self, *args, **kwargs):
        #makes user subdict if not exist
        user = self.find_user(args)
        if not user in self.pref_dict :
            self.pref_dict[user] = {}
        for key, value in kwargs.items():
            #changes value to user subdict
            self.pref_dict[user][key] = value

        self.write_json()

        return True

    def read_pref(self, user, *args):
        prefs = []
        for key in args:
            prefs.append(self.pref_dict[user][key])
        pass
        return prefs

    def find_user(self,args):
        if len(args) == 0:
            user = "general"
        elif len(args) == 1 :
            user = args[0]
        else:
            return False
        return user

    def write_json(self):
        f = open(self.filename, "w")
        json.dump(self.pref_dict,f)
        f.close()

if __name__ == "__main__":
    print("tesT")
    prefs = preferences("/home/etds27/python/chess/chess_prefs.json")
    prefs.make_default("Ethan", A="b", C="b")
    prefs.change_pref(A="B", G="L")
    prefs.read_pref("general","G")
