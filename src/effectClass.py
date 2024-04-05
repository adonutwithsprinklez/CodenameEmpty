
from dieClass import rollDice
from raceClass import Race
from textGeneration import generateString
from universalFunctions import getDataValue

class Effect(object):
    def __init__(self, data):
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
        self.effectID:str = getDataValue("effectID", data, "Err Loading Effect ID")
        self.name:str = getDataValue("name", data, "Err Loading Effect Name")
        self.desc:str = getDataValue("desc", data, "Err Loading Effect Desc")
        self.strength:str = getDataValue("strength", data, "1d6")
        self.duration:str = getDataValue("duration", data, "+0")
        self.durationLeft:int = rollDice(self.duration)
        self.durationInCombat:bool = getDataValue("durationInCombat", data, True)
        self.durationInTravel:bool = getDataValue("durationInTravel", data, True)
        self.repeat:bool = getDataValue("repeat", data, False)
        self.followUpEffects:list = getDataValue("followUpEffects", data, [])
        self.modifiers:list = getDataValue("modifiers", data, [])
        self.hidden:bool = getDataValue("hidden", data, False)
        self.hiddenDuration:bool = getDataValue("hiddenDuration", data, False)
        self.hiddenMessages:bool = getDataValue("hiddenMessages", data, False)
        self.chance:str = getDataValue("chance", data, "+0")
        self.immediate:bool = getDataValue("immediate", data, False)
        self.miscData:dict = getDataValue("miscData", data, {})
        self.permanent:bool = getDataValue("permanent", data, False)

        '''
        Possible effect lines:
            activated: Message to display when the effect is fired off
            applied: Message to display when effect is applied to a target
            wornOff: Message to display when effect wears off of the target
        '''
        self.effectLines:dict = getDataValue("effectLines", data, {})

    def rollStrength(self):
        return rollDice(self.strength)
    
    def rollChance(self):
        return rollDice(self.chance)
    
    def getFlags(self):
        if "flags" in self.miscData.keys():
            return self.miscData["flags"]
        return []

    def getPerks(self):
        if "perks" in self.miscData.keys():
            return self.miscData["perks"]
        return []


def processEffect(effect, target, gameData):
    '''Process an effect on a target, return messages to display to the player.'''
    messages = []

    # Process initial effect
    if effect.repeat or not effect.started:
        effect.started = True
        if "activated" in effect.effectLines.keys():
            messages.append(effect.effectLines["activated"])
        if effect.effectID == "heal":
            healing = effect.rollStrength()
            target.giveHP(healing)
            messages.append(f"{target.name} was healed for {healing} HP.")
        elif effect.effectID == "race_transform":
            # Remove any temporary transformations
            for currentEffect in target.effects:
                if currentEffect.effectID == "race_transform_temp":
                    target.Effects.remove(currentEffect)
            race = Race(gameData["races"][effect.miscData["race"]])
            target.setRace(race)
            messages.append(f"{target.name} has transformed into a {target.getRace().getName(False)}.")
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
        time = 1
        # TODO allow modifiers/target flags to affect duration
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
        else:
            messages.append(f"{effect.name} has worn off.")
        # Chcek for follow up effects
        for followUpEffect in effect.followUpEffects:
            newEffect = Effect(target.gameData["effects"][followUpEffect])
            target.effects.append(newEffect)
            if "applied" in newEffect.effectLines.keys():
                messages.append(newEffect.effectLines["applied"])
            else:
                messages.append(f"{newEffect.name} has been applied to {target.name}.")
    if effect.hiddenMessages:
        messages = []
    return messages

def processAppliedEffects(target, combat=False, travelling=False):
    messages = []
    for effect in target.effects:
        if (effect.durationInCombat and combat) or (effect.durationInTravel and travelling):
            newMessages = processEffect(effect, target, target.gameData)
            messages.extend(newMessages)
    return messages