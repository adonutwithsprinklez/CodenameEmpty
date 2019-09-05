

class Race(object):
    def __init__(self):
        self.baseStats = {}
        self.baseSkills = []
        self.standing = {}
        self.limbs = []


class Limb(object):
    def __init__(self):
        self.type = ""
        self.name = ""
        self.hitChance = ""
        self.maxHealth = 1
        self.attacks = []
        self.flags = []