
def getDataValue(variable, data, default):
    """
    Retrieves the value of a variable from a dictionary, or returns a default value if the variable is not found.

    Args:
        variable (str): The variable to retrieve from the dictionary.
        data (dict): The dictionary containing the variable.
        default: The default value to return if the variable is not found.

    Returns:
        The value of the variable if found in the dictionary, otherwise the default value.
    """
    if variable in data.keys():
        return data[variable]
    else:
        return default


# Evaluators
def _evaluateEqualsRule(criteria, query):
    return criteria == query

def _evaluateNotEqualsRule(criteria, query):
    return criteria != query

def _evaluateGreaterThanRule(criteria, query):
    return criteria < query

def _evaluateLessThanRule(criteria, query):
    return criteria > query

def _evaluateGreaterThanEqualRule(criteria, query):
    return criteria <= query

def _evaluateLessThanEqualRule(criteria, query):
    return criteria >= query

def _evaluateHasRule(criteria, query):
    return criteria in query

def _evaluateNotHasRule(criteria, query):
    return not criteria in query

TRUTHRULES = {
    "=":_evaluateEqualsRule,
    "!=":_evaluateNotEqualsRule,
    ">":_evaluateGreaterThanRule,
    "<":_evaluateLessThanRule,
    ">=":_evaluateGreaterThanEqualRule,
    "<=":_evaluateLessThanEqualRule,
    "has":_evaluateHasRule,
    "nothas":_evaluateNotHasRule
}

def evaluate_rule(critera, evaluation, value) -> bool:
    return TRUTHRULES[evaluation](critera, value)



# Modifiers
def _modifyFlagAdd(value, addition=1):
    return value + addition

def _modifyFlagSubtract(value, subtraction=1):
    return value - subtraction

def _modifyFlagSet(value, newValue):
    return newValue

def _modifyFlagMultiply(value, multiplier=1):
    return value * multiplier

def _modifyFlagDivide(value, divisor=1):
    return value / divisor

def _modifyFlagModulo(value, divisor=1):
    return value % divisor

def _modifyFlagExponent(value, exponent=1):
    return value ** exponent

def _modifyFlagAppend(value, addition=""):
    if addition not in value:
        value.append(addition)
    return value

def _modifyFlagRemove(value, removal=""):
    if removal in value:
        value.remove(removal)
    return value

FLAGMODIFIERS = {
    "+":_modifyFlagAdd,
    "-":_modifyFlagSubtract,
    "set":_modifyFlagSet,
    "*":_modifyFlagMultiply,
    "/":_modifyFlagDivide,
    "%":_modifyFlagModulo,
    "**":_modifyFlagExponent,
    "append":_modifyFlagAppend,
    "remove":_modifyFlagRemove
}

def modifyFlag(flag, modifier, value):
    return FLAGMODIFIERS[modifier](flag, value)