
import random
import re

from textGeneration import generateString
from weaponClass import Weapon


def generateWeapon(data=None, modifiers=None):
    newWeapon = Weapon(data, modifiers)
    if newWeapon.generated:
        newWeapon = _generateWeapon(newWeapon, data)
    return newWeapon

def _generateWeapon(newWeapon=None, data=None):
    newWeapon.name = generateString(data)
    return newWeapon
