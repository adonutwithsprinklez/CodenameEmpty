
# Official Python module imports
import random
import time
import os


# Local module imports

from ApplicationWindowClass import ApplicationWindow
from areaControllerClass import AreaController
from armorClass import Armor
from dieClass import rollDice
from enemyClass import Enemy
from itemGeneration import generateWeapon, generateAmorSet
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

        self.disp = ApplicationWindow()

        self.loaded = False
        self.settings = {}
        self.gameSettings = {}
        self.dataPackSettings = {}

        self.areaController = None
        self.starter = None

        self.nonRepeatableEvents = []
        self.globalRandomEvents = []

        self.logos = []
        self.descs = []

        self.displayIsInitialized = False

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
        DISPLAYSETTINGS = self.settings["DISPLAYSETTINGS"]
        DEBUGDISPLAY = self.gameSettings["DEBUGDISPLAY"]

        # Set up the display with a delay and whether or not to debug
        if not self.displayIsInitialized:
            self.disp.initiate_window(f'Codename: EMPTY v{self.settings["VERSION"]}', DISPLAYSETTINGS,
                                      DELAY, self.gameSettings["DELAYENABLED"], DEBUGDISPLAY)
            self.displayIsInitialized = True
        else:
            self.disp.set_settings(DISPLAYSETTINGS, DELAY, self.gameSettings["DELAYENABLED"], DEBUGDISPLAY)

        self.loadDataPackSettings()
        packs = self.dataPackSettings["packsToLoad"]
        self.starter = self.dataPackSettings["start"]
        print("\nLoading assets...")

        for pack in packs:
            if pack[1]:
                pack = pack[0]

                print("\tLoading pack \"{}\"...".format(pack))
                self.packs[pack] = loadJson("%s%s/meta.json" % (folder, pack))

                if "gameLogo" in self.packs[pack].keys():
                    self.logos.append(self.packs[pack]["gameLogo"])
                if "gameDesc" in self.packs[pack].keys():
                    for desc in self.packs[pack]["gameDesc"]:
                        self.descs.append(desc)

                # Asset loading
                # TODO: Clean this up. Either seperate into different functions or
                # rewrite. This was fine until data injection became a feature. Now
                # it's waaay too cluttered.
                for w in self.packs[pack]["weapons"]:
                    self.weapons[w] = loadJson("%s%s/weapons/%s.json" % (folder, pack, w))
                    self.disp.dprint("\t\tLoaded Weapon %s" % w)
                for a in self.packs[pack]["armor"]:
                    self.armor[a] = loadJson("%s%s/armor/%s.json" % (folder, pack, a))
                    self.disp.dprint("\t\tLoaded Armor %s" % a)
                for m in self.packs[pack]["misc"]:
                    self.misc[m] = loadJson("%s%s/misc/%s.json" % (folder, pack, m))
                    self.disp.dprint("\t\tLoaded Misc %s" % m)
                for a in self.packs[pack]["areas"]:
                    self.areas[a] = loadJson("%s%s/areas/%s.json" % (folder, pack, a))
                    if "injectArea" in self.areas[a].keys():
                        for aKey in self.areas[a]["injectArea"].keys():
                            injectData = [a] + self.areas[a]["injectArea"][aKey]
                            self.areas[aKey]["areas"].append(injectData)
                    self.disp.dprint("\t\tLoaded Area %s" % a)
                for r in self.packs[pack]["races"]:
                    raceData = loadJson("%s%s/races/%s.json" % (folder, pack, r))
                    self.races[raceData["id"]] = raceData
                    self.disp.dprint("\t\tLoaded Race %s" % r)
                for n in self.packs[pack]["npcs"]:
                    self.npcs[n] = loadJson("%s%s/npcs/%s.json" % (folder, pack, n))
                    self.disp.dprint("\t\tLoaded NPC %s" % n)
                for e in self.packs[pack]["enemies"]:
                    self.enemies[e] = loadJson("%s%s/enemies/%s.json" % (folder, pack, e))
                    if "injectArea" in self.enemies[e].keys():
                        for injection in self.enemies[e]["injectArea"]:
                            injectionEnemy = [e, injection[1]]
                            self.areas[injection[0]]["enemies"].append(injectionEnemy)
                            if "areaMinEnemyChance" in self.enemies[e].keys():
                                self.areas[aKey]["enemyChance"] = max(self.areas[injection[0]]["enemyChance"],
                                                                      self.enemies[e]["areaMinEnemyChance"])
                            if "areaEnemyPointsPerHostility" in self.enemies[e].keys():
                                self.areas[injection[0]]["enemyPointsPerHostility"] = self.enemies[e]["areaEnemyPointsPerHostility"]
                    self.disp.dprint("\t\tLoaded Enemy %s" % e)
                for q in self.packs[pack]["quests"]:
                    self.quests[q] = loadJson("%s%s/quests/%s.json" % (folder, pack, q))
                    self.disp.dprint("\t\tLoaded Quest %s" % q)
                for e in self.packs[pack]["events"]:
                    self.events[e] = loadJson("%s%s/events/%s.json" % (folder, pack, e))
                    if "injectArea" in self.events[e].keys():
                        for aKey in self.events[e]["injectArea"].keys():
                            injectionEvent = [e, self.events[e]["injectArea"][aKey]]
                            self.areas[aKey]["events"].append(injectionEvent)
                            if "injectAreaMinChance" in self.events[e].keys():
                                self.areas[aKey]["eventChance"] = max(self.areas[aKey]["eventChance"],
                                                                      self.events[e]["injectAreaMinChance"])
                    self.disp.dprint("\t\tLoaded Event %s" % e)
                for m in self.packs[pack]["modifiers"]:
                    mods = loadJson("%s%s/modifiers/%s.json" % (folder, pack, m))
                    for mod in mods.keys():
                        self.modifiers[mod] = Modifier(mod, mods[mod])
                    self.disp.dprint("\t\tLoaded Modifier %s" % m)
                for d in self.packs[pack]["dialogue"]:
                    dialogueData = loadJson("%s%s/dialogue/%s.json" % (folder, pack, d))
                    if "additionalDialogue" in dialogueData["flags"]:
                        for line in dialogueData["additionalDialogue"]:
                            self.dialogue[d]["lines"].append(line)
                    else:
                        self.dialogue[d] = dialogueData
                    self.disp.dprint("\t\tLoaded Dialogue %s" % d)
                print(f"\tFinished loading assets for pack {pack}.")

        # Adds all loaded quests into a list of possible quests, as well as
        # loads thems into actual objects
        for quest in self.quests.keys():
            self.possibleQuests.append(Quest(self.quests[quest]))
        if DEBUG:
            for q in self.possibleQuests:
                self.disp.dprint(q)
        
        self.nonRepeatableEvents = []
        self.globalRandomEvents = []
        # Load the global random events:
        for event in self.events.keys():
            if "globalEvent" in self.events[event].keys():
                if self.events[event]["globalEvent"]:
                    self.globalRandomEvents.append([event, self.events[event]["eventChance"]])

        self.loadStartingArea()
        self.loaded = True

    def loadStartingArea(self):
        if self.gameSettings["TUTORIALAREA"]:
            self.areaController = AreaController(self.areas, random.choice(self.packs[self.starter]["tutorialArea"]),
            self.weapons, self.armor, self.misc, self.enemies, self.races, self.npcs, self.events, self.modifiers, self.dialogue)
        else:
            self.areaController = AreaController(self.areas, random.choice(self.packs[self.starter]["startingArea"]),
            self.weapons, self.armor, self.misc, self.enemies, self.races, self.npcs, self.events, self.modifiers, self.dialogue)

    def loadPlayer(self):

        self.player.disp = self.disp
        
        for weapon in self.player.getStartingWeapons():
            # TODO: Allow for starting armors to have modifiers
            modifiers = None
            # TODO: Implement the ability to equip multiple weapons
            self.player.weapon = generateWeapon(self.weapons[weapon], modifiers)
        for armor in self.player.getStartingArmor():
            # TODO: Allow for starting armors to have modifiers
            modifiers = None
            armorSet = generateAmorSet(self.armor[armor[0]], modifiers, armor[1])
            self.player.equipArmorSet(armorSet)

        # Add all the extra inventory gear
        for item in self.player.getStartingInventory():
            newItem = None
            if item in self.misc.keys():
                newItem = Misc(self.misc[item], self.modifiers)
            elif item in self.weapons.keys():
                newItem = generateWeapon(self.weapons[item], self.modifiers)
            elif item in self.armor.keys():
                newItem = Armor(self.armor[item])
            if newItem != None:
                self.player.inv.append(newItem)
            

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
        self.dialogue = {}

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

    def close_display(self):
        if self.displayIsInitialized:
            self.disp.close_window()
            self.displayIsInitialized = False

    def displayCurrentArea(self):
        '''Displays info on the area the player is currently in.'''
        self.disp.clearScreen()
        title = "%s (%s) - Hostility: %d" % (self.areaController.getCurrentAreaName(),
                self.areaController.getCurrentAreaType(), self.areaController.getCurrentAreaHostility())
        self.disp.displayHeader(title)
        for desc in self.areaController.getCurrentAreaDesc().split("\n"):
            self.disp.display(desc)
        # Display enemies that are in the area (if there are any)
        if self.areaController.getCurrentAreaHasEnemies() and self.areaController.getCurrentAreaNeedToFight():
            self.disp.closeDisplay()
            enemyMessage = "You can see enemies in the distance:"
            if self.areaController.getCurrentAreaEnemyMessage() != None:
                enemyMessage = self.areaController.getCurrentAreaEnemyMessage()
            self.disp.display(enemyMessage, 1, 1)
            for enemy in self.areaController.getCurrentAreaEnemies():
                self.disp.display(f'{enemy.getName()} (Danger - {enemy.getDanger()})', 0, 0)
        self.disp.closeDisplay()

        # input("\nEnter to continue")
        self.disp.wait_for_enter()
        self.workOnBacklog()

    def reactCurrentArea(self):
        '''This is where the player becomes able to respond to any action that
        has occured within the game, such as enemies appearing, or quest
        objectives getting updated.'''

        ##### Random event Code #####
        if self.areaController.getCurrentAreaHasEvent(self.gameSettings["DISABLEFLAVOREVENTS"]):
            event = self.areaController.getCurrentAreaEvent()
            self.disp.dprint(event.name)
            while not event.finished:
                self.disp.clearScreen()
                self.disp.displayHeader(event.name)
                self.disp.display(event.msg, 1)
                x = 0
                choices = event.getPossibleActions(self.player)
                if len(choices) > 0:
                    self.disp.displayHeader("Actions", 1, 1)
                    for choice in choices:
                        x += 1
                        action = choice["action"]
                        self.disp.display(f'{x}. {action}', 0)
                    self.disp.closeDisplay()

                    try:
                        #cmd = int(input())
                        cmd = self.disp.get_input(True)
                    except:
                        cmd = -1
                    if cmd > 0 and cmd <= x:
                        for action in choices[cmd-1]["eventDo"]:
                            self.disp.dprint(action)
                            if action[0] == "say":
                                self.displayEventAction(action[1])
                            elif action[0] == "goto":
                                event.gotoPart(random.choice(action[1]))
                            elif action[0] == "addTag":
                                self.player.tags.append(event.getTag(action[1]))
                            elif action[0] == "take":
                                event.takeItem(action[1], action[2], self.player)
                            elif action[0] == "give":
                                for i in range(action[2]):
                                    result = event.giveItem(action[1], action[2], self.player, self.weapons,
                                                            self.armor, self.misc, self.modifiers)
                                    if self.settings["DEBUG"] and not result:
                                        raise Exception("Something went wrong when processing an event's 'give' command.")
                            elif action[0] == "spawnEnemy":
                                for enemyid in action[1]:
                                    self.areaController.addEnemyToCurrentArea(Enemy(
                                        self.enemies[enemyid], self.weapons, self.armor, self.misc, self.modifiers))
                            elif action[0] == "finish":
                                event.finish()
                else:
                    self.disp.closeDisplay()
                    event.finish()
                    #input("\nEnter to continue")
                    self.disp.wait_for_enter()
        else:
            self.areaController.clearEvent()

        self.fightEnemies()
        self.areaController.foughtCurrentAreaEnemies()
        if self.player.quit:
            return None

    def displayEventAction(self, message):
        self.disp.clearScreen()
        self.disp.displayHeader(self.areaController.getCurrentAreaEvent().name)
        self.disp.display(message)
        self.disp.closeDisplay()
        # input("\nEnter to continue")
        self.disp.wait_for_enter()

    def fightEnemies(self):
        ##### Fighting Code #####
        if self.areaController.getCurrentAreaNeedToFight() and self.areaController.getCurrentAreaHasEnemies() and not self.gameSettings["DISABLEENEMIES"]:
            self.disp.clearScreen()
            for areaEnemy in self.areaController.getCurrentAreaEnemies():
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
                    self.disp.clearScreen()
                    while not ((int(cmd) <= 2 and int(cmd) >= 0) or (cmd == 90 and DEBUG)):
                        self.disp.displayHeader("Enemy Encountered - %s" % (areaEnemy.name))
                        self.disp.display("%s The enemy has a danger level of %d." %
                                          (areaEnemy.getDesc(), areaEnemy.getDanger()), 1, 1)
                        self.disp.displayHeader("Info")
                        self.disp.display("Player: %s - %dHP" % (self.player.name, self.player.hp))
                        self.disp.display("HP: %s" % ("#" * self.player.getHealth()), 0)
                        self.disp.display("Weapon: %s" % (str(self.player.weapon)), 0)
                        self.disp.display("Enemy: %s - %dHP" % (areaEnemy.name, areaEnemy.hp))
                        self.disp.display("HP: %s" % ("#" * areaEnemy.getHealth()), 0)
                        self.disp.display("Weapon: %s" % (str(areaEnemy.weapon)), 0, 1)
                        self.disp.displayHeader("Actions")
                        self.disp.display("1. Use your weapon (%s)" % str(self.player.weapon))
                        self.disp.display("2. Attempt to escape", 0)
                        self.disp.display("0. Player Menu")
                        self.disp.closeDisplay()
                        try:
                            # cmd = int(input())
                            cmd = self.disp.get_input(True)
                            if not self.disp.window_is_open:
                                self.player.quit = True
                                return None
                            self.disp.clearScreen()
                        except ValueError:
                            self.disp.clearScreen()
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
                        elif cmd not in (1, 2, 0):
                            self.disp.displayHeader("Error")
                            self.disp.display("That was not a valid response.", 1, 1)

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
                        self.disp.display("%s You dealt %d damage." % (msg, damage), 1, 1)
                        self.disp.displayHeader(areaEnemy.name)
                        damage = areaEnemy.getWeaponDamage()
                        damage -= self.player.getArmorDefence()
                        if damage < 0:
                            self.disp.display("You deflect %s's attack." % areaEnemy.name)
                        elif self.player.getDodge() - areaEnemy.getAccuracy() > random.randint(1,100):
                            self.disp.display("%s missed their attack." % (areaEnemy.name))
                        else:
                            self.player.hp -= damage
                            self.disp.display("%s %s dealt %d damage." % (areaEnemy.weapon.getAction(), areaEnemy.name, damage))
                        self.disp.closeDisplay()
                        # input("\nEnter to continue.")
                        self.disp.wait_for_enter()
                    elif cmd == 2:
                        self.disp.clearScreen()
                        escape = False
                        if random.randint(0, self.player.getArmorDefence() + areaEnemy.getWeaponDamage()) < 1 + areaEnemy.getArmorDefence():
                            escape = True
                        if escape:
                            self.disp.displayHeader("Escape Successful")
                            self.disp.display(
                                "You successfully escape from %s." % (areaEnemy.name))
                        else:
                            self.disp.displayHeader("Escape Failed")
                            self.disp.display("You fail to escape from %s." % (areaEnemy.name), 1, 1)
                            self.disp.displayHeader(areaEnemy.name)
                            damage = areaEnemy.weapon.damage
                            damage += "-{0}".format(self.player.getArmorDefence())
                            damage = rollDice(damage)
                            if damage < 0:
                                damage = 0
                            self.player.hp -= damage
                            self.disp.display("%s %s dealt %d damage." % (
                                areaEnemy.weapon.getAction(), areaEnemy.name, damage))
                        self.disp.closeDisplay()
                        self.disp.wait_for_enter()
                        if escape:
                            break

                    self.disp.clearScreen()
                    enemyhp = areaEnemy.hp

                if self.player.hp > 0 and areaEnemy.hp <= 0:
                    self.disp.clearScreen()
                    self.disp.displayHeader("Victory")
                    self.disp.display( "You defeated the enemy, and got %d experience." % areaEnemy.xp)
                    self.importantQuestInfo.append( ["isKilled", areaEnemy.eID, True, False])
                    self.disp.display("%s %s" % (areaEnemy.name, areaEnemy.deathMsg))
                    if random.randint(1, 100) < areaEnemy.itemChance:
                        self.disp.display("")
                        self.disp.displayHeader("Reward")
                        itemMessage = areaEnemy.itemDrop[1].replace("$name", areaEnemy.name)
                        self.disp.display(itemMessage)
                        self.disp.display("You recieved %s." % (areaEnemy.itemDrop[0].name))
                        self.player.inv.append(areaEnemy.itemDrop[0])
                    self.disp.closeDisplay()
                    self.disp.wait_for_enter()
                    self.player.giveXP(areaEnemy.xp)

                # UPDATE QUEST INFO
                self.updateQuestInfo()
                self.workOnBacklog()
    
    def areaHub(self):
        ''' Acts as the area hub if there are NPCs'''
        npcList = self.areaController.getCurrentAreaNPCs()
        if len(npcList) > 0:
            npcDialogCheck = False
            while True:
                self.disp.clearScreen()
                self.disp.displayHeader(f"{self.areaController.getCurrentAreaName()}")
                if not npcDialogCheck and random.randint(0,100) > 25:
                    # Random NPC idle dialog
                    query = self.generateDialogueQuery("idle")
                    playerQuery = self.player.getPlayerQuery()
                    fullQuery = {**query, **playerQuery}
                    npc = random.choice(npcList)
                    npcdialog = npc.getDialogueLine(fullQuery)
                    self.disp.display("You hear someone mutter something.")
                    self.disp.display(f"{npc.getName()} - \"{npcdialog}\"  ")
                    self.disp.closeDisplay()
                    npcDialogCheck = True
                i = 1
                self.disp.display("1. Travel")
                for npc in npcList:
                    i+=1
                    npcProfessions = npc.getProfessions()
                    if len(npcProfessions) > 0:
                        npcProfessions = ", ".join(npcProfessions).upper()
                        self.disp.display(f"{i}. [{npcProfessions}] - {npc.getName()}")
                    else:
                        self.disp.display(f"{i}. {npc.getName()}")
                    pass
                self.disp.display("0. Player Menu")
                self.disp.closeDisplay()
                cmd = self.disp.get_input(True)
                if cmd == 1:
                    if self.chooseNewArea(True):
                        return None
                elif cmd == 0:
                    self.player.playerMenu(self.currentQuests, self.completedQuests)
                if self.player.quit:
                    return None
            '''
            query = self.generateDialogueQuery()
            # Add selections
            self.player.converseNPC(self.areaController.getCurrentAreaNPCs()[0], query)
            self.chooseNewArea(False)'''
        else:
            return self.chooseNewArea(False)
    
    def generateDialogueQuery(self, action = None):
        query = {
            "inAreaId":self.areaController.getCurrentAreaId(),
            "inAreaType":self.areaController.getCurrentAreaType()#,
            #"inAreaMinHostility":
        }
        if action:
            query["isAction"] = action
        return query

    def chooseNewArea(self, canCancel=True):
        '''This lets the player choose a new area to travel to.
           Returns True if travel occured, otherwise False'''
        # Create various area choices:
        choices = self.areaController.getCurrentAreaExits(self.nonRepeatableEvents, self.globalRandomEvents)
        # Shuffle the choices to make sure "required" areas don't always appaear first
        random.shuffle(choices)
        cmd = -1
        travelTypes = self.areaController.getTravelableTypes()

        # Allow the player to choose from those places:
        while not len(travelTypes) < cmd < len(choices) + len(travelTypes) + 1:
            self.disp.clearScreen()
            self.disp.displayHeader("Travel")
            self.disp.display("", 1, 0)
            x = 0
            if len(travelTypes) > 0:
                for category in travelTypes:
                    x += 1
                    self.disp.display("%d. %s Travel Locations" % (x, category.capitalize()), 0)
                self.disp.display("", 1, 0)
            for area in choices:
                x += 1
                self.disp.display("%d. %-37s %12s   Hostility - %2d" %
                                  (x, area.name, area.aType, area.hostility), 0)
            if canCancel:
                self.disp.display("0. Back")
            else:
                self.disp.display("0. Player Menu")
            self.disp.closeDisplay()
            try:
                cmd = self.disp.get_input(True)
                # Make sure the GUI window is still open. Exit if it is not
                if not self.disp.window_is_open:
                    self.player.quit = True
                    return None
            except ValueError:
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display("That was not a valid response.")
                self.disp.closeDisplay()
                cmd = -1
                self.disp.wait_for_enter()

            # Load the new area
            if 0 < cmd <= len(travelTypes):
                if self.chooseLoadedArea(travelTypes[cmd-1]):
                    return True
            elif cmd == 0:
                if canCancel:
                    return False
                else:
                    self.player.playerMenu(self.currentQuests, self.completedQuests)
                    if self.player.quit:
                        # TODO Exit the game completely
                        return False

        if cmd > len(travelTypes):
            cmd -= len(travelTypes)
        self.areaController.setAndLoadCurrentArea(choices[cmd - 1], self.weapons, self.armor,
                            self.misc, self.enemies, self.races, self.npcs, self.events, self.modifiers, self.dialogue)
        
        self.updateTravelInfoForQuests()

        return True
    
    def chooseLoadedArea(self, loadedKey):
        ''' Displays a list of areas that match the loadedKey and are not the current area '''
        choices = self.areaController.getSavedAreas(loadedKey)
        cmd = -1
        for area in choices:
            if self.areaController.getCurrentArea() == area:
                choices.remove(area)

        while not 1 <= cmd <= len(choices):
            print("CMD: " + str(cmd) + " | Areas: " + str(len(choices)))
            self.disp.clearScreen()
            self.disp.displayHeader("Travel to %s Location" % loadedKey.capitalize())
            x = 0
            for area in choices:
                x += 1
                self.disp.display("%d. %s" % (x, area.getName()))
            self.disp.display("0. to exit")
            self.disp.closeDisplay()
            try:
                cmd = self.disp.get_input(True)
                # Make sure the GUI window is still open. Exit if it is not
                if not self.disp.window_is_open:
                    self.player.quit = True
                    return None
            except ValueError:
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display("That was not a valid response.")
                self.disp.closeDisplay()
                cmd = -1
                self.disp.wait_for_enter()
            if cmd == 0:
                return None
        self.areaController.setCurrentArea(choices[cmd - 1])
        self.updateTravelInfoForQuests()
        return True
    
    def updateTravelInfoForQuests(self):
        if self.areaController.getCurrentAreaHasEvent():
            if not self.areaController.getCurrentAreaEvent().isRepeatable:
                self.nonRepeatableEvents.append(self.areaController.getCurrentAreaEvent().resourceId)

        self.importantQuestInfo.append(["inAreaType", self.areaController.getCurrentAreaType(), True, False])
        self.importantQuestInfo.append(["inAreaId", self.areaController.getCurrentAreaId(), True, False])

        self.updateQuestInfo()

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
                self.disp.wait_for_enter()
                self.disp.dprint("Processed say condition.")
            elif action[0] == "giveXP":
                self.player.xp += action[1]
                self.disp.display("You gained %d experience." % action[1])
                self.disp.dprint("Processed giveXP condition.")
            elif action[0] == "giveItem":
                itemKey = action[1]
                item = None
                if itemKey in self.weapons.keys():
                    item = generateWeapon(self.weapons[itemKey], self.modifiers)
                elif itemKey in self.misc.keys():
                    item = Misc(self.misc[itemKey], self.modifiers)
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
                for enemyid in action[1]:
                    self.areaController.addEnemyToCurrentArea(
                        Enemy(self.enemies[enemyid], self.weapons, self.armor, self.misc, self.modifiers))
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
    
    def newGameMenu(self):
        ''' This displays all required info for a player to start a new game '''
        cmd = -1
        ready = False
        playerName = ""
        playerRace = "human"
        while self.disp.window_is_open:
            if playerName != "" and playerRace != "":
                ready = True
            self.disp.clearScreen()
            self.disp.displayHeader("New Game")
            self.disp.display("Name: %s" % playerName)
            if playerRace == "":
                self.disp.display("Race: ")
            else:
                r = Race(self.races[playerRace])
                self.disp.display("Race: %s" % (r.getName()))
                self.disp.display(f"\t{r.getPlayerCreationDescription()}",0)
                self.disp.display("\t%s" %(r.getDescription()),0)
                self.disp.closeDisplay()
                self.disp.display("Stats:")
                self.disp.display(f'\tStrength     - {r.getStat("strength")}', 0)
                self.disp.display(f'\tVitality     - {r.getStat("vitality")}', 0)
                self.disp.display(f'\tPhysique     - {r.getStat("physique")}', 0)
                self.disp.display(f'\tIntelligence - {r.getStat("intelligence")}', 0)

            self.disp.closeDisplay()
            self.disp.display("1. Change Name")
            self.disp.display("2. Change Race", 0)
            self.disp.display("3. [DISABLED] Change Stats", 0)
            self.disp.display("4. [DISABLED] Change Skills", 0)
            self.disp.display("5. [DISABLED] Randomize All", 1, 1)
            if ready:
                self.disp.display("9. Start", 0)
            self.disp.display("0. Exit", 0)
            self.disp.closeDisplay()
            cmd = self.disp.get_input(True)
            if ready and cmd == 9:
                self.player = Player()
                self.player.setName(playerName)
                self.player.setRace(Race(self.races[playerRace]))
                return True
            elif cmd == 0:
                # Returns a None which causes the game to return to the main menu
                return None
            elif cmd == 1:
                playerName = self.newGameSetName(playerName)
            elif cmd == 2:
                playerRace = self.newGameSetRace(playerRace)
            elif cmd == 3:
                # TODO Randomize Money
                pass
            elif cmd == 4:
                # TODO Randomize race
                pass
            elif cmd == 5:
                # TODO Randomize full character
                pass
    
    def newGameSetName(self, currentName):
        self.disp.clearScreen()
        self.disp.displayHeader("Name Select")
        self.disp.display("Current Name: %s" % currentName)
        self.disp.display("Enter your desired name")
        self.disp.display("0. to Cancel")
        self.disp.closeDisplay()
        name = self.disp.get_input()
        if name == "0" or name == "":
            return currentName
        return name

    def newGameSetRace(self, currentRace):
        r = Race(self.races[currentRace])
        # Get all races to display
        races = []
        for raceData in self.races:
            additionalRace = Race(self.races[raceData])
            if additionalRace.getPlayeable():
                races.append(additionalRace)

        # Show menu to choose race:
        while True:
            self.disp.clearScreen()
            self.disp.displayHeader("Race Select")
            self.disp.display("Current Race: %s" % r.getName(False))
            self.disp.display(f"\t{r.getPlayerCreationDescription()}",0)
            self.disp.closeDisplay()
            self.disp.display("Choices:")
            x = 0
            for race in races:
                x += 1
                self.disp.display(f"\t{x}. {race.getName(False)} - {race.getShortDescription()}")
            self.disp.closeDisplay()
            self.disp.display("0. to Cancel")
            self.disp.closeDisplay()
            # Get input, convert to int
            cmd = self.disp.get_input(True)
            if 1 <= cmd <= len(races):
                # Display further race info
                if self.newGameRaceInspect(races[cmd-1]):
                    return races[cmd-1].getId()
            elif cmd == 0:
                # Cancel race selection
                return currentRace
    
    def newGameRaceInspect(self, race):
        self.disp.clearScreen()
        self.disp.displayHeader(f"Race Select: {race.getName(False)}")
        self.disp.display(f"Select {race.getName(False)}?")
        self.disp.display(f"Stats:")
        self.disp.display(f'\tStrength     - {race.getStat("strength")}', 0)
        self.disp.display(f'\tVitality     - {race.getStat("vitality")}', 0)
        self.disp.display(f'\tPhysique     - {race.getStat("physique")}', 0)
        self.disp.display(f'\tIntelligence - {race.getStat("intelligence")}', 0)
        self.disp.display(f"Description:")
        self.disp.display(f"\t{race.getPlayerCreationDescription()}", 0)
        self.disp.display(f"\t{race.getPureRaceDescription()}", 0)
        self.disp.closeDisplay()
        self.disp.display("1. to Confirm")
        self.disp.display("Anything else to cancel", 0)
        self.disp.closeDisplay()
        if self.disp.get_input(True, True, True) == 1:
            return True
        return False

    def displayMainMenu(self):
        self.disp.dprint("Debug Arguments: {}".format(self.settings["DEBUG"]))

        self.disp.clearScreen()
        self.disp.displayHeader("Main Menu")

        logo = random.choice(self.logos)
        firstLine = logo[0]
        self.disp.display(firstLine)
        for line in logo[1:]:
            self.disp.display(line, 0)
        
        self.disp.display(f'Version: {self.settings["VERSION"]}')
        self.disp.display(random.choice(self.descs))
        self.disp.closeDisplay()

        self.disp.display("1. New Game")
        # TODO: Check for save files and display below option if there are any
        if False:
            self.disp.display("2. Load Game", 0)
        self.disp.display("3. Settings")
        self.disp.display("4. Data Packs", 0)
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
                # cmd = int(input())
                cmd = self.disp.get_input(True)
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
        self.disp.closeDisplay()
        self.disp.display( "Input option # to toggle. Settings take effect on screen exit.")
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
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except ValueError:
                cmd = -1

            if cmd in range(1, 9) and cmd-1 <= len(toggleablePacks):
                packId = self.dataPackSettings["packsToLoad"][cmd-1+9*packPage][0]
                # Display pack info and toggle if the user responds affirmative
                loadString = f'{self.dataPackSettings["folder"]}{packId}/meta.json'
                packData = loadJson(loadString)
                enabled = "ENABLED" if self.dataPackSettings["packsToLoad"][cmd-1+9*packPage][1] else "DISABLED"
                toggle = self.displayPackDetails(packData, enabled)
                if toggle:
                    if not self.dataPackSettings["start"] == packId and not packData["packType"] == "standalone":
                        self.dataPackSettings["packsToLoad"][cmd-1+9*packPage][1] ^= True
                    # TODO Disable current standalone pack and enable new one
                    '''
                    elif not self.dataPackSettings["start"] and packData["packType"] == "standalone":
                        self.dataPackSettings["packsToLoad"][cmd-1+9*packPage][1] ^= True
                    '''
            elif cmd == 12 and packPage < numPages:
                packPage += 1
            elif cmd == 11 and packPage > 0:
                packPage -= 1
            elif cmd == 0:
                dataPacksWindow = False

        self.settings["DATAPACKSETTINGS"] = self.dataPackSettings
    
    def displayPackDetails(self, pack, enabled):
        
        packName = pack["name"]
        packType = pack["packType"]
        packDesc = pack["desc"]
        packAuth = pack["author"]

        self.disp.clearScreen()
        self.disp.displayHeader(f'{packName}')

        self.disp.display(f'{packName}')
        self.disp.display(f'Status: {enabled}')
        self.disp.display(f'Author: {packAuth}')
        self.disp.display(f'Info: {packDesc}')
        self.disp.display(f'Type:{packType}')

        self.disp.closeDisplay()
        if pack["packType"] == "standalone" and enabled:
            self.disp.display("INFO: This data pack cannot be disabled. You must enabled a different " +
                              "\"standalone\" data pack in order for this one to be disabled.")
            self.disp.display("Enter to exit")
        elif pack["packType"] == "standalone" and not enabled:
            self.disp.display("1. to change the currently active \"standalone\" data pack to this one")
            self.disp.display("Anything else to cancel", 0)
        else:
            self.disp.display("1. to toggle status")
            self.disp.display("Anything else to cancel", 0)
        self.disp.closeDisplay()
        return self.disp.get_input(True, True, True) == 1

    def displayPacks(self, numPages=1, page=0):
        self.disp.clearScreen()
        self.disp.displayHeader("Data Packs")

        startOptions = page*9
        endOptions = 9+(page*9)

        i = 0
        listOfOptions = self.dataPackSettings["packsToLoad"][startOptions:endOptions]

        for pack in listOfOptions:
            i += 1
            enabled = "ENABLED" if pack[1] else "DISABLED"
            pack = loadJson(f'{self.dataPackSettings["folder"]}{pack[0]}/meta.json')
            packName = pack["name"]
            packType = pack["packType"]
            packAuth = pack["author"]

            self.disp.display(f'{i}. {packName:<50} {enabled:>18}')
            self.disp.display(f'\tPack Type: {packType.upper()} | Author: {packAuth}', 0)
        self.disp.closeDisplay()
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

    # GAME SHUTDOWN
    def shutdown_game(self):
        self.close_display()