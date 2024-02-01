
import random
import re

from armorClass import Armor
from miscClass import Misc
from textGeneration import generateString
from weaponClass import Weapon


def generateItem(itemId, armorData, miscData, weaponData, modifiers, limb=None):
    if itemId in armorData.keys():
        return generateArmor(armorData[itemId], modifiers, limb)
    if itemId in miscData.keys():
        return generateMisc(miscData[itemId], modifiers)
    if itemId in weaponData.keys():
        return generateWeapon(weaponData[itemId], modifiers)
    return None

def generateArmor(data=None, modifiers=None, limb=None):
    newArmor = Armor(data, limb, modifiers)
    return newArmor

def generateAmorSet(data=None, modifiers=None, limbs=[]):
    newArmors = []
    for limb in limbs:
        newArmors.append(generateArmor(data, modifiers, limb))
    return newArmors

def generateMisc(data=None, modifiers=None):
    newMisc = Misc(data, modifiers)
    return newMisc

def generateWeapon(data=None, modifiers=None):
    newWeapon = Weapon(data, modifiers)
    if newWeapon.generated:
        newWeapon = _generateWeapon(newWeapon, data)
    return newWeapon

def _generateWeapon(newWeapon=None, data=None):
    newWeapon.name = generateString(data)
    return newWeapon