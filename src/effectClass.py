
from dieClass import rollDice
from raceClass import Race
from textGeneration import generateString
from universalFunctions import getDataValue

MODS_TO_STORE = [
    "improvedEffect",
    "impairedEffect"
]

class Effect(object):
    def __init__(self, ID, data):
        self.started = False
        '''
        Possible effect IDs:
            heal: Heals the target for a certain amount
            hurt: Damages the target for a certain amount
            race_transform: Transforms the target into the race specified in miscData["race"]
                Also removes any temporary transformation effects from the target
            race_transform_temp: Temporarily transforms the target into the race specified in misc["race"]
                Only one temporary transformation can be active at a time
            lycanthropy: Affects stats and abilities of the target
        '''
        self.ID = ID
        self.effectID:str = getDataValue("effectID", data, "Err Loading Effect ID")
        self.name:str = getDataValue("name", data, "Err Loading Effect Name")
        self.desc:str = getDataValue("desc", data, "Err Loading Effect Desc")
        self.showDesc:bool = getDataValue("showDesc", data, True)
        self.strength:str = getDataValue("strength", data, "1d6")
        self.duration:str = getDataValue("duration", data, "+0")
        self.durationLeft:int = rollDice(self.duration) * 10
        self.durationInCombat:bool = getDataValue("durationInCombat", data, True)
        self.durationInTravel:bool = getDataValue("durationInTravel", data, True)
        self.repeat:bool = getDataValue("repeat", data, False)
        self.followUpEffects:list = getDataValue("followUpEffects", data, [])
        self.modifiers:list = getDataValue("modifiers", data, [])
        self.hidden:bool = getDataValue("hidden", data, False)
        self.hiddenDuration:bool = getDataValue("hiddenDuration", data, False)
        self.hiddenMessages:bool = getDataValue("hiddenMessages", data, False)
        self.useDefaultMessages:bool = getDataValue("useDefaultMessages", data, True)
        self.appliable:bool = getDataValue("appliable", data, False)
        self.removeAfterApply:bool = getDataValue("removeAfterApply", data, False)
        self.chance:str = getDataValue("chance", data, "1d10;-1d10")
        self.immediate:bool = getDataValue("immediate", data, False)
        self.miscData:dict = getDataValue("miscData", data, {})
        self.permanent:bool = getDataValue("permanent", data, False)
        self.overwrites:list = getDataValue("overwrites", data, [])
        self.modifiers:list = getDataValue("modifiers", data, [])

        '''
        Possible effect lines:
            activated: Message to display when the effect is fired off
            applied: Message to display when effect is applied to a target
            wornOff: Message to display when effect wears off of the target
        '''
        self.effectLines:dict = getDataValue("effectLines", data, {})
    
    def getDesc(self):
        descData = {
            "type":"choose",
            "desc":self.desc,
            "strength":{"type":"choose","choices":[self.getStrength()]},
            "duration":{"type":"choose","choices":[self.duration]},
        }
        return generateString(descData, "desc")
    
    def getTimeLeft(self):
        timeLeft = self.durationLeft // 10
        return timeLeft
    
    def getChance(self):
        chance = self.chance
        for modifier in self.modifiers:
            if modifier["e"] == "improvedChance":
                chance += f"+{modifier['s']}"
            elif modifier["e"] == "impairedChance":
                chance += f"-{modifier['s']}"
        return chance
    
    def getStrength(self):
        strength = self.strength
        for modifier in self.modifiers:
            if modifier["e"] == "improvedEffect":
                strength += f";{modifier['s']}"
            elif modifier["e"] == "impairedEffect":
                strength += f";-{modifier['s']}"
        return strength

    def rollStrength(self, withModifiers=True):
        if withModifiers:
            strength = self.getStrength()
        else:
            strength = self.strength
        print(strength)
        return rollDice(strength)
    
    def rollChance(self, withModifiers=True):
        if withModifiers:
            chance = self.getChance()
        else:
            chance = self.chance
        return rollDice(chance)
    
    def getFlags(self):
        if "flags" in self.miscData.keys():
            return self.miscData["flags"]
        return []

    def getPerks(self):
        if "perks" in self.miscData.keys():
            return self.miscData["perks"]
        return []


