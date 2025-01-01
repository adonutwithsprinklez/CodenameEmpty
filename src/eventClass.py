
import copy
import random

from dialogueRules import evaluateDialogueLine
from gameDataHandler import GameDataHandler
from itemGeneration import generateItem


class Event(object):
    def __init__(self, eventName, gameData=None):
        if not gameData:
            gameData = GameDataHandler()
        data = gameData.getGameData("event", eventName)
        self.id = data["id"]
        self.resourceId = eventName
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
        query = player.getPlayerQuery()
        return evaluateDialogueLine(requirements, query)

    def takeItem(self, item, amount, player):
        if item == "gold":
            print("Player gold before: " + str(player.gold))
            player.gold -= amount
            print ("Player gold after: " + str(player.gold))
        else:
            count = 0
            for i in player.inv:
                if item == i.get_id() and count < amount:
                    player.inv.remove(i)
                    count += 1
            print(f"Removed {count} {item} from player inventory")

    def giveItem(self, itemId, amount, player, gameData):
        # TODO: Rewrite to use the new GameDataHandler class
        if itemId == "gold":
            player.gold += amount
            return True
        else:
            item = generateItem(itemId, gameData)
            if item:
                player.inv.append(copy.deepcopy(item))
                return True
        print("Item id '{}' not found".format(itemId))
        return False
    
    def setName(self, name):
        self.name = name

class Tag(object):
    def __init__(self, data):
        self.id = data["id"]
        self.desc = data["desc"]
        self.value = data["value"]
