import json
def loadJson(objFile):
	'''This functions returns a dictionary object with the data found in the specified json file.'''
	return json.loads(open(objFile,"r").read())
def saveJson(objFile, obj):
	'''Saves the passed object as a dictionary object in the passed file location.'''
	json.dump(obj, open(objFile, "w"), indent=4)