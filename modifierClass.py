import random


class Modifier(object):
	def __init__(self,title,data):
		self.effect = data["effect"]
		self.strength = data["strength"]
		self.name = data["name"]
		self.title = title
	
	def getInfo(self):
		return {"e":self.effect,"s":self.strength,"n":random.choice(self.name),"t":self.title}