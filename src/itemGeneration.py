
import random
import re

from textGeneration import generateString
from weaponClass import Weapon
from armorClass import Armor


def generateWeapon(data=None, modifiers=None):
    newWeapon = Weapon(data, modifiers)
    if newWeapon.generated:
        newWeapon = _generateWeapon(newWeapon, data)
    return newWeapon

def _generateWeapon(newWeapon=None, data=None):
    newWeapon.name = generateString(data)
    return newWeapon

def generateArmor(data=None, modifiers=None, limb=None):
    newArmor = Armor(data, limb)
    return newArmor

def generateAmorSet(data=None, modifiers=None, limbs=[]):
    newArmors = []
    for limb in limbs:
        newArmors.append(generateArmor(data, modifiers, limb))
    return newArmors