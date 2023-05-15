import orjson as json
def loadJson(objFile):
	'''This functions returns a dictionary object with the data found in the specified json file.'''
	return json.loads(open(objFile,"r").read())
def saveJson(objFile, obj):
	'''Saves the passed object as a dictionary object in the passed file location.'''
	data = json.dumps(obj, option=json.OPT_INDENT_2)
	# open objFile and write the data to it
	with open(objFile, "wb") as f:
		f.write(data)