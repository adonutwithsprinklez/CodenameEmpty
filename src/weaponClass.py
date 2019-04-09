import random


class Weapon(object):
	def __init__(self,data):
		self.name = random.choice(data["name"])
		self.t="w"
		self.desc = random.choice(data["desc"])
		self.damage = data["damage"]
		if "actionText" in data.keys():
			self.actionText = data["actionText"]
		if "worthMin" in data.keys():
			self.worth = random.randint(data["worthMin"],data["worthMax"])

	def getAction(self):
		return random.choice(self.actionText)

	def __str__(self):
		return self.name