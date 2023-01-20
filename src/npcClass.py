import random

from dialogueRules import getSatisfactoryDialogueLines
from dieClass import rollDice
from raceClass import Race

class NPC(object):
	def __init__(self,data, npcId = "NO NPC ID PROVIDED"):
		self.npcId = npcId
		if data["name"]["type"] == "choice":
			self.name = random.choice(data["name"]["choices"])
		else:
			self.name = "Unloaded"
		self.race = random.choice(data["race"])
		self.professions = random.choices(data["professionPool"][::], k=rollDice(data["numProfessions"]))
		self.description = random.choice(data["description"])
		self.dialogueIds = data["dialogue"][::]
		self.dialogue = []
		self.numItems = data["numItems"]
		self.inventory = []
		self.itemPool = data["itemPool"]
		self.flags = random.choices(data["flagPool"], k=rollDice(data["numFlags"]))
		self.loaded = False
	
	def load(self, race, dialogue):
		self.race = Race(race[self.race])
		for dialogId in self.dialogueIds:
			self.dialogue.extend(dialogue[dialogId]["lines"])
		self.loaded = True
	
	# Dialog stuff
	def getDialogueLine(self, query):
		fullQuery = {**query, **self.getSelfQuery()}
		possibleDialog = getSatisfactoryDialogueLines(self.dialogue, fullQuery)
		print(fullQuery)
		print(possibleDialog)
		return random.choice(possibleDialog)["dialogue"]
	
	def getSelfQuery(self):
		return {
			"npcProfessions":self.getProfessions(),
			"npcFlags":self.getFlags(),
			"npcId":self.getId(),
			"npcRace":self.getRaceName()
		}

	# Getters

	def getId(self):
		return self.npcId

	def getName(self):
		return self.name

	def getRaceData(self):
		return self.race
	
	def getRaceName(self):
		return self.race.getId()

	def getProfessions(self):
		return self.professions

	def getFlags(self):
		return self.flags

	def getInventory(self):
		return self.inventory
	
	def getDialogueIds(self):
		return self.dialogueIds