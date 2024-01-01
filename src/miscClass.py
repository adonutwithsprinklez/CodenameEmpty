import random
from dieClass import rollDice


class Misc(object):
	def __init__(self, data, gameModifiers):
		self.name = random.choice(data["name"])
		self.t = data["iType"]
		self.desc = random.choice(data["desc"])
		self.worth = data["worth"]
		try:
			self.effects = data["effects"]
		except:
			self.effects = []
		try:
			self.consumeText = random.choice(data["consumeText"])
		except:
			self.consumeText = ""

		# Modifier logic
		print("\n" + self.name)
		print(data.keys())
		self.modifier = None
		if "modifier" in data.keys():
			modifiers = data["modifier"]
			mods = []
			for mod in modifiers:
				mods += [mod[0]]*mod[1]
			mod = random.choice(mods)
			if mod != "None":
				self.modifier = gameModifiers[mod].getInfo()
				self.name = "{} {}".format(self.modifier["n"], self.name)
		try:
			pass
		except:
			self.modifier = None

	def consumableEffect(self, player):
		player.disp.clearScreen()
		player.disp.displayHeader("You eat the {}".format(self.name))
		player.disp.display("You eat the {} and wait to feels its effects.".format(self.name))

		actualEffects = 0
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
		
		player.disp.closeDisplay()
		player.disp.wait_for_enter()
	
	def getName(self, full=False, reverse=True):
		if full:
			if reverse:
				return f"[{self.t.upper()}] {self.name}"
			return f"{self.name} [{self.t.upper()}]"
		return self.name
	
	def getValue(self):
		#TODO: Add modifiers to worth
		return self.worth