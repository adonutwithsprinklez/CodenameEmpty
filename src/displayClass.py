
import os
import textwrap
import time


class Screen(object):
    def __init__(self, pdelay=0,delay=True,debug=False):
        self.debugging = debug
        self.delay = delay
        self.printdelay = pdelay
        self.currentLines = []

    def clearScreen(self):
        '''Clears the screen of all text.'''
        if not self.debugging:
            # os.system('cls' if os.name == 'nt' else 'clear')
            self.currentLines = []

    def display(self, msg="", br=1, br2=0):
        '''Displays the info specified in the msg parameter. br1 = a line break
        before the message, and br2 = a line break after the message.'''
        if br == 1:
            if self.delay:
                time.sleep(self.printdelay)
            newline = "|{}|".format(" "*78)
            if self.debugging:
                print(newline)
            self.currentLines.append(newline)
        for line in textwrap.wrap(msg, 72):
            if self.delay:
                time.sleep(self.printdelay)
            newline = "|   {:75}|".format(line)
            if self.debugging:
                print(newline)
            self.currentLines.append("|   {:75}|".format(line))
            # print "|   %-75s|" % (line)
        if br2 == 1:
            time.sleep(self.printdelay)
            newline = "|%s|" % (" "*78)
            if self.debugging:
                print(newline)
            self.currentLines.append(newline)


    def displayHeader(self, msg="", br1=0, br2=0):
        '''Displays a text header. br1 = a line break after the header.'''
        if br2 == 1:
            if self.delay:
                time.sleep(self.printdelay)
            newline = "|%s|" % (" "*78)
            if self.debugging:
                print(newline)
            self.currentLines.append(newline)
        title = "+----[ %s ]" % (msg)
        if self.delay:
            time.sleep(self.printdelay)
        newline = "%s%s+" % (title, "-"*(79-len(title)))
        if self.debugging:
            print(newline)
        self.currentLines.append(newline)
        if br1 == 1:
            if self.delay:
                time.sleep(self.printdelay)
            newline = "|%s|" % (" "*78)
            if self.debugging:
                print(newline)
            self.currentLines.append("|%s|" % (" "*78))

    def closeDisplay(self):
        '''This ends the current display window.'''
        if self.delay:
            time.sleep(self.printdelay)
        newline = "|%s|" % (" "*78)
        if self.debugging:
            print(newline)
        self.currentLines.append(newline)
        if self.delay:
            time.sleep(self.printdelay)
        newline = "+%s+" % ("-"*78)
        if self.debugging:
            print(newline)
        self.currentLines.append(newline)


    def dprint(self,msg):
        '''DEBUG printing. Only prints the message if the debug variable is true.'''
        print(msg)

    def get_current_lines(self):
        return self.currentLines