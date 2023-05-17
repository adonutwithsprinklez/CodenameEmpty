
'''
This file is the one that is used to launch the game. It grabs the executable's
current path and passes it to the main.py file, which then uses it to find the
game's /res/ directory.
'''

import os, sys

from main import startApplication

if __name__ == "__main__":
    if len(sys.argv)>1:
        print(sys.argv[1:])

    PATH = os.path.dirname(sys.executable)

    startApplication(PATH)