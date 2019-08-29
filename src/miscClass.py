import random


class Misc(object):
	def __init__(self,data):
		self.name = random.choice(data["name"])
		self.t = data["iType"]
		self.desc = random.choice(data["desc"])
		self.worth = data["worth"]