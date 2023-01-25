import random

from dialogueRules import getSatisfactoryDialogueLines
from dieClass import rollDice
from itemGeneration import generateItem
from raceClass import Race

class NPC(object):
	def __init__(self,data, npcId = "NO NPC ID PROVIDED"):
		self.npcId = npcId
		if data["name"]["type"] == "choice":
			self.name = random.choice(data["name"]["choices"])
		else:
			self.name = "ERR - No NPC Name specified in NPC file"
		self.race = random.choice(data["race"])
		self.professions = random.sample(data["professionPool"][::], k=rollDice(data["numProfessions"]))
		self.description = random.choice(data["description"])
		self.dialogueIds = data["dialogue"][::]
		self.dialogue = []
		self.otherDialogueOptions = []
		numItems = rollDice(data["numItems"])
		self.inventoryData = data["itemPool"]
		possibleitems = []
		possibleWeights = []
		for item in self.inventoryData:
			possibleitems.append(item[0])
			possibleWeights.append(item[1])
		self.inventory = []
		if numItems > 0:
			self.inventory = random.choices(possibleitems, weights=possibleWeights, k=numItems)
		self.inventoryGenerated = False
		self.generatedInventory = []
		self.itemPool = data["itemPool"]
		self.flags = random.sample(data["flagPool"], k=rollDice(data["numFlags"]))
		self.loaded = False
	
	def load(self, race, dialogue, armor, misc, weapons, modifiers):
		self.race = Race(race[self.race])
		for dialogId in self.dialogueIds:
			self.dialogue.extend(dialogue[dialogId]["lines"])
			if "otherDialogueOptions" in dialogue[dialogId].keys():
				for option in dialogue[dialogId]["otherDialogueOptions"]:
					self.otherDialogueOptions.append(option)
		if not self.inventoryGenerated:
			for item in self.inventory:
				self.generatedInventory.append(generateItem(item, armor, misc, weapons, modifiers))
				self.inventoryGenerated = True
		self.loaded = True
	
	# Dialog stuff
	def getDialogueLine(self, query):
		fullQuery = {**query, **self.getSelfQuery()}
		possibleDialog = getSatisfactoryDialogueLines(self.dialogue, fullQuery)
		if len(possibleDialog["lines"]) > 0:
			return random.choices(possibleDialog["lines"], weights=possibleDialog["weights"], k=1)[0]["dialogue"]
		else:
			return f"ERR - No dialog line found\n'isAction'={query['isAction']}"
	
	def getSelfQuery(self):
		return {
			"npcProfessions":self.getProfessions(),
			"npcFlags":self.getFlags(),
			"npcId":self.getId(),
			"npcRace":self.getRaceId(),
			"npcInventoryCount":self.getInventoryCount(),
			"npcInventoryIds":self.getInventoryIds(),
			"npcInventoryItemTypes":self.getInventoryItemTypes(),
			"npcInventoryItemTypeCount":self.getNumInventoryItemTypes()
		}

	# Getters

	def getId(self):
		return self.npcId

	def getName(self):
		return self.name

	def getRaceData(self):
		return self.race
	
	def getRaceId(self):
		return self.race.getId()

	def getProfessions(self):
		return self.professions
	
	def getInventoryCount(self):
		if self.inventoryGenerated:
			return len(self.getGeneratedInventory())
		else:
			return len(self.inventory)
	
	def getInventoryIds(self):
		if self.inventoryGenerated:
			return list(set(self.getInventory()))
		else:
			return list(set(self.inventory))
	
	def getInventoryItemTypes(self):
		itemTypes = []
		for item in self.getGeneratedInventory():
			if item.t not in itemTypes:
				itemTypes.append(item.t)
		return itemTypes
	
	def getNumInventoryItemTypes(self):
		return len(self.getInventoryItemTypes())

	def getFlags(self):
		return self.flags

	def getInventory(self):
		return self.inventory
	
	def getGeneratedInventory(self):
		return self.generatedInventory
	
	def getGeneratedInventoryItem(self, index):
		return self.generatedInventory[index]

	def getGeneratedInventoryItemValue(self, index):
		return self.getGeneratedInventoryItem(index).worth
	
	def popItemFromGeneratedInventory(self, index):
		return self.generatedInventory.pop(index)
	
	def getDialogueIds(self):
		return self.dialogueIds
	
	def getOtherDialogueOptions(self):
		return self.otherDialogueOptions
	
	def addItemToInventory(self, item):
		self.generatedInventory.append(item)