import random

from dieClass import rollDice

class NPC(object):
	def __init__(self,data):
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
	
	def load(self, race, dialogue):
		for dialogId in self.dialogueIds:
			self.dialogue.extend(dialogue[dialogId]["lines"])
	
	# Dialog stuff
	def getDialogueLine(self, query):
		possibleDialog = []
		queryKeys = query.keys()
		for line in self.dialogue:
			checks = []
			for criteria in line["criteria"]:
				if criteria[0] in queryKeys:
					checks.append(criteria[1] == query[criteria[0]])
			if "criteriaInverse" in line.keys():
				for criteria in line["criteriaInverse"]:
					if criteria[0] not in queryKeys:
						checks.append(True)
					else:
						checks.append(criteria[1] != query[criteria[0]])
			if all(checks):
				possibleDialog.append(line)
		print(possibleDialog)
		return random.choice(possibleDialog)["dialogue"]

	# Getters

	def getName(self):
		return self.name

	def getRace(self):
		return self.race

	def getProfessions(self):
		return self.professions

	def getFlags(self):
		return self.flags

	def getInventory(self):
		return self.inventory
	
	def getDialogueIds(self):
		return self.dialogueIds