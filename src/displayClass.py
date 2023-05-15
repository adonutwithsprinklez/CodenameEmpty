
import os
import textwrap
import time


class Screen(object):
    def __init__(self, pdelay=0,delay=True,debug=False):
        self.debugging = debug
        self.delay = delay
        self.printdelay = pdelay
        self.currentLines = []
        self.lineWidth = 80 # Legacy

    def clearScreen(self):
        '''Clears the screen of all text.'''
        if not self.debugging:
            # os.system('cls' if os.name == 'nt' else 'clear')
            self.currentLines = []

    def display(self, msg="", br=1, br2=0):
        '''Displays the info specified in the msg parameter. br1 = a line break
        before the message, and br2 = a line break after the message.'''
        if br == 1 or br == True:
            if self.delay:
                time.sleep(self.printdelay)
            self.currentLines.append("")
        pCount = 0
        for paragraph in msg.split("\n"):
            if pCount >= 1:
                self.currentLines.append("")
            self.currentLines.append(f"<p>{paragraph}<p>")
            pCount += 1
        if br2 == 1 or br2 == True:
            time.sleep(self.printdelay)
            self.currentLines.append("")


    def displayHeader(self, msg="", br1=0, br2=0):
        '''Displays a text header. br1 = a line break after the header.'''
        if br2 == 1:
            if self.delay:
                time.sleep(self.printdelay)
            self.currentLines.append("")
        title = msg
        if self.delay:
            time.sleep(self.printdelay)
        self.currentLines.append(f"<h1>{title}<h1>")
        if br1 == 1:
            if self.delay:
                time.sleep(self.printdelay)
            self.currentLines.append("")

    def closeDisplay(self):
        '''This ends the current display window.'''
        if self.delay:
            time.sleep(self.printdelay)
        self.currentLines.append("")
        if self.delay:
            time.sleep(self.printdelay)
        self.currentLines.append(f"<h3><h3>")


    def dprint(self,msg):
        '''DEBUG printing. Only prints the message if the debug variable is true.'''
        print(msg)


    def get_current_lines(self):
        return self.currentLines
    
    def set_line_length(self, linelength):
        self.lineWidth = linelength