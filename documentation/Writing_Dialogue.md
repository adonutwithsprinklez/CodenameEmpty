# Writing Dialogue

*Written 23.5.24*

This document goes over how dialogue files, and how dialogue lines are structured, along with all of the optional options that can be used.

# Intro

## What does a Dialogue File Look Like?

    {
        "lines":[
            {"dialogue":"*Barks*", "criteria":[["isAction","=","idle"], ["playerPerks","nothas","Animal Speech"]]},
            {"dialogue":"\"Hi there!\"", "criteria":[["isAction","=","idle"], ["playerPerks","has","Animal Speech"]]},
            {"dialogue":"*Growls*", "criteria":[["isAction","=","pet"]]}
        ],
        "otherDialogueOptions":[
            {"option":"Pet dog","isAction":"pet","playerDialogue":"You pet it."}
        ],
        "flags":["additionalDialogue"]
    }

The above is an example of what a "full" dialogue file looks like. While this dialogue file on its own would not be enough to allow the player to have a full conversation with an NPC, it would be enough to act as a dialogue supplement.

In this example there are three main tags to take note of:

- "lines" – A required tag that contains a list of all of the actual dialogue that the NPC might say
- "otherDialogueOptions" – An optional tag containing a list of additional actions the player might want to make
- "flags" – A tag that currently only has one use, but will be expanded upon in the future

## What Does a Line of Dialogue Look Like?

    {
        "dialogue":"\"Tidings.\"",
        "criteria":[
            ["isAction", "=", "idle"]
        ]
    }

Dialogue lines are written as things called dictionary objects. These objects are a list of important details (called variables) that need to be present for the game engine to properly choose the dialogue line when the player talks to an NPC.

If the above example were to be chosen by the NPC to be displayed to the player, it would look something like this:

`NPC NAME – "Tidings."`

In the above example, the dialogue line includes two bits of important information, called "tags". The two tags included in the example are as follows:

- "dialogue"
- "criteria"

The "dialogue" tag is the most important, as it contains the actual line of dialogue an NPC might say.

The "criteria" tag is a list of requirements that must be met in order for a line of dialogue to be chosen by the NPC to say to the player. All listed criteria must be met for it to be considered.

There are many other tags that can be added to further specify when or if a specific line of dialogue will display or extra actions that could occur after the line is said. However, those tags are entirely optional.

## What Does Dialogue Option Look Like?

    {
        "option":"Ask the dog how its day is going",
        "isAction":"animalTalk",
        "playerDialogue":"You ask the dog how it's day is going.",
        "criteria":[["playerPerks","has","Animal Speech"]],
        "npcFlagActions":[
            {"flag":"dogConvo","modifies":"+","value":1,"defaultValueIfNone":0}
        ]
    }

The above is an example of a dialogue option. Dialogue options are used to give the player additional choices to make during a conversation. These are in addition to the default choices such as "Small Talk" and "Goodbye". In the above example, if the player has the "Animal Speech" perk, then they will be able to choose the option "Ask the dog how it's day is going" when talking to the dog.

Finally, in the above example, the "npcFlagActions" tag is used to modify a flag on the NPC during this specific conversation. If the player leaves the conversation and comes back, the flag will be reset to its default value. This can be useful to add conversations with multiple steps/parts, or to possibly keep track of the player asking the same thing multiple times and allowing the NPC to have an angry or irritated response. These flags can be checked in the "criteria" tag of a dialogue line like any other.

This on its own does not give a response for the NPC, but it does allow for NPC conversations to have special dialogue options that are only available to the player if they are talking to specific NPCs or if the player meets certain requirements.

If the additional dialogue option uses a custom "isAction" tag, then the "lines" tag *should* contain a line of dialogue that uses the same "isAction" tag, such as the example below:

    {
        "dialogue":"My day has been really good!",
        "criteria":[["isAction","=","animalTalk"]]
    }

This dialogue line will only be displayed if the player chose the additional dialogue option "Ask the dog how its day is going".

## What is the "flags" Tag?

The flags tag currently only has a single usable flag. That flag is "additionalDialogue". This flag is used to tell the game engine that the dialogue file is not meant to be used as a standalone dialogue file, but rather as a supplement to another, already existing dialogue file.

