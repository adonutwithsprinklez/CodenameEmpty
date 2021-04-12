import copy
import random
import re

from itemGeneration import generateWeapon
from miscClass import Misc
from armorClass import Armor


class Event(object):
    def __init__(self, data, resourceId):
        self.id = data["id"]
        self.resourceId = resourceId
        self.name = random.choice(data["name"])
        self.eventType = data["type"]

        self.start = random.choice(data["start"])
        self.msg = random.choice(data[self.start]["msg"])
        self.actions = data[self.start]["actions"]

        keys = data.keys()

        self.parts = {}
        for part in keys:
            if "#" in part:
                self.parts[part] = data[part]
        
        # Check if the event can be repeated (If not specified defaults to true)
        if "isRepeatable" in keys:
            self.isRepeatable = data["isRepeatable"] 
        else:
            self.isRepeatable = True

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
            if requirement[0] == "hasMinimumStat":
                # used to make sure the player meets the minimum stat requirement
                if player.getStat(requirement[1]) < requirement[2]:
                    meetsRequiements = False
                
        return meetsRequiements

    def takeItem(self, item, amount, player):
        # TODO add support for other items
        if item == "gold":
            player.gold -= amount

    def giveItem(self, itemId, amount, player, weapons, armor, misc, modifiers):
        if itemId == "gold":
            player.gold += amount
            return True
        elif itemId in weapons.keys():
            player.inv.append(copy.copy(generateWeapon(weapons[itemId])), modifiers)
            return True
        elif itemId in armor.keys():
            player.inv.append(copy.copy(Armor(armor[itemId])))
            return True
        elif itemId in misc.keys():
            player.inv.append(copy.copy(Misc(misc[itemId], modifiers)))
            return True
        print("Item id '{}' not found".format(itemId))
        return False

class Tag(object):
    def __init__(self, data):
        self.id = data["id"]
        self.desc = data["desc"]
        self.value = data["value"]
