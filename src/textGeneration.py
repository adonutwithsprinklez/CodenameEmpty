
import random
import re

def generateString(data=None, tag="name"):
    nameString = random.choice(data[tag])
    result = re.findall("\\B\\$\\w+", nameString)
    for command in result:
        addition = command[1:] # removes the $ from the command
        replacementData = data[addition] # Get the command data that will be used to generate the replacement text
        if replacementData["type"] == "markov":
            replacement = _makeMarkovChain(replacementData)
        elif replacementData["type"] == "choose":
            replacement = random.choice(replacementData["choices"])
        nameString = nameString.replace(command, replacement)
    return nameString

def generateDescription(descriptors, numDescriptorsToUse = 1):
    string = ""
    for i in range(numDescriptorsToUse):
        string += random.choice(descriptors).getString()
    return string

def _makeMarkovChain(dataInput=None):
    chain = ""
    if dataInput["markovType"] == "data":
        chain = _makeMarkovChainFromData(dataInput)
    return chain

def _makeMarkovChainFromData(data=None):
    stringFinished = False
    while not stringFinished:
        # Set the start of the string
        finalString = random.choice(data["starters"])

        # Make the middle of the string
        addSection = True
        addedSections = 0
        while addSection and addedSections < data["maxMiddleLength"]:
            lastCharacters = finalString[-2:]
            if not lastCharacters.lower() in data["middles"].keys() and lastCharacters.lower() in data["ends"].keys():
                addSection = False
                stringFinished = True
            elif lastCharacters.lower() in data["ends"].keys() and random.random() < 0.30 and addedSections > data["minMiddleLength"]:
                addSection = False
                stringFinished = True
            elif lastCharacters.lower() in data["middles"].keys():
                finalString += random.choice(data["middles"][lastCharacters.lower()])
                addedSections += 1
            else:
                # The string failed to be finished properly
                addSection = False

        # Set the end of the string
        lastCharacters = finalString[-2:]
        if lastCharacters.lower() in data["ends"].keys() and random.random() < .75:
            finalString += random.choice(data["ends"][lastCharacters.lower()])
        if not stringFinished and data["allowFailed"]:
            stringFinished = True
    return finalString