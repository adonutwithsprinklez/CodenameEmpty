# Writing Effects


# effectClass.py

This module defines the `Effect` class and functions to process effects on targets in a game. The `Effect` class encapsulates various attributes and behaviors of an effect, while the functions handle the application and processing of these effects.

## Classes

### Effect

Represents an effect that can be applied to a target.

#### Attributes

- `ID`: The identifier for the effect.
- `effectID`: The specific effect ID.
- `name`: The name of the effect.
- `desc`: The description of the effect.
- `showDesc`: Whether to show the description.
- `strength`: The strength of the effect.
- `duration`: The duration of the effect.
- `durationLeft`: The remaining duration of the effect.
- `durationInCombat`: Whether the effect duration is counted in combat.
- `durationInTravel`: Whether the effect duration is counted in travel.
- `repeat`: Whether the effect repeats.
- `followUpEffects`: List of follow-up effects.
- `modifiers`: List of modifiers affecting the effect.
- `hidden`: Whether the effect is hidden.
- `hiddenDuration`: Whether the duration is hidden.
- `hiddenMessages`: Whether the messages are hidden.
- `useDefaultMessages`: Whether to use default messages.
- `appliable`: Whether the effect is appliable.
- `removeAfterApply`: Whether to remove the effect after applying.
- `chance`: The chance of the effect occurring.
- `immediate`: Whether the effect is immediate.
- `miscData`: Miscellaneous data related to the effect.
- `permanent`: Whether the effect is permanent.
- `overwrites`: List of effects that this effect overwrites.
- `effectLines`: Dictionary of messages for different effect states.

#### Methods

- `__init__(self, ID, data)`: Initializes an effect with the given ID and data.
- `hasColor(self)`: Checks if the effect has a color.
- `getColor(self)`: Gets the color of the effect.
- `getName(self)`: Gets the name of the effect.
- `getDesc(self)`: Gets the description of the effect.
- `getTimeLeft(self)`: Gets the remaining time of the effect.
- `getChance(self)`: Gets the chance of the effect occurring.
- `getStrength(self)`: Gets the strength of the effect.
- `rollStrength(self, withModifiers=True)`: Rolls the strength of the effect.
- `rollChance(self, withModifiers=True)`: Rolls the chance of the effect occurring.
- `getFlags(self)`: Gets the flags associated with the effect.
- `getPerks(self)`: Gets the perks associated with the effect.

## Functions

### processEffect(effect, target, gameData, modifiers=[])

Processes an effect on a target and returns messages to display to the player.

#### Parameters

- `effect`: The effect to process.
- `target`: The target of the effect.
- `gameData`: The game data.
- `modifiers`: List of modifiers affecting the effect.

#### Returns

- `messages`: List of messages to display to the player.

### processAppliedEffects(target, combat=False, travelling=False, modifiers=[])

Processes all applied effects on a target and returns messages to display to the player.

#### Parameters

- `target`: The target of the effects.
- `combat`: Whether the target is in combat.
- `travelling`: Whether the target is travelling.
- `modifiers`: List of modifiers affecting the effects.

#### Returns

- `messages`: List of messages to display to the player.