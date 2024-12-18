import random
import copy

from armorClass import Armor
from dieClass import rollDice, maxRoll
from eventClass import Event
from itemGeneration import generateWeapon
from miscClass import Misc
from textGeneration import generateStringWithVariables
from universalFunctions import getDataValue


class Enemy(object):
    def __init__(self, enemy, gameData):
        data = gameData.getGameData("enemy", enemy)
        self.name = generateStringWithVariables(data, "name")
        self.eID = data["eID"]
        self.desc = generateStringWithVariables(data, "desc")
        self.hpMax = rollDice(data["hp"])
        self.damage = data["damage"]
        self.xp = data["xp"]
        self.weapon = None
        self.effects = getDataValue("effects", data, [])
        self.flags = getDataValue("flags", data, [])
        if data["weapon"]:
            self.weapon = generateWeapon(random.choice(data["weapon"]), gameData)

        # Adds modifiers to the enemy
        self.modifiers = []
        if "modCount" in data.keys():
            numberOfMods = rollDice(data["modCount"])
        else:
            numberOfMods = 0
        if data["modifier"]:
            for i in range(numberOfMods):
                # Calculates the chance for each mod
                mods = []
                for mod in data["modifier"]:
                    mods += [mod[0]]*mod[1]
                # Chooses a mod
                mod = random.choice(mods)
                # If the mod is not none add the info
                if mod != "None":
                    mod = gameData.getGameData("modifier", mod).getInfo()
                    # modifies the enemy's name to match the effect
                    self.name = "%s %s" % (mod["n"], self.name)
                    # Gets into the mod's effects
                    if mod["e"] == "damage":
                        self.damage += ";%s" % (mod["s"])
                    elif mod["e"] == "health":
                        self.hpMax += rollDice(mod["s"])
                    self.modifiers.append(mod)
        # Wait until modifiers are added to set the starting health
        self.hp = self.hpMax

        armorType = random.choice(data["armor"])
        if armorType != "None":
            self.armor = Armor(gameData.getGameData("armor", armorType))
        else:
            self.armor = None
        self.deathMsg = random.choice(data["deathMsg"])
        self.itemChance = data["itemChance"]
        if self.itemChance > 0:
            self.itemDrop = copy.copy(random.choice(data["itemDrops"]))
            try:
                if self.itemDrop[0] in gameData.getListOfKeys("weapon"):
                    self.itemDrop[0] = generateWeapon(self.itemDrop[0], gameData)
                elif self.itemDrop[0] in gameData.getListOfKeys("armor"):
                    self.itemDrop[0] = Armor(gameData.getGameData("armor",self.itemDrop[0]))
                elif self.itemDrop[0] in gameData.getListOfKeys("misc"):
                    self.itemDrop[0] = Misc(gameData.getGameData("misc", self.itemDrop[0]), gameData)
            except Exception as e:
                print("Error loading {} item reward.".format(self.name))
                print(e)
        
        self.defeatEvent = getDataValue("defeatEvent", data, None)
        if self.defeatEvent:
            self.defeatEventRoll = getDataValue("defeatEventRoll", data, "1d20")
            roll = rollDice(self.defeatEventRoll)
            # Check if the roll is high enough to trigger the event
            # Default value to beat is 0, meaning if one is not provided, the event will always trigger
            if roll < getDataValue("defeatEventScoreToBeat", data, 0):
                self.defeatEvent = None
            else:
                event = random.choice(self.defeatEvent)
                self.defeatEvent = Event(event, gameData)

        
        # Get tags
        self.tags = getDataValue("tags", data, [])

        if self.xp < 1:
            self.xp = 1
    
    def getAccuracy(self):
        # TODO: Implement
        return 100
    
    def getDesc(self):
        description = self.desc
        for mod in self.modifiers:
            if "d" in mod.keys() and random.random() > .5:
                description = "{} {}".format(description, mod["d"])
        description = description.replace("$name", self.name)
        return description
    
    def getEffects(self):
        return self.effects
    
    def getHp(self):
        return self.hp
    
    def getMaxHP(self):
        return self.hpMax

    def getHealth(self):
        return int(((1.0*self.hp)/self.hpMax)*68 + 0.5)
    
    def getName(self):
        return self.name

    def getWeaponDamage(self):
        if self.weapon:
            return rollDice(self.damage) + self.weapon.getAttack()
        else:
            return rollDice(self.damage)

    def getStrength(self):
        return self.damage

    def getRawWeaponDamage(self):
        if self.weapon:
            return self.weapon.damage
        else:
            return "0"

    def getWeaponAction(self):
        if self.weapon:
            return random.choice(self.weapon.actionText)
        else:
            return f"{self.getName} attacks."

    def getArmorDefence(self):
        if self.armor:
            return rollDice(self.armor.defence) - 1
        else:
            return 0

    def getDanger(self):
        if self.armor != None:
            armor = self.armor.defence
        else:
            armor = "0"
        maxDamage = maxRoll(self.damage)
        maxWeaponDamage = maxRoll(self.weapon.damage)
        maxArmor = maxRoll(armor)
        danger = int((1.0*(self.hpMax+self.hp) + maxDamage + maxWeaponDamage + maxArmor)/5)
        return danger
    
    def getTags(self):
        '''Returns the tags associated with the enemy.'''
        return self.tags
    
    def hasTag(self, tag):
        '''Returns true if the enemy has the given tag.'''
        return tag in self.tags
    
    def giveHP(self, hp):
        """
        Increases the enemy's HP by the specified amount.

        Args:
            hp (int): The amount of HP to add.

        Returns:
            None
        """
        self.hp += hp
        if self.hp > self.getMaxHP():
            self.hp = self.getMaxHP()
    
    def takeHP(self, hp):
        """
        Decreases the enemy's HP by the specified amount.

        Args:
            hp (int): The amount of HP to subtract.

        Returns:
            None
        """
        self.hp -= hp
        # TODO check for death
        if self.hp < 0:
            self.hp = 0