This typically only happens in the case of Data Packs that are modifying dialogue files that are already being used by certain NPCs.

For example: if a merchant NPC is already defined as having "merchantNpcDialogue" assigned to it, instead of modifying the NPC itself, the Data Pack can simply modify the "merchantNpcDialogue" dialogue file to include the new lines of dialogue.

# Types of Dialogue Line Tags

## The Dialogue Tag

The "dialogue" tag is a required tag for an obvious reason: without it there would not be any dialogue to display to the player. This should be the first piece of information written when adding new lines of dialogue.

`"dialogue":"\"Hello there.\""`

Displays as:

`NPC NAME - "Hello There"`

In the above example, extra slashes and quotation marks are to help show that the dialogue is being spoken. Lines of dialogue do not need these extra markings, but they should be present if the dialogue is being spoken.

An example of a line of dialogue that does not use the extra quotations is below:

`"dialogue": "*Grunts*"`

As you can see, there are no extra quotations or slashes used. This means that the dialogue will display as:

`NPC NAME - *Grunts*`

As you can see, this allows for more complex lines of dialogue to be written, such as a line of dialogue where the way an NPC says something to the player might be important.

An example of a complex piece of dialogue could be:

`"dialogue":"\"Wait a minute,\" the NPC says confused, \"Who are you?\""`

This would display as:

`NPC NAME - "Wait a minute," the NPC says confused, "Who are you?"`

## The Criteria Tag

The "criteria" tag is a required tag due to its important job: to let the game engine and NPC know when a certain line of dialogue can be said. Each requirement in the list of criteria is made up of three parts:

- The item/stat/action/etc. being checked
- The way it should checked
- The value in which it should be compared to

These three things when put together look like this:

`["isAction", "=", "idle"]`

In the above example, the thing being checked is the "isAction" criteria. The "isAction" criteria tells the game what action the player last took. By default, the actions or states that can be used here are listed below:

- "idle" – The player is not talking to the NPC
- "greeting" – The player has initiated a conversation with the NPC
- "smalltalk" – The player has attempted to make small talk with the NPC
- "goodbye" – The player is ending the conversation with the NPC

So, if a line of dialogue requires the player to try and make some small talk with an NPC, then you can specify that within the requirement like so:

`["isAction", "=", "idle"]`

Don't forget, since the criteria tag is a list of these requirements, you can make dialogue only appear if multiple requirements are met. For example:

    {
        "dialogue":"\"I can't stand all these Elves running about.\"",
        "criteria":[
            ["isAction", "=", "smalltalk"],
            ["playerRace", "!=", "elf"],
            ["npcRace", "!=", "elf"],
            ["npcFlags", "has", "racist"]
        ]
    }

This line of dialogue would display as:

`"I can't stand all these Elves running about."`

As long as:

- The player is making small talk with the NPC
- The player is not an elf
- The NPC is not an elf
- The NPC generated with a "racist" flag

This line of dialogue will only have a chance of being said if **ALL** of the requirements are met.

There are additional states and actions that requirements within criteria can use. Those are listed in the section *Usable Criteria*. There are also additional isAction states that are supported in the game by default. The section *"isAction" Criteria Expanded* covers those.

## The Weight Tag

Now that we have covered the required tags, we can move on to the optional tags. The first optional tag we will cover is the "weight" tag.

A line of dialogue that uses the weight tag will look like this:

    {
        "dialogue":"\"I am special dialogue that has a higher chance of being said.\"",
        "criteria":[
            ["isAction", "=", "smalltalk"]
        ],
        "weight": 5
    }

In the above example, the dialogue has a weight of 5. This means that if there were two lines of dialogue that could be said, and one had a weight of 5 and the other had a weight of 1, then the line of dialogue with a weight of 5 would have a 5/6 chance of being said, while the line of dialogue with a weight of 1 would have a 1/6 chance of being said.

Basically, the higher the weight, the more likely the line of dialogue will be said by an NPC.

Setting weights can be extremely useful when a line has a super specific list of criteria and you want to guarantee that the player will see it.

## The Add and Remove Player Flags

The "addPlayerFlags" and "removePlayerFlags" tags are used to add or remove flags from the player when a line of dialogue is said. This can be useful for a variety of reasons, such as keeping track of rumors or conversational details the player has heard.

