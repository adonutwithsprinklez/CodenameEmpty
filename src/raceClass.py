
import copy

class Race(object):
    def __init__(self, data=None):
        if data:
            self.id = data["id"]
            self.name = data["name"]
            self.baseStats = data["baseStats"]
            self.baseSkills = data["baseSkills"]
            self.standing = data["standing"]
            self.playable = data["playable"]
            self.startable = data["startabke"]
            self.limbs = []
            if self.startable:
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
    def getBaseStats(self):
        return self.baseStats
    
    def getBaseSkills(self):
        return self.baseSkills
    
    def getBaseStanding(self):
        return self.standing
    
    def getPlayeable(self):
        return self.playable
    
    def getStartable(self):
        return self.startable
    
    def getCreatorDescription(self):
        if self.startable:
            return self.playerCreationDesc
        else:
            return None
    
    def getDescription(self):
        pass


class Limb(object):
    def __init__(self, data=None):
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