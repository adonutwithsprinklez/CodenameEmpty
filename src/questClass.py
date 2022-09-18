import random


class Flag(object):
	def __init__(self,data=[]):
		self.fID = data[0]
		self.requirement = data[1]
		self.fulfilled = False

	def __str__(self):
		return "%s - %s - %s" % (self.fID, self.requirement, self.fulfilled)


class Quest(object):
	qNum = 0 # Static variable used to make sure qID's are distinct
	def __init__(self,data={}):
		Quest.qNum += 1
		self.qID = data["qID"] + str(Quest.qNum)
		self.title = data["title"]
		self.desc  = data["desc"]
		self.hidden = False
		self.complete = False
		self.started = False
		self.spawnConditions = []
		for f in data["spawnConditions"]:
			self.spawnConditions.append(Flag(f))
		self.spawnChance = data["spawnChance"]
		self.do = data["do"]
		self.requirements = []
		self.nextStep = data["nextStep"]

	def setFlagToValue(self,fID,requirement,valueIfTrue=True,valueIfFalse=False):
		if not self.started:
			for f in self.spawnConditions:
				if f.fID == fID:
					if f.requirement == requirement:
						f.fulfilled = valueIfTrue
					else:
						f.fulfilled = valueIfFalse
		elif self.started:
			for f in self.requirements:
				if f.fID == fID:
					if f.requirement == requirement:
						f.fulfilled = valueIfTrue
					else:
						f.fulfilled = valueIfFalse

	def doNextStep(self):
		for f in self.requirements:
			if not f.fulfilled:
				return False
		return self.getDo()

	def start(self):
		if not self.started and random.randint(0,10) < self.spawnChance:
			for f in self.spawnConditions:
				if not f.fulfilled:
					return False
			self.started = True
			return self.getDo()
		return False

	def getDo(self):
		do = self.do
		if self.nextStep:
			nextStep = self.nextStep
			if "nextStep" in nextStep.keys():
				self.nextStep = nextStep["nextStep"]
			self.do = nextStep["do"]
			self.requirements = nextStep["requirements"]
			requirements = []
			for f in self.requirements:
				requirements.append(Flag(f))
			self.requirements = requirements
		for action in do:
			print(action)
			if action[0] == "setDesc":
				self.desc = action[1]
			elif action[0] == "hideFromQuestLog":
				self.hidden = action[1]
			else:
				action.append(self.qID)
		return do

	def __str__(self):
		return "Quest: %-30s | Started: %-5s | Complete: %-5s" % (self.title,self.started,self.complete)
