import copy
import random
import re

from itemGeneration import generateWeapon
from miscClass import Misc
from armorClass import Armor


class Event(object):
    def __init__(self, data):
        self.id = data["id"]
        self.name = random.choice(data["name"])

        self.start = random.choice(data["start"])
        self.msg = random.choice(data[self.start]["msg"])
        self.actions = data[self.start]["actions"]

        self.parts = {}
        for part in data.keys():
            if "#" in part:
                self.parts[part] = data[part]

        self.finished = False

    def gotoPart(self, partId):
        if partId in self.parts.keys():
            self.msg = random.choice(self.parts[partId]["msg"])
            self.actions = self.parts[partId]["actions"]
        else:
            raise Exception(
                "The next part was not properly setup. Event ID: " + self.id)

    def finish(self):
        self.finished = True

    def getTag(self, tagData):
        return Tag(tagData)

    def getPossibleActions(self, player):
        actions = []
        for action in self.actions:
            if "requirements" in action.keys():
                if self.playerMeetsRequirements(action["requirements"], player):
                    actions.append(action)
            else:
                actions.append(action)
        return actions

    def playerMeetsRequirements(self, requirements, player):
        # TODO add support for other types of requirements
        meetsRequiements = True
        for requirement in requirements:
            if requirement[0] == "have":
                # Used to see if player has the corresponding item/gold/xp/lvl/etc.
                if requirement[1] == "gold":
                    if player.gold < requirement[2]:
                        meetsRequiements = False
        return meetsRequiements

    def takeItem(self, item, amount, player):
        # TODO add support for other items
        if item == "gold":
            player.gold -= amount

    def giveItem(self, itemId, amount, player, weapons, armor, misc):
        if itemId == "gold":
            player.gold += amount
        elif itemId in weapons.keys():
            player.inv.append(copy.copy(generateWeapon(weapons[itemId])))
        elif itemId in armor.keys():
            player.inv.append(copy.copy(Armor(armor[itemId])))
        elif itemId in misc.keys():
            player.inv.append(copy.copy(Misc(misc[itemId])))

class Tag(object):
    def __init__(self, data):
        self.id = data["id"]
        self.desc = data["desc"]
        self.value = data["value"]
