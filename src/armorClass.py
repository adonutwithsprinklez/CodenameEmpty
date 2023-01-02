import random

from textGeneration import generateString

ARMOR_TYPES_LIGHT = {
	"head": ["Cap","Hood"],
	"torso": ["Robe","Garmet"],
	"arm":["Wraps"],
	"leg":["Pants"],
	"tail":["Tailcover"]
}

ARMOR_TYPES_MEDIUM = {
	"head": ["Helmet"],
	"torso": ["Armor"],
	"arm":["Gloves"],
	"leg":["Leggings"],
	"tail":["Cover"]
}

ARMOR_TYPES_HEAVY = {
	"head": ["Helm"],
	"torso": ["Breastplate"],
	"arm":["Gauntles"],
	"leg":["Legguards"],
	"tail":["Tailguard"]
}

ARMOR_TYPES = {
	"light":ARMOR_TYPES_LIGHT,
	"medium":ARMOR_TYPES_MEDIUM,
	"heavy":ARMOR_TYPES_HEAVY
}

class Armor(object):
	def __init__(self,data,limb=None):
		self.name = generateString(data)
		self.t = "a"
		self.desc = generateString(data, "desc")
		self.defence = data["defence"]
		self.worth = random.randint(data["worthMin"],data["worthMax"])

		# Optional Tags:

		# Size (ranges):
		#	1 - Tiny
		#	2 - Small
		#	3 - Medium
		#	4 - Large
		#	5 - Massive
		if "size" in data.keys():
			self.sizeMin = data["size"][0]
			self.sizeMax = data["size"][1]
		else:
			self.sizeMin = 1
			self.sizeMax = 5
		
		# Weight type:
		if "weight" in data.keys():
			self.armorWeight = data["weight"]
		else:
			self.armorWeight = random.choice(list(ARMOR_TYPES.keys()))
		
		# Limb Type:
		if limb:
			self.limb = limb
		else:
			if "limb" in data.keys():
				self.limb = random.choice(list(data["limb"].keys()))
			else:
				self.limb = random.choice(list(ARMOR_TYPES[self.armorWeight].keys()))
		if "limb" in data.keys():
			self.nameSuffix = random.choice(data["limb"][self.limb])
		else:
			self.nameSuffix = random.choice(ARMOR_TYPES[self.armorWeight][self.limb])
		
		print(vars(self))
		print(self)
	
	def getName(self):
		return self.name + " " + self.nameSuffix
	
	def getDefenceRating(self):
		return self.defence

	def __str__(self):
		return self.getName()

	def __int__(self):
		return self.getDefenceRating()