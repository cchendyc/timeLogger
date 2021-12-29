#present by @Cindy Chen 12/24/2021
#xychencindy@gmail.com

import tkinter as tk
import graphics
import os
import collections

INPUT_FILES = {'ans': 'a',
               'quest': 'q'}

class GUI:
    """Load the directories, please look into the graphics.py file for more details """

    def __init__(self):
        self.initialized = False

    def initialize_graphics(self):
        """Create canvas"""
        a_direct, q_direct, elst = self.file_handling()
        self._ans = collections.OrderedDict(sorted(a_direct.items()))
        self._quests = collections.OrderedDict(sorted(q_direct.items()))
        self.initialized = True
        self.canvas = graphics.Canvas(self._ans, self._quests, elst, title="better call saul is a great tv show")

    def file_handling(self):
        #files handling
        # answers: {1 : ["1. xx", "2. xxx", "3. x"], ...}
        a_direct = {}
        a_path = INPUT_FILES["ans"]
        a_list = os.listdir(a_path)
        elst = []

        for ans in sorted(a_list):
            if ans.endswith(".txt") and ans.startswith('e'):
                index = ans[2:-4]
                elst.append(int(index))
            if ans.endswith(".txt") and ans.startswith('a'):
                a_values = []
                with open(a_path + "/" + ans, 'r') as f:
                    for line in f:
                        a_values.append(line)
                index = ans[1:-4]
                a_direct[int(index)] = a_values
                f.close()

        # questions: {1 : "xxx", 2: xxx, 3: "x", ...}
        q_direct = {}
        q_path = INPUT_FILES["quest"]
        q_list = os.listdir(q_path)
        for qu in sorted(q_list):
            if qu.endswith(".txt") and qu.startswith('q'):
                question = ""
                with open(q_path + "/" + qu, 'r') as f:
                    for line in f:
                        question += str(line)
                index = qu[1:-4]
                q_direct[int(index)] = question
                f.close()

        return [a_direct, q_direct, elst]


k = GUI()
k.initialize_graphics()
