import random

from textGeneration import generateString

ARMOR_TYPES_LIGHT = {
	"head": ["Cap","Hood"],
	"torso": ["Robe","Garmet"],
	"arm":["Wrap"],
	"leg":["shoe"],
	"tail":["Tailcover"]
}

ARMOR_TYPES_MEDIUM = {
	"head": ["Helmet"],
	"torso": ["Armor"],
	"arm":["Glove"],
	"leg":["Legging"],
	"tail":["Tailcover", "Tailguard"]
}

ARMOR_TYPES_HEAVY = {
	"head": ["Helm"],
	"torso": ["Breastplate"],
	"arm":["Gauntlet"],
	"leg":["Legguard"],
	"tail":["Tailguard"]
}

ARMOR_TYPES = {
	"light":ARMOR_TYPES_LIGHT,
	"medium":ARMOR_TYPES_MEDIUM,
	"heavy":ARMOR_TYPES_HEAVY
}

ARMOR_SIZES = [
	"Tiny",
	"Small",
	"Medium",
	"Large",
	"Massive"
]

def getArmorSize(size):
	if size < 1 or size > 5:
		return "Mysterious"
	return ARMOR_SIZES[size-1]

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
	
	def getName(self, full=False, reverse = True):
		if full:
			if reverse:
				return f"[{self.limb.upper()} ARMOR] {self.name} {self.nameSuffix}"
			return f"{self.name} {self.nameSuffix} [{self.limb.upper()} ARMOR]"
		return self.name + " " + self.nameSuffix
	
	def getDefenceRating(self):
		return self.defence
	
	def getValue(self):
		#TODO: Add modifiers and defense rating to worth
		return self.worth

	def __str__(self):
		return self.getName()

	def __int__(self):
		return self.getDefenceRating()