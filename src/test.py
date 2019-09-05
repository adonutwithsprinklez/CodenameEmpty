

from itemGeneration import generateName
from jsonDecoder import loadJson

data = loadJson("res/official/weapons/template_IronSword.json")

for i in range(10):
    print(generateName(data))