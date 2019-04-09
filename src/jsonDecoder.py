import json
def loadJson(objFile):
	'''This functions returns a dictionary object with the data found in the specified json file.'''
	return json.loads(open(objFile,"r").read())