import random


class Modifier(object):
	def __init__(self,title,data):
		self.effect = data["effect"]
		self.strength = data["strength"]
		self.name = data["name"]
		self.title = title
		if "desc" in data.keys():
			self.desc = data["desc"]
		else:
			self.desc = []
	
	def getInfo(self):
		info = {"e":self.effect,"s":self.strength,"n":random.choice(self.name),"t":self.title}
		if len(self.desc) > 0:
			info["d"] = random.choice(self.desc)

		return info