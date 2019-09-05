
import copy

class Race(object):
    def __init__(self, data=None):
        if data:
            self.id = data["id"]
            self.baseStats = data["baseStats"]
            self.baseSkills = data["baseSkills"]
            self.standing = data["standing"]
            self.playable = data["playable"]
            self.limbs = []
            if self.playable:
                self.playerCreationDesc = data["playerCreationDescription"]
            for limb in data["limbs"]:
                newLimb = copy.copy(Limb(limb))
                self.limbs.append(newLimb)
        else:
            self.id = ""
            self.baseStats = {}
            self.baseSkills = []
            self.standing = {}
            self.limbs = []


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