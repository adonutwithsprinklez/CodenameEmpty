
import random
import re

from armorClass import Armor
from miscClass import Misc
from textGeneration import generateString
from weaponClass import Weapon


def generateItem(itemId, gameData, limb=None):
    if itemId in gameData.getListOfKeys("armor"):
        return generateArmor(gameData.getGameData("armor",itemId), gameData, limb)
    elif itemId in gameData.getListOfKeys("misc"):
        return generateMisc(gameData.getGameData("misc",itemId), gameData)
    elif itemId in gameData.getListOfKeys("weapon"):
        return generateWeapon(itemId, gameData)
    return None

def generateArmor(data=None, gameData=None, limb=None):
    newArmor = Armor(data, limb, gameData)
    return newArmor

def generateAmorSet(data=None, gameData=None, limbs=[]):
    newArmors = []
    for limb in limbs:
        newArmors.append(generateArmor(data, gameData, limb))
    return newArmors

def generateMisc(data=None, gameData=None):
    newMisc = Misc(data, gameData)
    return newMisc

def generateWeapon(name=None, gameData=None):
    newWeapon = Weapon(name, gameData)
    if newWeapon.generated:
        newWeapon = _generateWeapon(newWeapon, gameData.getGameData("weapon", name))
    return newWeapon

def _generateWeapon(newWeapon=None, data=None):
    newWeapon.name = generateString(data)
    return newWeapon