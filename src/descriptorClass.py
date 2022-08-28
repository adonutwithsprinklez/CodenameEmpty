
import random


class Descriptor(object):
    def __init__(self):
        self.descriptions = []

    def getText(self, textId=None):
        if textId == None:
            textId = random.randint(0,len(self.descriptions)-1)
        return ""