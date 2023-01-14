import random
import copy

from itemGeneration import generateWeapon
from textGeneration import generateStringWithVariables
from armorClass import Armor
from miscClass import Misc
from dieClass import rollDice, maxRoll


class Enemy(object):
    def __init__(self, data, weapons, armor, misc, modifiers):
        self.name = generateStringWithVariables(data, "name")
        self.eID = data["eID"]
        self.desc = generateStringWithVariables(data, "desc")
        self.hpMax = rollDice(data["hp"])
        self.damage = data["damage"]
        self.xp = data["xp"]
        self.weapon = None
        if data["weapon"]:
            self.weapon = generateWeapon(weapons[random.choice(data["weapon"])], modifiers)

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
                    mod = modifiers[mod].getInfo()
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
            self.armor = Armor(armor[armorType])
        else:
            self.armor = None
        self.deathMsg = random.choice(data["deathMsg"])
        self.itemChance = data["itemChance"]
        if self.itemChance > 0:
            self.itemDrop = copy.copy(random.choice(data["itemDrops"]))
            try:
                if self.itemDrop[0] in weapons.keys():
                    self.itemDrop[0] = generateWeapon(
                        weapons[self.itemDrop[0]], modifiers)
                elif self.itemDrop[0] in armor.keys():
                    self.itemDrop[0] = Armor(armor[self.itemDrop[0]])
                elif self.itemDrop[0] in misc.keys():
                    self.itemDrop[0] = Misc(misc[self.itemDrop[0]], modifiers)
            except Exception as e:
                print("Error loading {} item reward.".format(self.name))
                print(e)

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
