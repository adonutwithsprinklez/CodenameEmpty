
import random

from universalFunctions import evaluate_rule

def evaluateDialogueLine(criteriaList, query):
    queryKeys = query.keys()
    # Checks if all required tags are even in the query
    # Immediately returns False if not
    # (No need to evaluate truth statements then)
    if (set(criteria[0] for criteria in criteriaList) - queryKeys):
        return False

    # Check truth values for each criteria:
    truthTable = []
    for criteria in criteriaList:
        truthTable.append(
            evaluate_rule(criteria[2], criteria[1], query[criteria[0]])
        )
    return all(truthTable)

def getAllPossibleSpeachOptions(speachLines, query):
    possibleSpeachOptions = []
    for line in speachLines:
        if "criteria" in line.keys():
            if evaluateDialogueLine(line["criteria"], query):
                possibleSpeachOptions.append(line)
        else:
            possibleSpeachOptions.append(line)
    return possibleSpeachOptions

def getSatisfactoryDialogueLines(lines, query):
    satisfactoryLines = {
        "lines":[],
        "weights":[]
    }
    for line in lines:
        if evaluateDialogueLine(line["criteria"], query):
            satisfactoryLines["lines"].append(line)
            if "weight" in line.keys():
                satisfactoryLines["weights"].append(line["weight"])
            else:
                satisfactoryLines["weights"].append(1)
    return satisfactoryLines

def getRandomSatisfatoryDialogueLine(lines, query, weighted=True):
    satisfactoryLines = getSatisfactoryDialogueLines(lines, query)
    if len(satisfactoryLines["lines"]) > 0:
        getRandomLine(satisfactoryLines["lines"], satisfactoryLines["weights"])
    else:
        return {"dialogue":"ERR - No dialog line found"}

def getRandomLine(lines, weights=[]):
        if len(weights)>0:
            return random.choices(lines, weights=weights, k=1)[0]
        return random.choice(lines)