import random


class Misc(object):
	def __init__(self,data):
		self.name = random.choice(data["name"])
		self.t="m"
		self.desc = random.choice(data["desc"])
		self.worth = random.randint(data["worthMin"],data["worthMax"])