
import copy
import random

from dialogueRules import evaluateDialogueLine
from dieClass import rollDice
from raceClass import Race, Limb
from textGeneration import generateString
from universalFunctions import getDataValue

# These are mods that get used in the processEffect function,
# but are not immediately applied to the effect
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
        # Required data
        self.ID = ID
        self.effectID:str = getDataValue("effectID", data, -1)
        self.name:str = getDataValue("name", data, -1)
        self.desc:str = getDataValue("desc", data, -1)

        # Crash immediately to allow for easier debugging,
        # instead of waiting for game to crash
        if self.effectID == -1 or self.name == -1 or self.desc == -1:
            raise ValueError(f"{self.ID} is missing required data.\neffectID:{self.effectID}\nname:{self.name}\ndesc:{self.desc}")

        # Optional data 
        # Could crash if data is not included. Depends on effectID
        self.showDesc:bool = getDataValue("showDesc", data, True)
        self.strength:str = getDataValue("strength", data, "1d6")
        self.duration:str = getDataValue("duration", data, "+0")
        self.durationLeft:int = rollDice(self.duration) * 10
        self.durationInCombat:bool = getDataValue("durationInCombat", data, True)
        self.durationInTravel:bool = getDataValue("durationInTravel", data, True)
        self.repeat:bool = getDataValue("repeat", data, False)
        self.followUpEffects:list = getDataValue("followUpEffects", data, [])
        self.randomFollowUpEffect:bool = getDataValue("randomFollowUpEffect", data, False)
        self.randomFollowUpEffectOnDispel:bool = getDataValue("randomFollowUpEffectOnDispel", data, False)
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
        self.requirements:list = getDataValue("requirements", data, [])
        self.occasionalMessage:bool = getDataValue("occasionalMessage", data, False)
        self.occasionalMessageTimer:str = getDataValue("occasionalMessageChance", data, "1d10+10")
        self.occasionalMessageRepeats:bool = getDataValue("occasionalMessageRepeats", data, True)
        self.occasionalMessageTimeLeft:int = rollDice(self.occasionalMessageTimer) * 10
        self.occasionalMessageFired:bool = False

        '''
        Possible effect lines:
            activated: Message to display when the effect is fired off
            applied: Message to display when effect is applied to a target
            occasionalMessage: A list of random messages that will be played
                when the occasional message timer fires
            wornOff: Message to display when effect wears off of the target
            dispelled: Message to display when effect is dispelled
            heal: Message to display when healing the target
            hurt: Message to display when damaging the target
        '''
        self.effectLines:dict = getDataValue("effectLines", data, {})
    
    def hasColor(self):
        return "color" in self.miscData.keys()
    
    def getColor(self):
        if self.hasColor():
            return self.miscData["color"]
        return "white" # Default value
    
    def getName(self):
        return self.name
    
    def getDesc(self):
        descData = {
            "type":"choose",
            "desc":self.desc,
            "strength":{"type":"choose","choices":[self.getStrength()]},
            "duration":{"type":"choose","choices":[self.duration]},
        }
        return generateString(descData, "desc")
    
    def getEffectLines(self):
        return self.effectLines
    
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
    REMOVED_AFTER = False

    # Check for modifiers that affect the effect 
    for modifier in modifiers:
        if modifier["e"] in MODS_TO_STORE:
            allowModifierRepeats = getDataValue("allowModifierRepeats", effect.miscData, False)
            if allowModifierRepeats or modifier["e"] not in effect.modifiers:
                effect.modifiers.append(modifier)
        elif modifier["e"] == "longEffect":
            time -= rollDice(modifier["s"])
        elif modifier["e"] == "shortEffect":
            time += rollDice(modifier["s"])
    
    if time < 0:
        time = 0
    
    # See if the target is the player, and grab call the player's query
    # function to see if it meets all requirements to keep the effect
    if type(target).__name__ == "Player":
        query = target.getPlayerQuery()
        meetsRequirements = evaluateDialogueLine(effect.requirements, query)
        if not meetsRequirements:
            if effect in target.effects:
                target.effects.remove(effect)
            effect.durationLeft = 0
            if "dispelled" in effect.effectLines.keys():
                messages.append(copy.copy(effect.effectLines["dispelled"]))
            elif effect.useDefaultMessages:
                messages.append(copy.copy(f"{effect.name} dissipates within {target.name}."))
            if not effect.randomFollowUpEffectOnDispel:
                return messages
            else:
                REMOVED_AFTER = True

    # Check if effect has overwrites
    # Use first in first out for overwrites
    for overwrite in reversed(effect.overwrites):
        for currentEffect in target.effects:
            if currentEffect == effect:
                continue
            if currentEffect.ID == overwrite["ID"]:
                # Check if the overwrite needs to be a longer duration
                if overwrite["onlyIfLongerDuration"] and ((currentEffect.durationLeft > effect.durationLeft and not effect.permanent) or currentEffect.permanent):
                    if effect in target.effects:
                        target.effects.remove(effect)
                    effect.durationLeft = 0
                    messages.append(copy.copy(f"{target.name} does nothing due to {currentEffect.name}."))
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
            messages.append(copy.copy(effect.effectLines["activated"]))
        elif effect.useDefaultMessages:
            messages.append(copy.copy(f"{effect.name} has been activated."))
        
        # Healing effect
        if effect.effectID == "heal":
            target.giveHP(strengthRoll)
            if "heal" in effect.effectLines.keys():
                messages.append(copy.copy(effect.effectLines["heal"]))
            elif effect.useDefaultMessages:
                messages.append(copy.copy(f"{target.name} was healed for {strengthRoll} HP."))
        
        # Damage effect
        elif effect.effectID == "hurt":
            target.takeHP(strengthRoll)
            if "hurt" in effect.effectLines.keys():
                messages.append(copy.copy(effect.effectLines["hurt"]))
            elif effect.useDefaultMessages:
                messages.append(copy.copy(f"{target.name} took {strengthRoll} damage."))
        
        # Race transformation effect
        elif effect.effectID == "race_transform":
            # Remove any temporary transformations
            for currentEffect in target.effects:
                if currentEffect.effectID == "race_transform_temp":
                    target.Effects.remove(currentEffect)
            race = Race(gameData["races"][effect.miscData["race"]])
            # Make sure the race is actually playable
            if race.playable:
                target.setRace(race)
                messages.append(copy.copy(f"{target.name} has transformed into a {target.getRace().getName(False)}."))
        
        # Temporary Race transformation effect
        elif effect.effectID == "race_transform_temp":
            allowTempTransformation = True
            for currentEffect in target.effects:
                if currentEffect.effectID == "race_transform_temp" and effect != currentEffect:
                    allowTempTransformation = False
                elif currentEffect.effectID == "body_part_temp":
                    allowTempTransformation = False
            if allowTempTransformation:
                race = Race(gameData.getGameData("race", effect.miscData["race"]))
                # Make sure the race is playable
                if not race.playable:
                    messages = [f"This form is not compatible with {target.name}'s soul."]
                    effect.durationLeft = 0
                    return messages
                # Otherwise, set the race
                target.setRace(race, False, True)
                messages.append(copy.copy(f"{target.name} has transformed into a {target.getRace().getName(False)}."))
            else:
                messages = [copy.copy(f"{target.name}'s current effects block them from transforming.")]
                effect.durationLeft = 0
                return messages
        
        # Temporary limb effect
        elif effect.effectID == "body_part_temp":
            numLimbs = rollDice(effect.miscData["count"])
            repeat = effect.miscData["repeat"]
            possibleLimbData = effect.miscData["bodyPart"]
            for i in range(numLimbs):
                if len(possibleLimbData) > 0:
                    limbData = random.choice(possibleLimbData)
                    # Get possible limbs that meet criteria from race game data
                    raceData = gameData["races"][limbData["race"]]
                    possibleRaceLimbs = []
                    for limb in raceData["limbs"]:
                        if limb["type"] == limbData["type"]:
                            possibleRaceLimbs.append(limb)
                    if len(possibleRaceLimbs) > 0:
                        limb = Limb(random.choice(possibleRaceLimbs))
                        limbsToAdd = [limb] * rollDice(limbData["count"])
                        for limbToAdd in limbsToAdd:
                            if limbData["replace"]:
                                pass
                            else:
                                target.tempAddedLimbs.append(limbToAdd)
                    if repeat:
                        possibleLimbData.remove(limbData)

    
    # Process duration
    if effect.durationLeft > 0:
        if "permanentEffects" not in target.flags:
            effect.durationLeft -= time
        if effect.occasionalMessage:
            if effect.occasionalMessageTimeLeft <= 0 and (effect.occasionalMessageRepeats or not effect.occasionalMessageFired):
                # Time to display random message
                messages.append(random.choice(copy.copy(effect.effectLines["occasionalMessage"])))
                effect.occasionalMessageTimeLeft = rollDice(effect.occasionalMessageTimer) * 10
                effect.occasionalMessageFired = True
            else:
                # Decrement time
                effect.occasionalMessageTimeLeft -= time

    elif effect.durationLeft <= 0 and (effect in target.effects or REMOVED_AFTER) and not effect.permanent:
        # Check if effect needs any final processing
        if effect.effectID == "race_transform_temp":
            target.setRace(target.previousRace)
            messages.append(copy.copy(f"{target.name} has reverted to their previous form."))
        elif effect.effectID == "body_part_temp":
            for limb in target.tempAddedLimbs:
                target.tempAddedLimbs.remove(limb)

        # Remove effect
        if not REMOVED_AFTER:
            target.effects.remove(effect)
        if "wornOff" in effect.effectLines.keys():
            messages.append(copy.copy(effect.effectLines["wornOff"]))
        elif effect.useDefaultMessages:
            messages.append(copy.copy(f"{effect.name} has worn off."))
        # Chcek for follow up effects
        if not effect.randomFollowUpEffect:
            for followUpEffect in effect.followUpEffects:
                newEffect = Effect(followUpEffect, target.gameData.getGameData("effect", followUpEffect))
                target.effects.append(newEffect)
                if "applies" in effect.effectLines.keys():
                    messages.append(copy.copy(effect.effectLines["applies"]))
                if "applied" in newEffect.effectLines.keys():
                    messages.append(copy.copy(newEffect.effectLines["applied"]))
                elif newEffect.useDefaultMessages:
                    messages.append(copy.copy(f"{newEffect.name} has been applied to {target.name}."))
        else:
            e = random.choice(effect.followUpEffects)
            if e.lower() != "none":
                newEffect = Effect(e, target.gameData.getGameData("effect", e))
                target.effects.append(newEffect)
                if "applies" in effect.effectLines.keys():
                    messages.append(copy.copy(effect.effectLines["applies"]))
                if "applied" in newEffect.effectLines.keys():
                    messages.append(copy.copy(newEffect.effectLines["applied"]))
                elif newEffect.useDefaultMessages:
                    messages.append(copy.copy(f"{newEffect.name} has been applied to {target.name}."))
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