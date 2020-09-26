import random
import copy

from itemGeneration import generateWeapon, generateName
from armorClass import Armor
from miscClass import Misc
from dieClass import rollDice, maxRoll


class Enemy(object):
    def __init__(self, data, weapons, armor, misc, modifiers):
        self.name = generateName(data)
        self.eID = data["eID"]
        self.desc = random.choice(data["desc"])
        self.hpMax = rollDice(data["hp"])
        self.damage = data["damage"]
        self.xp = int(random.random()*data["xp"]+0.5)
        if data["weapon"]:
            self.weapon = generateWeapon(
                weapons[random.choice(data["weapon"])])
        # Adds modifiers to the enemy
        if data["modifier"]:
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
                        weapons[self.itemDrop[0]])
                elif self.itemDrop[0] in armor.keys():
                    self.itemDrop[0] = Armor(armor[self.itemDrop[0]])
                elif self.itemDrop[0] in misc.keys():
                    self.itemDrop[0] = Misc(misc[self.itemDrop[0]])
            except:
                print("Error loading {} item reward.".format(self.name))

        if self.xp < 1:
            self.xp = 1

    def getHealth(self):
        return int(((1.0*self.hp)/self.hpMax)*68 + 0.5)

    def getWeaponDamage(self, rand=True):
        if self.weapon:
            return rollDice(self.damage) + rollDice(self.weapon.damage)
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
            return "Something happens. Blame the developer for this. This was implemented very late one night."

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
        return int((1.0*(self.hpMax+self.hp) + maxRoll(self.damage) + maxRoll(self.weapon.damage) + maxRoll(armor))/5)
