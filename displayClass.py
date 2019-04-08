
import os
import textwrap
import time


class Screen(object):
    def __init__(self, pdelay=0,debug=False):
        self.debugging = debug
        self.printdelay = pdelay

    def clearScreen(self):
        '''Clears the screen of all text.'''
        if not self.debugging:
            os.system('cls' if os.name == 'nt' else 'clear')

    def display(self, msg="", br=1, br2=0):
        '''Displays the info specified in the msg parameter. br1 = a line break
        before the message, and br2 = a line break after the message.'''
        if br == 1:
            time.sleep(self.printdelay)
            print("|{}|".format(" "*78))
        for line in textwrap.wrap(msg, 72):
            time.sleep(self.printdelay)
            print("|   {:75}|".format(line))
            # print "|   %-75s|" % (line)
        if br2 == 1:
            time.sleep(self.printdelay)
            print("|%s|" % (" "*78))


    def displayHeader(self, msg="", br1=0):
        '''Displays a text header. br1 = a line break after the header.'''
        title = "+----[ %s ]" % (msg)
        time.sleep(self.printdelay)
        print("%s%s+" % (title, "-"*(79-len(title))))
        if br1 == 1:
            time.sleep(self.printdelay)
            print("|%s|" % (" "*78))

    def closeDisplay(self):
        '''This ends the current display window.'''
        time.sleep(self.printdelay)
        print("|%s|" % (" "*78))
        time.sleep(self.printdelay)
        print("+%s+" % ("-"*78))


    def dprint(self,msg):
        '''DEBUG printing. Only prints the message if the debug variable is true.'''
        if self.debugging:
            print(msg)