def processEffect(effect, target, gameData, modifiers=[]):
    '''Process an effect on a target, return messages to display to the player.'''
    messages = []
    time = 10

    # Check for modifiers that affect the effect
    for modifier in modifiers:
        if modifier["e"] in MODS_TO_STORE:
            allowModifierRepeats = False
            if "allowModifierRepeats" in effect.miscData.keys():
                allowModifierRepeats = effect.miscData["allowModifierRepeats"]
            if allowModifierRepeats or modifier["e"] not in effect.modifiers:
                effect.modifiers.append(modifier)
        elif modifier["e"] == "longEffect":
            time -= rollDice(modifier["s"])
        elif modifier["e"] == "shortEffect":
            time += rollDice(modifier["s"])
    
    if time < 0:
        time = 0

    # Check if effect has overwrites
    for overwrite in effect.overwrites:
        for currentEffect in target.effects:
            if currentEffect == effect:
                continue
            if currentEffect.ID == overwrite["ID"]:
                # Check if the overwrite needs to be a longer duration
                if overwrite["onlyIfLongerDuration"] and currentEffect.durationLeft > effect.durationLeft:
                    if effect in target.effects:
                        target.effects.remove(effect)
                    effect.durationLeft = 0
                    messages.append(f"{target.name} does nothing due to {currentEffect.name}.")
                else:
                    # Overwrite the old effect
                    target.effects.remove(currentEffect)
                return messages

    # Process initial effect
    if effect.repeat or not effect.started:
        effect.started = True
        strengthRoll = effect.rollStrength(True)
        allowNegatives = False
        if "allowNegatives" in effect.miscData.keys():
            allowNegatives = effect.miscData["allowNegatives"]
        if strengthRoll < 0 and not allowNegatives:
            strengthRoll = 0

        if "activated" in effect.effectLines.keys():
            messages.append(effect.effectLines["activated"])
        elif effect.useDefaultMessages:
            messages.append(f"{effect.name} has been activated.")
        
        # Healing effect
        if effect.effectID == "heal":
            target.giveHP(strengthRoll)
            if "heal" in effect.effectLines.keys():
                messages.append(effect.effectLines["heal"])
            elif effect.useDefaultMessages:
                messages.append(f"{target.name} was healed for {strengthRoll} HP.")
        
        # Damage effect
        elif effect.effectID == "hurt":
            target.takeHP(strengthRoll)
            if "hurt" in effect.effectLines.keys():
                messages.append(effect.effectLines["hurt"])
            elif effect.useDefaultMessages:
                messages.append(f"{target.name} took {strengthRoll} damage.")
        
        # Race transformation effect
        elif effect.effectID == "race_transform":
            # Remove any temporary transformations
            for currentEffect in target.effects:
                if currentEffect.effectID == "race_transform_temp":
                    target.Effects.remove(currentEffect)
            race = Race(gameData["races"][effect.miscData["race"]])
            target.setRace(race)
            messages.append(f"{target.name} has transformed into a {target.getRace().getName(False)}.")
        
        # Temporary R ace transformation effect
        elif effect.effectID == "race_transform_temp":
            allowTempTransformation = True
            for currentEffect in target.effects:
                if currentEffect.effectID == "race_transform_temp" and effect != currentEffect:
                    allowTempTransformation = False
            if allowTempTransformation:
                race = Race(gameData["races"][effect.miscData["race"]])
                target.setRace(race, False, True)
                messages.append(f"{target.name} has transformed into a {target.getRace().getName(False)}.")
            else:
                messages = [f"{target.name}'s current effects block them from transforming."]
                effect.durationLeft = 0
                return messages
    
    # Process duration
    if effect.durationLeft > 0:
        if "permanentEffects" not in target.flags:
            effect.durationLeft -= time
    elif effect.durationLeft <= 0 and effect in target.effects and not effect.permanent:
        # Check if effect needs any final processing
        if effect.effectID == "race_transform_temp":
            target.setRace(target.previousRace)
            messages.append(f"{target.name} has reverted to their previous form.")

        # Remove effect
        target.effects.remove(effect)
        if "wornOff" in effect.effectLines.keys():
            messages.append(effect.effectLines["wornOff"])
        elif effect.useDefaultMessages:
            messages.append(f"{effect.name} has worn off.")
        # Chcek for follow up effects
        for followUpEffect in effect.followUpEffects:
            newEffect = Effect(followUpEffect, target.gameData["effects"][followUpEffect])
            target.effects.append(newEffect)
            if "applies" in effect.effectLines.keys():
                messages.append(effect.effectLines["applies"])
            if "applied" in newEffect.effectLines.keys():
                messages.append(newEffect.effectLines["applied"])
            elif newEffect.useDefaultMessages:
                messages.append(f"{newEffect.name} has been applied to {target.name}.")
    if effect.hiddenMessages:
        messages = []
    return messages

def processAppliedEffects(target, combat=False, travelling=False, modifiers=[]):
    messages = []
    for effect in target.effects:
        if (effect.durationInCombat and combat) or (effect.durationInTravel and travelling):
            newMessages = processEffect(effect, target, target.gameData, modifiers)
            messages.extend(newMessages)
    return messages