An example of a line of dialogue that adds a flag to the player is below:

    {
        "dialogue":"\"I heard that the King is sick.\"",
        "criteria":[
            ["isAction", "=", "smalltalk"]
        ],
        "addPlayerFlags": ["heardKingIsSick"]
    }

This line of dialogue if chosen and displayed to the player will add a behind the scenes flag that can be queried or checked on in the future. In the above example, after the player hears the rumor, other dialogue or conversational choices could appear that required the player to know of such a detail, possibly unlocking future quests, events, areas, and the like.

If the player has a flag such as "isOwedAFavor", and the NPC speaking to the player pays back that favor with some other information or dialogue, then it would make sense to remove that flag from the player so that they do not get the same dialogue multiple times. This can be done via the example below:

    {
        "dialogue":"\"I heard that the King is sick.\"",
        "criteria":[
            ["isAction", "=", "smalltalk"]
        ],
        "addPlayerFlags": ["heardKingIsSick"],
        "removePlayerFlags": ["isOwedAFavor"]
    }

In the above example, the NPC removes the "isOwedAFavor" flag from the player, and added the "heardKingIsSick" flag. Thus conversational transaction can occur. Notice, though, that this line of dialogue does not require the player to have the "isOwedAFavor" flag, nor does it require the player to not have the "heardKingIsSick" flag. This is because the "addPlayerFlags" and "removePlayerFlags" tags are not criteria. They are actions that occur when the line of dialogue is said.

Remember, the "addPlayerFlags" does not add duplicates of flags to the player. If the player already has a flag that is being added, then the flag will not be added again. Similarly the "removePlayerFlags" will not remove flags that the player does not have. If a line of dialogue depends on the player having one flag, and not having another flag, then that should be checked in the criteria tag. An example of this is below:

    {
        "dialogue":"\"I heard that the King is sick.\"",
        "criteria":[
            ["isAction", "=", "smalltalk"],
            ["playerFlags", "has", "isOwedAFavor"],
            ["playerFlags", "doesNotHave", "heardKingIsSick"]
        ],
        "addPlayerFlags": ["heardKingIsSick"],
        "removePlayerFlags": ["isOwedAFavor"]
    }

This line of dialogue will only be said if:

- The player is making small talk with the NPC
- The player has the "isOwedAFavor" flag
- The player does not have the "heardKingIsSick" flag

If all of these requirements are met, then the line of dialogue will be said, and the "heardKingIsSick" flag will be added to the player, and the "isOwedAFavor" flag will be removed from the player.

Finally, both the "addPlayerFlags" and "removePlayerFlags" tags can take a list of flags to add or remove. This can be useful if you want to add or remove multiple flags at once.

# An Example Dialogue File

    {
        "lines":[
            {
                "dialogue":"\"What a nice breeze.\"",
                "criteria":[
                    ["isAction", "=", "idle"]
                ]
            },
            {
                "dialogue":"\"Howdy.\"",
                "criteria":[
                    ["isAction", "=", "greeting"]
                ]
            },
            {
                "dialogue":"\"Hopefully the weather stays this nice. It'll be good for the crops.\"",
                "criteria":[
                    ["isAction", "=", "smalltalk"]
                ]
            },
            {
                "dialogue":"\"I'll be seeing ya.\"",
                "criteria":[
                    ["isAction", "=", "goodbye"]
                ]
            },
            {
                "dialogue":"\"I'm just a farmer.\"",
                "criteria":[
                    ["isAction", "=", "askAboutProfession"]
                ],
                "addPlayerFlags": ["knowsWhoTheFarmerIs"]
            },
            {
                "dialogue":"\"I'm just a farmer, what gold could I possibly give you?\"",
                "criteria":[
                    ["isAction", "=", "askForGold"],
                ],
                "addPlayerFlags": ["knowsWhoTheFarmerIs"]
            },
            {
                "dialogue":"\"You know that I'm just a farmer. I've got not gold to spare.\"",
                "criteria":[
                    ["isAction", "=", "askForGold"],
                    ["playerFlags", "has", "knowsWhoTheFarmerIs"]
                ],
                "weight":5
            }
        ],
        "otherDialogueOptions":[
            {
                "option":"\"What do you do around here?\"",
                "isAction":"askAboutProfession",
                "criteria":[
                    ["playerFlags", "nothas", "knowsWhoTheFarmerIs"]
                ]
            },
            {
                "option":"\"Ask for gold.\"",
                "isAction":"askForGold",
                "criteria":[]
            }
        ],
        "flags":[]
    }

