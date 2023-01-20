
def _evaluateEqualsRule(criteria, query):
    return criteria == query

def _evaluateNotEqualsRule(criteria, query):
    return criteria != query

def _evaluateGreaterThanRule(criteria, query):
    return criteria > query

def _evaluateLessThanRule(criteria, query):
    return criteria < query

def _evaluateHasRule(criteria, query):
    return criteria in query

TRUTHRULES = {
    "=":_evaluateEqualsRule,
    "!=":_evaluateNotEqualsRule,
    ">":_evaluateGreaterThanRule,
    "<":_evaluateLessThanRule,
    "has":_evaluateHasRule
}

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
            TRUTHRULES[criteria[1]](criteria[2], query[criteria[0]])
        )
    return all(truthTable)

def getSatisfactoryDialogueLines(lines, query):
    satisfactoryLines = []
    for line in lines:
        if evaluateDialogueLine(line["criteria"], query):
            satisfactoryLines.append(line)
    return satisfactoryLines