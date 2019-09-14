import random
import re

class Event(object):
	def __init__(self,data):
		self.id = data["id"]
		self.name = random.choice(data["name"])

		self.start = random.choice(data["start"])
		self.msg = random.choice(data[self.start]["msg"])
		self.actions = data[self.start]["actions"]
		
		self.parts = {}
		for part in data.keys():
			if "#" in part:
				self.parts[part] = data[part]
		
		self.finished = False
	
	def gotoPart(self, partId):
		if partId in self.parts.keys():
			self.msg = random.choice(self.parts[partId]["msg"])
			self.actions = self.parts[partId]["actions"]
		else:
			raise Exception("The next part was not properly setup. Event ID: " + self.id)
	
	def finish(self):
		self.finished = True
	
	def getTag(self, tagData):
		return Tag(tagData)

class Tag(object):
	def __init__(self, data):
		self.id = data["id"]
		self.desc = data["desc"]
		self.value = data["value"]