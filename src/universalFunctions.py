


def getDataValue(variable, data, default):
    if variable in data.keys():
        return data[variable]
    else:
        return default