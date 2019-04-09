import random


class NPC(object):
	def __init__(self,data):
		self.name = random.choice(data["name"])