import random
from armorClass import Armor
from miscClass import Misc
from weaponClass import Weapon


class Event(object):
	def __init__(self,data,weapons,armor,misc):
		self.name    = random.choice(data["name"])
		self.msg     = random.choice(data["msg"])
		self.actions = random.choice(data["actions"])
		for k in self.actions.keys():
			if type(self.actions[k]).__name__ == "dict":
				t = random.choice(self.actions[k]["reward"].keys())
				self.actions[k]["reward"] = random.choice(self.actions[k]["reward"][t])
				if t == "weapon":
					self.actions[k]["reward"] = Weapon(weapons[self.actions[k]["reward"]])
				elif t == "armor":
					self.actions[k]["reward"] = Armor(armor[self.actions[k]["reward"]])
				elif t == "misc":
					self.actions[k]["reward"] = Misc(misc[self.actions[k]["reward"]])
			else:
				self.actions[k] = {
					"msg":self.actions[k],
					"reward":0
				}