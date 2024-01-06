
import copy
import random

from dieClass import rollDice


class Weapon(object):
	def __init__(self, data=None, modifiers = None):
		# Decides whether or not the item is generated
		if "generated" in data.keys():
			self.generated = data["generated"]
		else:
			self.generated = False
		self.name = random.choice(data["name"])
		self.t="w"
		self.desc = random.choice(data["desc"])
		self.damage = data["damage"]
		if "requiredHands" in data.keys():
			self.requiredHands = data["requiredHands"]
		else:
			self.requiredHands = 1
		if "actionText" in data.keys():
			self.actionText = data["actionText"]
		else:
			self.actionText = ""
		if "worthMin" in data.keys():
			self.worth = random.randint(data["worthMin"],data["worthMax"])
		else:
			self.worth = 0
		self.modifiers = []
		if "modifiers" in data.keys():
			# Get the chance of a modifier
			if random.randint(0,100) < data["modifierChance"]:
				# Get the number of modifers to add
				modCount = rollDice(data["modifierCount"])

				# Add the modifers:
				possibleMods = copy.copy(data["modifiers"])
				for i in range(modCount):
					if len(possibleMods) > 0:
						highRoll = 0
						newMod = None
						for mod in possibleMods:
							newRoll = rollDice(mod[1])
							if newRoll > highRoll:
								newMod = mod
								highRoll = newRoll
						if newMod:
							possibleMods.remove(newMod)
							newMod = modifiers[newMod[0]].getInfo()
							self.name = "{} {}".format(newMod["n"], self.name)
							if newMod["e"] == "damage":
								self.damage += ";{}".format(newMod["s"])
							elif newMod["e"] == "worth":
								self.worth += rollDice(newMod["s"])
							if "d" in newMod.keys():
								self.desc += " {}".format(newMod["d"])
	
	def getAttack(self):
		attack = rollDice(self.damage)
		return attack
	
	def getAttackInfo(self):
		return ["Weapon", self.name, random.choice(self.actionText), self.damage]

	def getAction(self):
		return random.choice(self.actionText)
	
	def getName(self, full=False, reverse=True):
		if full:
			if reverse:
				return f"[WEAPON] {self.name}"
			return f"{self.name} [WEAPON]"
		return self.name
	
	def getValue(self):
		#TODO: Add modifiers to worth
		return self.worth

	def __str__(self):
		return self.getName()