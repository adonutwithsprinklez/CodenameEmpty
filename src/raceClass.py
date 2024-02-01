
import copy
import random

from universalFunctions import getDataValue

class Race(object):
    def __init__(self, data):
        ''' Instantiates a Race object. '''
        self.id:str = data["id"]
        self.name:str = data["name"]
        self.baseStats:dict = data["baseStats"]
        self.baseSkills:list = data["baseSkills"]
        self.standing:dict = data["standing"]
        self.playable:bool = getDataValue("playable", data, False)
        self.limbs:Limb = []
        self.basePerks:list = getDataValue("basePerks", data, [])
        for limb in data["limbs"]:
            newLimb = copy.copy(Limb(limb, self.id))
            self.limbs.append(newLimb)
        self.shortDescription:str = getDataValue("shortDescription", data, "")
        self.playerCreationDescription:str = getDataValue("playerCreationDescription", data, "")
        self.startingWeapon:list = getDataValue("startingWeapon", data, [])
        self.startingArmor:list = getDataValue("startingArmor", data, [])
        self.startingInventory:list = getDataValue("startingInventory", data, [])
        self.basePerks:list = getDataValue("basePerks", data, [])
        self.names:list = getDataValue("names", data, [])

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
        ''' Returns a dictionary with each limb race, and type as a key, and the count of each type as the value '''
        returnable = {}
        for limb in self.limbs:
            if limb.race in returnable.keys():
                if limb.type in returnable[limb.race].keys():
                    returnable[limb.race][limb.type] += 1
                else:
                    returnable[limb.race][limb.type] = 1
            else:
                returnable[limb.race] = {}
                returnable[limb.race][limb.type] = 1
        return returnable
    
    def getLimbsOfLimbType(self, limbType, equippableOnly=False):
        limbs = []
        for limb in self.limbs:
            if limb.type == limbType:
                if not equippableOnly or limb.armorable:
                    limbs.append(limb)
        return limbs
    
    def getLimbsEquippableLimbs(self):
        limbs = []
        for limb in self.limbs:
            if limb.armorable:
                limbs.append(limb)
        return limbs
    
    def getIsPureRace(self):
        return len(self.getLimbCounts().keys()) == 1

    def getDescription(self):
        ''' Generates a description of the race's appearance. '''
        if self.getIsPureRace():
            return self.getPureRaceDescription()
        else:
            return self.getMixedRaceDescription()

    def getPureRaceDescription(self):
        ''' This description is used when the character is of a pure race.
            Eg. only made up of limbs from the same race. '''
        limbCounts = self.getLimbCounts()
        firstLimbType = list(limbCounts[self.id].keys())[0]
        description = f'Your body is that of the typical {self.name}. You have {limbCounts[self.id][firstLimbType]} {firstLimbType}'
        if limbCounts[self.id][firstLimbType] > 1:
            description += "s"
        for limbtype in list(limbCounts[self.id].keys())[1:]:
            description = f'{description}, {limbCounts[self.id][limbtype]} {limbtype}'
            if limbCounts[self.id][limbtype] > 1:
                description += "s"
        description += "."
        return description
    
    def getMixedRaceDescription(self):
        ''' Creates a dynamic description for the race since their limbs do not all belong to any singular race '''
        # TODO add a description generator for nonpure races.
        limbCounts = self.getLimbCounts()
        description = 'You look like a strange Chimera of different races.\n\t'
        for rId in limbCounts.keys():
            firstLimbType = list(limbCounts[rId].keys())[0]
            description += f'You have {limbCounts[rId][firstLimbType]} {firstLimbType}'
            if limbCounts[rId][firstLimbType] > 1:
                description += "s"
            for limbtype in list(limbCounts[rId].keys())[1:]:
                description = f'{description}, {limbCounts[rId][limbtype]} {limbtype}'
                if limbCounts[rId][limbtype] > 1:
                    description += "s"
            description += f" that appears to be of the {rId} race. "
        return description
    
    def getVitalLimbs(self):
        ''' Returns a list of limbs that are vital to the race '''
        vitals = []
        for limb in self.getLimbObjects():
            if "vital" in limb.flags:
                vitals.append(limb)
        return vitals
    
    def getHurtLimbs(self):
        ''' Returns all limbs that are not at 100% health '''
        hurtLimbs = []
        for limb in self.getLimbObjects():
            if not "unattackable" in limb.flags and limb.health < limb.maxHealth:
                hurtLimbs.append(limb)
        return hurtLimbs
    
    def getAllLimbAttacks(self):
        limbAttacks = []
        for limb in self.getLimbObjects():
            for attack in limb.getAttacks():
                limbAttacks.append([limb.name] + attack)
        return limbAttacks
    
    def getStat(self, stat):
        ''' Returns the race's base stat '''
        if stat in self.baseStats.keys():
            return self.baseStats[stat]
        else:
            return 0
    
    def getSkill(self, skill):
        ''' Returns the race's base skill '''
        if skill in self.baseSkills.keys():
            return self.baseSkills[skill]
        else:
            return 0
        
    def getName(self, includePureRace = True):
        name = self.name
        if includePureRace and self.getIsPureRace():
            name = "Pure Blooded %s" % name
        return name
    
    def getId(self):
        return self.id

    def getShortDescription(self):
        return self.shortDescription
    
    def getPlayerCreationDescription(self):
        return self.playerCreationDescription
    
    def getStartingWeapons(self):
        return self.startingWeapon
    
    def getStartingArmor(self):
        return self.startingArmor
    
    def getStartingInventory(self):
        return self.startingInventory
    
    def getPerks(self):
        return self.basePerks
    
    def getRandomName(self):
        return random.choice(self.names)
    
    def __str__(self):
        return f"{self.getId()} - {self.getName(False)}"


class Limb(object):
    def __init__(self, data=None, race=None):
        ''' Instantiates a limb object. '''
        if data:
            self.type = data["type"]
            self.name = data["name"]
            self.hitChance = data["hitChance"]
            self.maxHealth = data["maxHealth"]
            self.health = self.maxHealth
            self.attacks = data["attacks"]
            self.flags = data["flags"]
            if "race" in data.keys():
                self.race = data["race"]
            else:
                self.race = race
        else:
            self.type = ""
            self.name = ""
            self.hitChance = ""
            self.maxHealth = 1
            self.health = 1
            self.attacks = []
            self.flags = []
            self.race = None
        self.armor = None
        self.armorable = True
        if "armorable" in data.keys():
            self.armorable = data["armorable"]
        
    def getArmor(self):
        if self.armor:
            return self.armor
        elif not self.armorable:
            return "Unequippable"
        return None
    
    def getAttacks(self):
        return self.attacks