The above dialogue file is a good example of how to use the dialogue system. It includes the four basic "isAction" states, while also introducing two additional ones. It also shows how to add and remove flags from the player, while also showing possible uses for such a feature. Finally it also shows the weight tag, and how it can be used to make certain lines of dialogue more likely to be said than others.

The first additional dialogue option also makes use of criteria. It will only be available to the player if they do not already know who the farmer is. This is done by checking if the player has the "knowsWhoTheFarmerIs" flag. If they do not, then the option will be available to the player. If they do, then the option will not be available to the player.

That flag also affect the outcome of the "Ask for gold" option. If the player does not know the NPC is a farmer, he will respond with "I'm just a farmer, what gold could I possibly give you?". If the player does know the NPC is a farmer, then he will have a significantly  higher chance (thanks to the weight tag) of responding with "You know that I'm just a farmer. I've got not gold to spare."

To finish this example up, there is also the fact that the dialogue file is nice and small with a specific purpose. It could easily be added to the list of dialogue files loaded onto an NPC, meaning that any NPC that is a farmer would be able to make use of this dialogue along with whatever more specific lines they may need, without needing to rewrite the same lines multiple times.

# Additional Information

## Usable Criteria

The game gives dialogue access to a wide range of possible criteria. The above examples have shown "isAction", "playerRace", "npcRace", and "npcFlags", but there are many more that can be used. The full list of usable criteria is listed below:

- "inAreaId" – The area ID the player is currently in
- "inAreaType" – The area type the player is currently in
- "isAction" – The action the player last took during a conversation
- "npcFlags" - A list of the flags the NPC has
- "npcId" - The ID of the NPC
- "npcInventoryCount" - The number of items the NPC has in their inventory
- "npcInventoryIds" - The IDs of the items the NPC has in their inventory
- "npcInventoryItemTypeCount" - The number of the types of items the NPC has in their inventory
- "npcInventoryItemTypes" - The item types of the items the NPC has in their inventory
- "npcPersonalId" - The personal ID of the NPC
- "npcProfessions" - A list of the professions the NPC has
- "npcRace" - The race the NPC is
- "playerDialogueFlags" - A list of the flags the player has for the current conversation
- "playerFlags" – A list of all of the flags the player has
- "playerGold" - The amount of gold the player has
- "playerHealth" - The amount of health the player has
- "playerMaxHealth" - The maximum amount of health the player can have
- "playerHealthPercent" - The percentage of health the player has
- "playerLevel" - The level the player is
- "playerPerks" – A list of all of the perks the player has
- "playerRace" - The race the player is
- "playerXp" - The amount of experience the player has
- "playerXpNeededForLevelUp" - The amount of experience the player needs to level up

## "isAction" Criteria Expanded

Along with the "isAction" states that were listed in the Criteria section, there are some other states that could occur if the NPC has a profession. The most common profession that an NPC might have is the "merchant" profession. Any NPC with the "merchant" profession will need to have at least a single line for each of the "isAction" states listed below below:

- "shop" – The player has asked to see what good the NPC has to offer
- "shopSell" – The player has decided to sell something to the NPC
- "shopSellFail" – The player has nothing to sell to the NPC
- "buyItem" – The player has bought an object from the NPC
- "buyItemFail" – The player has attempted to buy an item from the NPC, but does not have enough gold
- "buyItemCancel" – The player decided not to buy the item they were examining
- "sellItem" – The player has sold an item to the NPC
- "sellItemCancel" – The player decided not to sell the item they were examining
- "finishSell" – The player has decided to stop selling items to the NPC
- "finishShop" – The player has decided to stop buying items from the NPC

While the list of criteria can be empty (meaning that the line of dialogue could be said at any time), it is recommended that at a minimum the list of criteria at least include a "isAction" check.