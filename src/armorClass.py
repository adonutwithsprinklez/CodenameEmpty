import random

from textGeneration import generateString
from universalFunctions import getDataValue

ARMOR_TYPES_LIGHT = {
	"head":{
		"name":["Cap","Hood"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	},
	"torso":{
		"name":["Robe","Garmet"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	},
	"arm":{
		"name":["Wraps"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":2
	},
	"leg":{
		"name":["Shoes"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":2
	},
	"tail":{
		"name":["Tailcover"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	}
}

ARMOR_TYPES_MEDIUM = {
	"head":{
		"name":["Helmet"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	},
	"torso":{
		"name":["Armor"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	},
	"arm":{
		"name":["Gloves"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":2
	},
	"leg":{
		"name":["Leggings"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":2
	},
	"tail":{
		"name":["Tailcover", "Tailguard"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	}
}

ARMOR_TYPES_HEAVY = {
	"head":{
		"name":["Helm"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	},
	"torso":{
		"name":["Breastplate"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	},
	"arm":{
		"name":["Gauntlets"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":2
	},
	"leg":{
		"name":["Legguards"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":2
	},
	"tail":{
		"name":["Tailguard"],
		"desc":"",
		"numLimbsRequired":1,
		"numLimbsAllowed":1
	}
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
	def __init__(self, data, limb=None):
		"""
		Initialize an instance of the Armor class.

		Parameters:
		- data (dict): A dictionary containing the data for the armor.
		- limb (str, optional): The limb type for the armor. Defaults to None.
		"""
		self.name:str = generateString(data)
		self.t:str = "a"
		self.desc:str = generateString(data, "desc")
		self.defence:str = data["defence"]
		self.worth:int = random.randint(data["worthMin"], data["worthMax"])

		# Optional Tags:

		# Size (ranges):
		#   1 - Tiny
		#   2 - Small
		#   3 - Medium
		#   4 - Large
		#   5 - Massive
		sizes = getDataValue("size", data, [1,5])
		self.sizeMin:int = sizes[0]
		self.sizeMax:int = sizes[1]
		
		# Weight type:
		self.armorWeight:str = getDataValue("weight", data, random.choice(list(ARMOR_TYPES.keys())))
		
		# Limb Type:
		# First select a limb type
		if limb:
			self.limb = limb
			limbData = data["limb"][self.limb]
		else:
			if "limb" in data.keys():
				self.limb = random.choice(list(data["limb"].keys()))
				limbData = data["limb"][self.limb]
			else:
				self.limb = random.choice(list(ARMOR_TYPES[self.armorWeight].keys()))
				limbData = ARMOR_TYPES[self.armorWeight][self.limb]

		# Now get limb specific data
		self.nameSuffix:str = random.choice(limbData["name"])
		self.numLimbsRequired:int = limbData["numLimbsRequired"]
		self.numLimbsAllowed:int = limbData["numLimbsAllowed"]
		self.limbDesc:str = limbData["desc"]
	
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
	
	def getWeight(self):
		''' Returns the weight of the armor. '''
		return self.armorWeight
	
	def getLimb(self):
		''' Returns the limb type the armor is for. '''
		return self.limb
	
	def getLimbDesc(self):
		''' Returns the description of the limb the armor is for. '''
		return self.limbDesc
	
	def getNumLimbsRequired(self):
		''' Returns the number of limbs required to wear the armor. '''
		return self.numLimbsRequired
	
	def getNumLimbsAllowed(self):
		''' Returns the number of limbs allowed to wear the armor. '''
		return self.numLimbsAllowed

	def __str__(self):
		return self.getName()

	def __int__(self):
		return self.getDefenceRating()