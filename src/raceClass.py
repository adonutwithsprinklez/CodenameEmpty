
import copy


class Race(object):
    def __init__(self, data=None):
        ''' Instantiates a Race object. '''
        if data:
            self.id = data["id"]
            self.name = data["name"]
            self.baseStats = data["baseStats"]
            self.baseSkills = data["baseSkills"]
            self.standing = data["standing"]
            self.playable = data["playable"]
            self.limbs = []
            if "playerCreationDescription" in data.keys():
                self.playerCreationDesc = data["playerCreationDescription"]
            for limb in data["limbs"]:
                newLimb = copy.copy(Limb(limb))
                self.limbs.append(newLimb)
        else:
            self.id = ""
            self.name = ""
            self.baseStats = {}
            self.baseSkills = []
            self.standing = {}
            self.playable = False
            self.limbs = []

    ### GETTERS ###
    # These functions are to allow for future changes without having to modify the calls to them.

    def getBaseStats(self):
        ''' Returns the dictionary of base stats. '''
        return self.baseStats

    def getBaseSkills(self):
        ''' Returns the dictionary of base skills. '''
        return self.baseSkills

    def getBaseStanding(self):
        ''' Returns the dictionary of base standing '''
        return self.standing

    def getPlayeable(self):
        ''' Returns whether or not the race is a playable one. This is different from being a starting
            race. Starting races are added to the character creation menu, playable races set whether
            or not the player will ever be able to assume control of one of these races. '''
        return self.playable

    def getLimbObjects(self):
        ''' Returns the list of limb objects without any modifications. '''
        return self.limbs

    def getLimbCounts(self):
        ''' Returns a dictionary with each limb tyoe as a key, and the count of each type as the value '''
        returnable = {}
        for limb in self.limbs:
            if limb.type in returnable.keys():
                returnable[limb.type] += 1
            else:
                returnable[limb.type] = 1
        return returnable

    def getDescription(self):
        ''' Generates a description of the race's appearance. '''
        pass


class Limb(object):
    def __init__(self, data=None):
        ''' Instantiates a limb object. '''
        if data:
            self.type = data["type"]
            self.name = data["name"]
            self.hitChance = data["hitChance"]
            self.maxHealth = data["maxHealth"]
            self.attacks = data["attacks"]
            self.flags = data["flags"]
        else:
            self.type = ""
            self.name = ""
            self.hitChance = ""
            self.maxHealth = 1
            self.attacks = []
            self.flags = []
