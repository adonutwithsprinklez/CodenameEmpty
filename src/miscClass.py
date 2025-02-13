import copy
import random
from dieClass import rollDice
from effectClass import Effect, processEffect
from universalFunctions import getDataValue


class Misc(object):
	def __init__(self, data, gameData):
		self.id = getDataValue("id", data, None)
		self.name = random.choice(data["name"])
		self.t = data["iType"]
		self.desc = random.choice(data["desc"])
		self.worth = data["worth"]
		effectsList = getDataValue("effects", data, [])
		self.effects = []
		for effect in effectsList:
			newEffect = Effect(effect, copy.copy(gameData.getGameData("effect", effect)))
			self.effects.append(newEffect)
		try:
			self.consumeText = random.choice(data["consumeText"])
		except:
			self.consumeText = ""
		self.consumeTextDetailed = getDataValue("consumeTextDetailed", data,
			["You {} the {} and wait to feels its effects.".format(self.consumeText.lower(), self.getName())])
		self.appliable = getDataValue("appliable", data, False)
		# Modifier logic
		self.modifier = None
		if "modifier" in data.keys():
			modifiers = data["modifier"]
			mods = []
			for mod in modifiers:
				mods += [mod[0]]*mod[1]
			mod = random.choice(mods)
			if mod != "None":
				self.modifier = gameData.getGameData("modifier", mod).getInfo()
				self.name = "{} {}".format(self.modifier["n"], self.name)
		try:
			pass
		except:
			self.modifier = None

	def consumableEffect(self, player, gameData):
		player.disp.clearScreen()
		player.disp.displayHeader("You {} the {}".format(self.consumeText.lower(), self.name))		
		player.disp.display(random.choice(self.consumeTextDetailed))

		mods = []
		if self.modifier:
			mods = [self.modifier]

		for effect in self.effects:
			player.effects.append(effect)
			effect = player.effects[-1]
			messages = processEffect(effect, player, gameData, mods)
			for message in messages:
				player.disp.display(message)
		'''
		for effect in self.effects:
			if effect[0] == "heal":
				healing = rollDice(effect[1])
				if self.modifier:
					if self.modifier["e"] == "strongEffect":
						healing *= rollDice(self.modifier["s"])
					elif self.modifier["e"] == "improved":
						healing += rollDice(self.modifier["s"])
					elif self.modifier["e"] == "impaired":
						healing -= rollDice(self.modifier["s"])
				if healing > 0:
					actualEffects += 1
					player.giveHP(healing)
					player.disp.display("You feel strengthened from the {}, giving you {} hp.".format(self.name, healing))
		if actualEffects <= 0:
			# TODO Display no effects message
			pass
		'''
		
		player.disp.closeDisplay()
		player.disp.wait_for_enter()
	
	def applyEffectsTo(self, disp, target):
		disp.displayHeader(f"Applying {self.getName()} to {target.name}")
		disp.display(f"You apply the {self.getName()} to {target.name}.")
		
		for effect in self.effects:
			if effect.appliable:
				target.effects.append(effect)

		disp.closeDisplay()
		disp.wait_for_enter()
	
	def getName(self, full=False, reverse=True):
		if full:
			if reverse:
				return f"[{self.t.upper()}] {self.name}"
			return f"{self.name} [{self.t.upper()}]"
		return self.name
	
	def get_id(self):
		return self.id
	
	def getValue(self):
		#TODO: Add modifiers to worth
		return self.worth