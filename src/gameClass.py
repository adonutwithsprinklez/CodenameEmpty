import random
import time
import os
import textwrap

from areaClass import Area
from armorClass import Armor
import copy
from dieClass import rollDice
from displayClass import Screen
from enemyClass import Enemy
from itemGeneration import generateWeapon
from jsonDecoder import loadJson
from miscClass import Misc
from modifierClass import Modifier
from playerClass import Player
from questClass import Quest
from raceClass import Race
from weaponClass import Weapon


DEBUG = 0
DELAY = 0
EVENTDELAY = 0


class Game(object):

    def __init__(self):
        '''Initializes the Game object. This also sets some required variable
        to empty so they can be initialized later.'''
        self.player = None

        self.disp = Screen()

        self.loaded = False
        self.settings = {}
        self.gameSettings = {}
        self.dataPackSettings = {}

        self.currentArea = None
        self.starter = None

        self.logos = []
        self.descs = []

    def initialLoad(self, folder="res/", settingsdata={}):
        '''This does all of the heavy duty loading. Once this is complete, all
        game data is loaded until the game is closed, which cuts down on load
        times.'''
        self.cleanDataPackInfo()

        global DELAY, DEBUG, EVENTDELAY
        self.settings = settingsdata
        self.loadGameSettings()
        DELAY = self.settings["DELAY"]
        EVENTDELAY = self.settings["EVENTDELAY"]
        DEBUG = self.settings["DEBUG"]
        DEBUGDISPLAY = self.gameSettings["DEBUGDISPLAY"]

        # Set up the display with a delay and whether or not to debug
        self.disp.debugging = DEBUGDISPLAY
        self.disp.delay = self.gameSettings["DELAYENABLED"]
        self.disp.printdelay = DELAY

        self.loadDataPackSettings()
        packs = self.dataPackSettings["packsToLoad"]
        self.starter = self.dataPackSettings["start"]
        print("\nLoading assets...")

        for pack in packs:
            if pack[1]:
                pack = pack[0]

                print("Loading pack \"{}\"...".format(pack))
                self.packs[pack] = loadJson("%s%s/meta.json" % (folder, pack))

                if "gameLogo" in self.packs[pack].keys():
                    self.logos.append(self.packs[pack]["gameLogo"])
                if "gameDesc" in self.packs[pack].keys():
                    for desc in self.packs[pack]["gameDesc"]:
                        self.descs.append(desc)

                # Asset loading
                for w in self.packs[pack]["weapons"]:
                    self.weapons[w] = loadJson(
                        "%s%s/weapons/%s.json" % (folder, pack, w))
                    self.disp.dprint("Loaded asset %s" % w)
                for a in self.packs[pack]["armor"]:
                    self.armor[a] = loadJson(
                        "%s%s/armor/%s.json" % (folder, pack, a))
                    self.disp.dprint("Loaded asset %s" % a)
                for m in self.packs[pack]["misc"]:
                    self.misc[m] = loadJson(
                        "%s%s/misc/%s.json" % (folder, pack, m))
                    self.disp.dprint("Loaded asset %s" % m)
                for a in self.packs[pack]["areas"]:
                    self.areas[a] = loadJson(
                        "%s%s/areas/%s.json" % (folder, pack, a))
                    self.disp.dprint("Loaded asset %s" % a)
                for r in self.packs[pack]["races"]:
                    raceData = loadJson("%s%s/races/%s.json" %
                                        (folder, pack, r))
                    self.races[raceData["id"]] = raceData
                    self.disp.dprint("Loaded asset %s" % r)
                for n in self.packs[pack]["npcs"]:
                    self.npcs[n] = loadJson(
                        "%s%s/npcs/%s.json" % (folder, pack, n))
                    self.disp.dprint("Loaded asset %s" % n)
                for e in self.packs[pack]["enemies"]:
                    self.enemies[e] = loadJson(
                        "%s%s/enemies/%s.json" % (folder, pack, e))
                    self.disp.dprint("Loaded asset %s" % e)
                for q in self.packs[pack]["quests"]:
                    self.quests[q] = loadJson(
                        "%s%s/quests/%s.json" % (folder, pack, q))
                    self.disp.dprint("Loaded asset %s" % q)
                for e in self.packs[pack]["events"]:
                    self.events[e] = loadJson(
                        "%s%s/events/%s.json" % (folder, pack, e))
                    self.disp.dprint("Loaded asset %s" % e)
                for m in self.packs[pack]["modifiers"]:
                    mods = loadJson("%s%s/%s.json" % (folder, pack, m))
                    for mod in mods.keys():
                        self.modifiers[mod] = Modifier(mod, mods[mod])
                print("Finished loading assets.")

        # Adds all loaded quests into a list of possible quests, as well as
        # loads thems into actual objects
        for quest in self.quests.keys():
            self.possibleQuests.append(Quest(self.quests[quest]))
        if DEBUG:
            for q in self.possibleQuests:
                self.disp.dprint(q)

        self.loadStartingArea()

        # Sets up the player variables and also gives the player some starting gear.
        # Spawns in an extra weapon for the player to switch between.
        self.loadPlayer()
        self.loaded = True

    def loadStartingArea(self):
        self.currentArea = Area(self.areas[self.packs[self.starter][
                                "startingArea"]], DEBUG, **{"playerLevel": 1, "difficultyModifier": 1})
        self.currentArea.load(self.weapons, self.armor, self.misc,
                              self.enemies, self.npcs, self.events, self.modifiers)
        # Disables enemies in the first area.
        self.currentArea.enemy = []

    def loadPlayer(self):
        self.player = Player()
        self.player.race = Race(self.races["human"])
        self.player.disp = self.disp
        self.player.weapon = Weapon(self.weapons["weapon_ironSword"])
        self.player.armor = Armor(self.armor["armor_hideArmor"])
        self.player.inv.append(generateWeapon(
            self.weapons["template_IronSword"]))
        self.player.gold = 100
        self.loadStartingArea()
        self.player.hp = self.player.getMaxHP()

    def cleanDataPackInfo(self):
        self.packs = {}
        self.weapons = {}
        self.armor = {}
        self.misc = {}
        self.areas = {}
        self.races = {}
        self.quests = {}
        self.events = {}
        self.npcs = {}
        self.enemies = {}
        self.modifiers = {}

        self.possibleQuests = []
        self.currentQuests = []
        self.completedQuests = []
        self.backlog = []
        self.importantQuestInfo = []

    def loadGameSettings(self):
        self.gameSettings = {}
        for setting in self.settings["GAMESETTINGS"]:
            self.gameSettings[setting[0]] = setting[2]

    def loadDataPackSettings(self):
        self.dataPackSettings = {}
        for setting in self.settings["DATAPACKSETTINGS"].keys():
            self.dataPackSettings[setting] = self.settings["DATAPACKSETTINGS"][setting]

    def displayCurrentArea(self):
        '''Displays info on the area the player is currently in.'''
        self.disp.clearScreen()
        title = "%s (%s) - Hostility: %d" % (self.currentArea.name,
                                             self.currentArea.aType, self.currentArea.hostility)
        self.disp.displayHeader(title)
        for desc in self.currentArea.desc.split("\n"):
            self.disp.display(desc)
        print("|{}|".format(" " * 78))
        print("+{}+".format("-" * 78))
        time.sleep(DELAY)
        input("\nEnter to continue")
        self.workOnBacklog()

    def reactCurrentArea(self):
        '''This is where the player becomes able to respond to any action that
        has occured within the game, such as enemies appearing, or quest
        objectives getting updated.'''

        self.fightEnemies()
        if self.player.quit:
            return None

        ##### Random event Code #####
        if self.currentArea.event:
            while not self.currentArea.event.finished:
                self.disp.clearScreen()
                self.disp.displayHeader(self.currentArea.event.name)
                self.disp.display(self.currentArea.event.msg, 1)
                x = 0
                choices = self.currentArea.event.getPossibleActions(
                    self.player)
                if len(choices) > 0:
                    self.disp.displayHeader("Actions", 1, 1)
                    for choice in choices:
                        x += 1
                        action = choice["action"]
                        self.disp.display(f'{x}. {action}', 0)
                    self.disp.closeDisplay()

                    try:
                        cmd = int(input())
                    except:
                        cmd = -1
                    if cmd > 0 and cmd <= x:
                        for action in choices[cmd-1]["eventDo"]:
                            self.disp.dprint(action)
                            if action[0] == "say":
                                self.displayEventAction(action[1])
                            elif action[0] == "goto":
                                self.currentArea.event.gotoPart(
                                    random.choice(action[1]))
                            elif action[0] == "addTag":
                                self.player.tags.append(
                                    self.currentArea.event.getTag(action[1]))
                            elif action[0] == "take":
                                self.currentArea.event.takeItem(
                                    action[1], action[2], self.player)
                            elif action[0] == "give":
                                self.currentArea.event.giveItem(action[1], action[2], self.player,
                                                                self.weapons, self.armor, self.misc)
                            elif action[0] == "finish":
                                self.currentArea.event.finish()
                else:
                    self.disp.closeDisplay()
                    self.currentArea.event.finish()
                    if self.gameSettings["EVENTDELAYENABLED"]:
                        time.sleep(EVENTDELAY)
                    input("\nEnter to continue")

        ##### Interacting with an NPC Code #####
        if self.currentArea.npc:
            self.disp.clearScreen()
            self.disp.displayHeader(self.currentArea.npc.name)
            self.disp.display(self.currentArea.npc)

    def displayEventAction(self, message):
        self.disp.clearScreen()
        self.disp.displayHeader(self.currentArea.event.name)
        self.disp.display(message)
        self.disp.closeDisplay()
        input("\nEnter to continue")

    def fightEnemies(self):
        ##### Fighting Code #####
        if self.currentArea.enemy != []:
            self.disp.clearScreen()
            for areaEnemy in self.currentArea.enemy:
                enemyhp = areaEnemy.getHealth()
                while enemyhp > 0 and self.player.hp:
                    self.disp.dprint(
                        "Enemy Danger Level:   {}".format(areaEnemy.getDanger()))
                    self.disp.dprint(
                        "Enemy Max Health:     {}".format(areaEnemy.hpMax))
                    self.disp.dprint(
                        "Enemy Current Health: {}".format(areaEnemy.hp))
                    self.disp.dprint("Enemy Strength:       {}".format(
                        areaEnemy.getStrength()))
                    self.disp.dprint("Enemy Weapon Damage:  {}".format(
                        areaEnemy.getRawWeaponDamage()))

                    cmd = -1
                    while not ((int(cmd) <= 2 and int(cmd) >= 0) or (cmd == 90 and DEBUG)):
                        self.disp.clearScreen()
                        self.disp.displayHeader("Enemy Encountered - %s" %
                                                (areaEnemy.name))
                        self.disp.display("%s The enemy has a danger level of %d." %
                                          (areaEnemy.desc, areaEnemy.getDanger()), 1, 1)
                        self.disp.displayHeader("Info")
                        self.disp.display("Player: %s - %dHP" %
                                          (self.player.name, self.player.hp))
                        self.disp.display("HP: %s" % ("#" * self.player.getHealth()),
                                          0)
                        self.disp.display("Weapon: %s" %
                                          (str(self.player.weapon)), 0)
                        self.disp.display("Enemy: %s - %dHP" %
                                          (areaEnemy.name, areaEnemy.hp))
                        self.disp.display("HP: %s" %
                                          ("#" * areaEnemy.getHealth()), 0)
                        self.disp.display("Weapon: %s" %
                                          (str(areaEnemy.weapon)), 0, 1)
                        self.disp.displayHeader("Actions")
                        self.disp.display("1. Use your weapon (%s)" %
                                          str(self.player.weapon))
                        self.disp.display("2. Attempt to escape", 0)
                        self.disp.display("0. Player Menu")
                        self.disp.closeDisplay()
                        try:
                            cmd = int(input())
                        except ValueError:
                            cmd = -1
                        if cmd == 0:
                            self.player.playerMenu(
                                self.currentQuests, self.completedQuests)
                            if self.player.quit:
                                # TODO Exit the game completely
                                return None
                        elif cmd in (9, 90) and DEBUG:
                            self.disp.dprint("Healing player fully.")
                            self.player.hp = self.player.getMaxHP()
                        elif cmd not in (1, 2, 9, 0):
                            self.disp.clearScreen()
                            self.disp.displayHeader("Error")
                            self.disp.display("That was not a valid response.",
                                              1, 1)

                    if cmd == 1 or cmd == 90:
                        self.disp.clearScreen()
                        damage = self.player.getWeaponDamage()
                        if DEBUG and cmd == 90:
                            damage *= 10
                        msg = self.player.getWeaponAction()
                        damage -= int(areaEnemy.getArmorDefence())
                        if damage < 0:
                            damage = 0
                        areaEnemy.hp -= damage
                        self.disp.displayHeader("You")
                        self.disp.display("%s You dealt %d damage." %
                                          (msg, damage), 1, 1)
                        self.disp.displayHeader(areaEnemy.name)
                        damage = areaEnemy.getWeaponDamage()
                        if self.player.armor:
                            damage -= self.player.getArmorDefence()
                        if damage < 0:
                            damage = 0
                        self.player.hp -= damage
                        self.disp.display("%s %s dealt %d damage." % (
                            areaEnemy.weapon.getAction(), areaEnemy.name, damage))
                        self.disp.closeDisplay()
                        time.sleep(DELAY)
                        input("\nEnter to continue.")
                    elif cmd == 2:
                        self.disp.clearScreen()
                        escape = False
                        if random.randint(0, self.player.getArmorDefence() + areaEnemy.getWeaponDamage()) < areaEnemy.getArmorDefence():
                            escape = True
                        if escape:
                            self.disp.displayHeader("Escape Successful")
                            self.disp.display(
                                "You successfully escape from %s." % (areaEnemy.name))
                        else:
                            self.disp.displayHeader("Escape Failed")
                            self.disp.display("You fail to escape from %s." %
                                              (areaEnemy.name), 1, 1)
                            self.disp.displayHeader(areaEnemy.name)
                            damage = areaEnemy.weapon.damage
                            if self.player.armor:
                                damage += "-{0}".format(self.player.getArmorDefence())
                            damage = rollDice(damage)
                            if damage < 0:
                                damage = 0
                            self.player.hp -= damage
                            self.disp.display("%s %s dealt %d damage." % (
                                areaEnemy.weapon.getAction(), areaEnemy.name, damage))
                        self.disp.closeDisplay()
                        time.sleep(DELAY)
                        input("\nEnter to continue")
                        if escape:
                            break

                    self.disp.clearScreen()
                    enemyhp = areaEnemy.hp

                if self.player.hp > 0 and areaEnemy.hp <= 0:
                    self.disp.clearScreen()
                    self.disp.displayHeader("Victory")
                    self.disp.display(
                        "You defeated the enemy, and got %d experience." % areaEnemy.xp)
                    self.importantQuestInfo.append(
                        ["isKilled", areaEnemy.eID, True, False])
                    self.disp.display("%s %s" %
                                      (areaEnemy.name, areaEnemy.deathMsg))
                    if random.randint(1, 100) < areaEnemy.itemChance:
                        self.disp.display("")
                        self.disp.displayHeader("Reward")
                        self.disp.display(areaEnemy.itemDrop[1])
                        self.disp.display("You recieved %s." %
                                          (areaEnemy.itemDrop[0].name))
                        self.player.inv.append(areaEnemy.itemDrop[0])
                    self.disp.closeDisplay()
                    time.sleep(DELAY)
                    input("\nEnter to continue")

                # UPDATE QUEST INFO
                self.updateQuestInfo()
                self.workOnBacklog()

    def chooseNewArea(self):
        '''This lets the player choose a new area to travel to.'''
        # Create various area choices:
        choices = self.randomAreaChoices()
        cmd = -1

        # Allow the player to choose from those places:
        while not 1 <= cmd <= len(choices):
            self.disp.clearScreen()
            self.disp.displayHeader("Where to next?")
            self.disp.display("", 1, 0)
            x = 0
            for area in choices:
                x += 1
                self.disp.display("%d. %-37s %12s   Hostility - %2d" %
                                  (x, area.name, area.aType, area.hostility), 0)
            self.disp.display("0. Player Menu")
            self.disp.closeDisplay()
            try:
                cmd = int(input())
            except ValueError:
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display("That was not a valid response.")
                self.disp.closeDisplay()
                cmd = -1
                time.sleep(DELAY)
                input("\nEnter to continue")

            if cmd == 0:
                self.player.playerMenu(
                    self.currentQuests, self.completedQuests)
                if self.player.quit:
                    # TODO Exit the game completely
                    return None

        # Load the new area
        self.currentArea = choices[cmd - 1]
        self.currentArea.load(self.weapons, self.armor, self.misc,
                              self.enemies, self.npcs, self.events, self.modifiers)

        self.importantQuestInfo.append(
            ["inAreaType", self.currentArea.aType, True, False])

        self.updateQuestInfo()

    def randomAreaChoices(self):
        '''This randomly generates areas for the player to choose from.'''
        choices = []
        # This is to guarantee that no "limited" areas are used more than once
        usedAreas = []

        # Grab all required areas and throw them into a seperate list. This is to
        # guarantee that they are generated.
        areatypes = self.currentArea.newAreaTypes[::]
        required = []
        for area in areatypes:
            if len(area) > 2:
                for flag in area[2]:
                    if flag == "required":
                        required.append(area)

        # Actually generate areas:
        for i in range(1, self.currentArea.newArea + 1):
            if len(required) > 0:
                newArea = required.pop(0)
            else:
                areatypes = self.currentArea.newAreaTypes[::]
                highroll = 0
                for aType in areatypes:
                    newroll = rollDice(aType[1])
                    alreadyUsed = False
                    if len(aType) > 2:
                        if "limited" in aType[2]:
                            if aType[0] in usedAreas:
                                alreadyUsed = True
                    if newroll > highroll and not alreadyUsed:
                        newArea = aType
                        highroll = newroll
            generatedArea = Area(self.areas[newArea[0]])
            usedAreas.append(newArea[0])
            choices.append(generatedArea)
        return choices

    def workOnBacklog(self):
        '''This collects and organizes the information in the backlog of
        actions to be carried out by the quest system.'''
        self.disp.dprint("\nWorking on backlog...")
        for collection in self.backlog:
            self.processActions(collection)
            self.backlog.remove(collection)

    def processActions(self, actions):
        '''This processes all actions that were given by the quest system.'''
        for action in actions:
            if action[0] == "say":
                self.disp.clearScreen()
                self.disp.displayHeader("Event")
                self.disp.display(action[1])
                self.disp.closeDisplay()
                if self.gameSettings["EVENTDELAYENABLED"]:
                    time.sleep(1)
                input("\nEnter to continue")
                self.disp.dprint("Processed say condition.")
            elif action[0] == "giveXP":
                self.player.xp += action[1]
                self.disp.display("You gained %d experience." %
                                  action[1])
                self.disp.dprint("Processed giveXP condition.")
            elif action[0] == "giveItem":
                itemKey = action[1]
                item = None
                if itemKey in self.weapons.keys():
                    item = generateWeapon(self.weapons[itemKey])
                elif itemKey in self.misc.keys():
                    item = Misc(self.misc[itemKey])
                elif itemKey in self.armor.keys():
                    item = Armor(self.armor[itemKey])
                if item != None:
                    self.disp.display("You recieved {}.".format(item.name))
                    self.player.inv.append(item)
            elif action[0] == "questComplete":
                for quest in self.currentQuests:
                    self.disp.dprint(action)
                    self.disp.dprint("Quest: {}".format(quest.qID))
                    self.disp.dprint("Completed Quest: {}".format(action[-1]))
                    if quest.qID == action[-1]:
                        quest.complete = True
                        self.completedQuests.append(quest)
                        self.currentQuests.remove(quest)
                self.disp.dprint("Processed questComplete condition.")
            elif action[0] == "spawnEnemy":
                self.currentArea.enemy.append(Enemy(
                    self.enemies[action[1]], self.weapons, self.armor, self.misc, self.modifiers))
                self.disp.dprint("Processed spawnEnemy condition.")

    def updateQuestInfo(self):
        '''This updates all quest related variables and states.'''
        # update any currently loaded quests to see if any requirements are met
        self.disp.dprint("\nUnstarted quests:")
        for quest in self.possibleQuests:
            self.disp.dprint(quest)
            for event in self.importantQuestInfo:
                quest.setFlagToValue(event[0], event[1], event[2], event[3])
            do = quest.start()
            if do:
                self.currentQuests.append(quest)
                self.possibleQuests.remove(quest)
                self.backlog.append(do)
        self.disp.dprint("Started quests:")
        for quest in self.currentQuests:
            self.disp.dprint(quest)
            for event in self.importantQuestInfo:
                quest.setFlagToValue(event[0], event[1], event[2], event[3])
            do = quest.doNextStep()
            if do:
                self.backlog.append(do)
        self.disp.dprint("Completed Quests:")
        for quest in self.completedQuests:
            self.disp.dprint(quest)
        self.importantQuestInfo = []

    def displayMainMenu(self):
        self.disp.dprint("Debug Arguments: {}".format(self.settings["DEBUG"]))

        self.disp.clearScreen()
        self.disp.displayHeader("Main Menu")

        logo = random.choice(self.logos)
        firstLine = logo[0]
        self.disp.display(firstLine)
        for line in logo[1:]:
            self.disp.display(line, 0)

        self.disp.display(random.choice(self.descs))
        self.disp.display("1. New Game")
        self.disp.display("2. Settings", 0)
        self.disp.display("3. Data Packs", 0)
        self.disp.display("0. Exit")
        self.disp.closeDisplay()

    def openOptionsWindow(self):
        settingsOpen = True
        settingsPage = 0
        settingsNumOfPages = int(len(self.settings["GAMESETTINGS"]) / 9)

        while settingsOpen:
            toggleableOptions = self.displayOptions(
                settingsNumOfPages, settingsPage)
            try:
                cmd = int(input())
            except ValueError:
                cmd = -1

            if cmd in range(1, 9) and cmd-1 <= len(toggleableOptions):
                self.settings["GAMESETTINGS"][cmd-1+9*settingsPage][2] ^= True
            elif cmd == 12 and settingsPage < settingsNumOfPages:
                settingsPage += 1
            elif cmd == 11 and settingsPage > 0:
                settingsPage -= 1
            elif cmd == 0:
                settingsOpen = False

    def displayOptions(self, numPages=1, page=0):
        self.disp.clearScreen()
        self.disp.displayHeader("Settings")

        startOptions = page*9
        endOptions = 9+(page*9)

        listOfOptions = self.settings["GAMESETTINGS"][startOptions:endOptions]
        firstOption = listOfOptions.pop(0)
        enabled = "ENABLED" if firstOption[2] else "DISABLED"
        self.disp.display(f'1. {firstOption[1]:<50} {enabled:>18}')
        i = 1
        for option in listOfOptions:
            i += 1
            enabled = "ENABLED" if option[2] else "DISABLED"
            self.disp.display(f'{i}. {option[1]:<50} {enabled:>18}', 0)
        self.disp.display(
            "Input option # to toggle. Settings take effect on screen exit.")
        pagebreak = 1
        if page < numPages:
            self.disp.display("12. for next page of settings")
            pagebreak = 0
        if page > 0:
            self.disp.display("11. for previous page of settings", pagebreak)
            pagebreak = 0
        self.disp.display("0. to exit", pagebreak)
        self.disp.closeDisplay()

        return listOfOptions

    def openDataPacks(self):
        self.loadDataPackSettings()

        dataPacksWindow = True
        packPage = 0
        numPages = int(len(self.dataPackSettings["packsToLoad"]) / 9)

        while dataPacksWindow:
            toggleablePacks = self.displayPacks(numPages, packPage)
            try:
                cmd = int(input())
            except ValueError:
                cmd = -1

            if cmd in range(1, 9) and cmd-1 <= len(toggleablePacks):
                if self.dataPackSettings["packsToLoad"][cmd-1+9*packPage][0] != "official":
                    self.dataPackSettings["packsToLoad"][cmd -
                                                         1+9*packPage][1] ^= True
                else:
                    # TODO Display error when attempting to disable the official datapack.
                    pass
                    # The official data pack should be allowed to be disabled, only if
                    # another data pack is enabled
            elif cmd == 12 and packPage < numPages:
                packPage += 1
            elif cmd == 11 and packPage > 0:
                packPage -= 1
            elif cmd == 0:
                dataPacksWindow = False

        self.settings["DATAPACKSETTINGS"] = self.dataPackSettings

    def displayPacks(self, numPages=1, page=0):
        self.disp.clearScreen()
        self.disp.displayHeader("Data Packs")

        startOptions = page*9
        endOptions = 9+(page*9)

        listOfOptions = self.dataPackSettings["packsToLoad"][startOptions:endOptions]
        firstOption = listOfOptions.pop(0)
        enabled = "ENABLED" if firstOption[1] else "DISABLED"
        firstOption = loadJson(
            self.dataPackSettings["folder"] + firstOption[0] + "/meta.json")
        packName = firstOption["name"]
        packDesc = firstOption["desc"]
        packAuth = firstOption["author"]

        self.disp.display(f'1. {packName:<50} {enabled:>18}')
        self.disp.display(f'\t{packDesc}', 0)
        self.disp.display(f'\tBy: {packAuth}', 0)

        i = 1

        for pack in listOfOptions:
            i += 1
            enabled = "ENABLED" if pack[1] else "DISABLED"
            pack = loadJson(
                self.dataPackSettings["folder"] + pack[0] + "meta.json")
            packName = pack["name"]
            packDesc = pack["desc"]
            packAuth = pack["author"]

            self.disp.display(f'{i}. {packName:<50} {enabled:>18}')
            self.disp.display(f'\t{packDesc}', 0)
            self.disp.display(f'\tBy {packAuth}', 0)
        self.disp.display(
            "Input pack # to toggle. Changes to enabled data packs take effect on screen exit.")
        pagebreak = 1
        if page < numPages:
            self.disp.display("12. for next page of settings")
            pagebreak = 0
        if page > 0:
            self.disp.display("11. for previous page of settings", pagebreak)
            pagebreak = 0
        self.disp.display("0. to exit", pagebreak)
        self.disp.closeDisplay()

        return listOfOptions
