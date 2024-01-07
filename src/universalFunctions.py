


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