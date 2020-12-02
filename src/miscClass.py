import random
from dieClass import rollDice


class Misc(object):
	def __init__(self,data):
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

	def consumableEffect(self, player):
		player.disp.clearScreen()
		player.disp.displayHeader("You eat the {}".format(self.name))
		player.disp.display("You eat the {} and wait to feels its effects.".format(self.name))

		actualEffects = 0
		for effect in self.effects:
			if effect[0] == "heal":
				healing = rollDice(effect[1])
				if healing > 0:
					actualEffects += 1
					player.giveHP(healing)
					player.disp.display("You feel from the {}, giving you {} hp.".format(self.name, healing))
		
		if actualEffects <= 0:
			# TODO Display no effects message
			pass
		
		player.disp.closeDisplay()
		player.disp.wait_for_enter()
