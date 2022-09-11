import tomllib

'''
Retuires Python 3.11.x
tomllib is not supplied in earlier Python versions.
'''

def loadToml(objFile):
    '''Returns a dictionary object with the data in the specified toml file.'''
    return tomllib.loads(open(objFile,"r").read())