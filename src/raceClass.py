
import copy
import random

from universalFunctions import getDataValue

class Race(object):
    def __init__(self, data):
        ''' Instantiates a Race object. '''
        # Required data
        self.id:str = data["id"]
        self.name:str = data["name"]
        self.baseStats:dict = data["baseStats"]
        self.baseSkills:list = data["baseSkills"]

        # Optional data
        self.standing:dict = getDataValue("standing", data, {})
        self.playable:bool = getDataValue("playable", data, False) # Defaults to false
        self.basePerks:list = getDataValue("basePerks", data, [])
        self.shortDescription:str = getDataValue("shortDescription", data, "")
        self.playerCreationDescription:str = getDataValue("playerCreationDescription", data, "")
        self.startingWeapon:list = getDataValue("startingWeapon", data, [])
        self.startingArmor:list = getDataValue("startingArmor", data, [])
        self.startingInventory:list = getDataValue("startingInventory", data, [])
        self.baseEffects:list = getDataValue("baseEffects", data, [])
        self.names:list = getDataValue("names", data, [])

        # Limbs and calculations
        self.limbs:list = []
        for limb in data["limbs"]:
            newLimb = copy.copy(Limb(limb, self.id))
            self.limbs.append(newLimb)
        self.limbsOptional:list = getDataValue("limbsOptional", data, [])
        self.selectedOptional:list = []
        for choice in self.getOptionalLimbs():
            for default in choice["defaultSelection"]:
                self.selectedOptional.append(choice["choices"][default])


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

    def getLimbCounts(self, optionalSelected=False):
        ''' Returns a dictionary with each limb race, and type as a key, and the count of each type as the value '''
        returnable = {}
        limbs = copy.copy(self.limbs)
        if optionalSelected:
            for limb in self.selectedOptional:
                limbs.append(limb)
        for limb in limbs:
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

    def getDescription(self, optionalSelected = False):
        ''' Generates a description of the race's appearance. '''
        if self.getIsPureRace():
            return self.getPureRaceDescription(optionalSelected)
        else:
            return self.getMixedRaceDescription(optionalSelected)

    def getPureRaceDescription(self, optionalSelected = False):
        ''' This description is used when the character is of a pure race.
            Eg. only made up of limbs from the same race. '''
        limbCounts = self.getLimbCounts(optionalSelected)
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
    
    def getMixedRaceDescription(self, optionalSelected=False):
        ''' Creates a dynamic description for the race since their limbs do not all belong to any singular race '''
        # TODO add a description generator for nonpure races.
        limbCounts = self.getLimbCounts(optionalSelected)
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
    
    def getOptionalLimbs(self):
        optionallimbs = []
        # Check for optional limbs and add the default choices if there are any
        for ol in self.limbsOptional:
            choice = {
                "name":ol["name"],
                "type":ol["type"],
                "minCount":ol["minCount"],
                "maxCount":ol["maxCount"],
                "defaultSelection":getDataValue("defaultSelection", ol, []),
                "choices":[]
            }
            for l in ol["choices"]:
                limb = Limb(l, self.id)
                choice["choices"].append(limb)
            optionallimbs.append(choice)
        return optionallimbs
    
    def updateLimbs(self):
        for choice in self.getOptionalLimbs():
            for default in choice["defaultSelection"]:
                l = choice["choices"][default]
                for e in l.getAdditionalEffects():
                    self.baseEffects.append(e)
                self.limbs.append(l)
    
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
        self.additionalEffects = getDataValue("additionalEffects", data, [])
        
    def getArmor(self):
        if self.armor:
            return self.armor
        elif not self.armorable:
            return "Unequippable"
        return None
    
    def getType(self):
        return self.type
    
    def getAttacks(self):
        return self.attacks
    
    def getName(self):
        return self.name
    
    def getAdditionalEffects(self):
        return self.additionalEffects