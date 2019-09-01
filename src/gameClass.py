import random
import time
import os
import textwrap

from areaClass import Area
from armorClass import Armor
from dieClass import rollDice
from displayClass import Screen
from enemyClass import Enemy
from jsonDecoder import loadJson
from modifierClass import Modifier
from playerClass import Player
from questClass import Quest
from weaponClass import Weapon


DEBUG = 0
VERSION = 0
DELAY = 0


class Game(object):

    def __init__(self):
        '''Initializes the Game object. This also sets some required variable
        to empty so they can be initialized later.'''
        self.cleanDataPackInfo()
        self.player = Player()

        self.disp = Screen()

        self.loaded = False
        self.settings = {}

        self.possibleQuests = []
        self.currentQuests = []
        self.completedQuests = []
        self.backlog = []
        self.importantQuestInfo = []

        self.currentArea = None

    def initialLoad(self, folder="res/", settingsdata={}):
        '''This does all of the heavy duty loading. Once this is complete, all
        game data is loaded until the game is closed, which cuts down on load
        times.'''
        global VERSION, DELAY, DEBUG
        self.settings = settingsdata
        VERSION = self.settings["VERSION"]
        DELAY = self.settings["DELAY"]
        EVENTDELAY = self.settings["EVENTDELAY"]
        DEBUG = self.settings["DEBUG"]
        DEBUGDISPLAY = self.settings["DEBUGDISPLAY"]

        # Set up the display with a delay and whether or not to debug
        self.disp.debugging = DEBUGDISPLAY
        self.disp.printdelay = DELAY

        packs = loadJson(folder + "packs.json")
        starter = packs["start"]
        print("\nLoading assets...")
        for pack in packs["packs"]:
            print("Loading pack \"{}\"...".format(pack))
            self.packs[pack] = loadJson("%s%s/meta.json" % (folder, pack))

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
                print(q)

        self.currentArea = Area(self.areas[self.packs[starter][
                                "startingArea"]], DEBUG, **{"playerLevel": 1, "difficultyModifier": 1})
        self.currentArea.load(self.weapons, self.armor, self.misc,
                              self.enemies, self.npcs, self.events, self.modifiers)
        # Disables enemies in the first area.
        self.currentArea.enemy = []

        # Sets up the player variables and also gives the player some starting gear.
        # Spawns in an extra weapon for the player to switch between.
        self.player.disp = self.disp
        self.player.weapon = Weapon(self.weapons["weapon_ironSword"])
        self.player.armor = Armor(self.armor["armor_hideArmor"])
        self.player.inv.append(Weapon(self.weapons["weapon_ironSword"]))
        self.loaded = True
    
    def cleanDataPackInfo(self):
        self.packs = {}
        self.weapons = {}
        self.armor = {}
        self.misc = {}
        self.areas = {}
        self.quests = {}
        self.events = {}
        self.npcs = {}
        self.enemies = {}
        self.modifiers = {}

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

        ##### Random event Code #####
        if self.currentArea.event:
            self.disp.clearScreen()
            self.disp.displayHeader("Random Event")
            self.disp.display(self.currentArea.event.name)
            self.disp.display(self.currentArea.event.msg, 1, 1)
            self.disp.displayHeader("Actions", 1)
            x = 0
            for choice in self.currentArea.event.actions.keys():
                x += 1
                self.disp.display("%d. %s" % (x, choice), 0)
            self.disp.closeDisplay()
            time.sleep(DELAY)
            input("Enter to continue")

        ##### Interacting with an NPC Code #####
        if self.currentArea.npc:
            self.disp.clearScreen()
            self.disp.displayHeader(self.currentArea.npc.name)
            self.disp.display(self.currentArea.npc)
    
    def fightEnemies(self):
        ##### Fighting Code #####
        if self.currentArea.enemy != []:
            self.disp.clearScreen()
            for areaEnemy in self.currentArea.enemy:
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
                enemyhp = areaEnemy.getHealth()
                while enemyhp > 0 and self.player.hp:
                    cmd = -1
                    while not ((cmd <= 2 and cmd >= 1) or (cmd == 0 and DEBUG)):
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
                        self.disp.display("3. Player Menu", 0)
                        self.disp.closeDisplay()
                        try:
                            cmd = int(input())
                        except ValueError:
                            cmd = -1

                        if cmd == 3:
                            self.player.playerMenu(self.currentQuests,self.completedQuests)
                        elif cmd == 9 and DEBUG:
                            self.disp.dprint("Healing player fully.")
                            self.player.hp = self.player.hpMax
                        elif cmd not in (1, 2, 9, 0):
                            self.disp.clearScreen()
                            self.disp.displayHeader("Error")
                            self.disp.display("That was not a valid response.",
                                              1, 1)

                    if cmd == 1 or cmd == 0:
                        self.disp.clearScreen()
                        damage = self.player.getWeaponDamage()
                        if DEBUG and cmd == 0:
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
                                damage -= int(self.player.getArmorDefence())
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
                self.disp.display("%d. %-32s %17s   Hostility - %2d" %
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
                self.player.playerMenu(self.currentQuests, self.completedQuests)

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
        for i in range(1, self.currentArea.newArea + 1):
            areatypes = self.currentArea.newAreaTypes[::]
            newArea = areatypes.pop(0)
            highroll = rollDice(newArea[1])
            for aType in areatypes:
                newroll = rollDice(aType[1])
                if newroll > highroll:
                    newArea = aType
                    highroll = newroll
            generatedArea = Area(self.areas[newArea[0]])
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
                if not DEBUG:
                    time.sleep(1)
                input("\nEnter to continue")
                self.disp.dprint("Processed say condition.")
            elif action[0] == "giveXP":
                self.player.xp += action[1]
                self.disp.display("You gained %d experience." %
                                  action[1])
                self.disp.dprint("Processed giveXP condition.")
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
        self.disp.dprint("\nGame Load status: {}".format(self.loaded))
        self.disp.dprint("Debug Arguments: {}".format(self.settings["DEBUG"]))

        self.disp.clearScreen()
        self.disp.displayHeader("Main Menu")
        self.disp.display("PROJECT: EMPTY")
        self.disp.display("Welcome to the Void.",0)
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
            toggleableOptions = self.displayOptions(settingsNumOfPages, settingsPage)
            try:
                cmd = int(input())
            except ValueError:
                cmd = -1
            
            if cmd in range(1,9) and cmd-1<=len(toggleableOptions):
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
        self.disp.display(f'1. {firstOption[1]:<20} {enabled:>48}')
        i = 1
        for option in listOfOptions:
            i+=1
            enabled = "ENABLED" if option[2] else "DISABLED"
            self.disp.display(f'{i}. {option[1]:<20} {enabled:>48}', 0)
        self.disp.display("Input option # to toggle")
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