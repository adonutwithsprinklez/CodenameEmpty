
import copy
import random

from dieClass import rollDice
from effectClass import Effect
from universalFunctions import getDataValue


class Weapon(object):
	def __init__(self, data=None, modifiers = None, effectData = None):
		# Decides whether or not the item is generated
		if "generated" in data.keys():
			self.generated = data["generated"]
		else:
			self.generated = False
		self.name = random.choice(data["name"])
		self.t="w"
		self.desc = random.choice(data["desc"])
		self.damage = data["damage"]
		self.requiredHands = getDataValue("requiredHands", data, 1)
		self.actionText = getDataValue("actionText", data, "")
		minworth = getDataValue("worthMin", data, 0)
		maxworth = getDataValue("worthMax", data, 0)
		self.worth = random.randint(minworth,maxworth)
		effects = getDataValue("effects", data, [])
		self.effects = []
		for effect in effects:
			newEffect = Effect(effect, copy.copy(effectData[effect]))
			self.effects.append(newEffect)
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
		return ["Weapon", self.name, random.choice(self.actionText), self.damage, self.effects]

	def getAction(self):
		return random.choice(self.actionText)
	
	def getModifiers(self):
		return self.modifiers
	
	def getName(self, full=False, reverse=True, effects = False):
		if full:
			if reverse:
				return f"[WEAPON] {self.name}"
			return f"{self.name} [WEAPON]"
		if effects and len(self.effects) > 0:
			postfix = ""
			i = 0
			for effect in self.effects:
				if i > 0:
					postfix += ", "
				color = ""
				if effect.hasColor():
					color = f"<{effect.getColor()}>"
				postfix += f"{color}{effect.getName()}{color}"
				i += 1
			return f"{self.name} ({postfix})"
		return self.name
	
	def getValue(self):
		#TODO: Add modifiers to worth
		return self.worth
	
	def getEffects(self, appliableOnly):
		if appliableOnly:
			effects = []
			for effect in self.effects:
				if effect.appliable:
					effects.append(effect)
		else:
			effects = self.effects
		return effects
	
	def hasEffect(self, appliableOnly):
		return len(self.getEffects(appliableOnly)) > 0

	def __str__(self):
		return self.getName()