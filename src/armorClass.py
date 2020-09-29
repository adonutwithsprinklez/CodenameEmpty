import random

from textGeneration import generateString

class Armor(object):
	def __init__(self,data):
		self.name = generateString(data)
		self.t = "a"
		self.desc = generateString(data, "desc")
		self.defence = data["defence"]
		self.worth = random.randint(data["worthMin"],data["worthMax"])

	def __str__(self):
		return self.name

	def __int__(self):
		return self.defence