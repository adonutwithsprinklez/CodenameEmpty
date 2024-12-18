
import copy
import os
import time

from effectClass import Effect
from modifierClass import Modifier
from jsonDecoder import loadJson
from universalFunctions import getDataValue


class GameDataHandler(object):
    def __init__(self, datapackSettings={}, defaultResources={}, DEBUG=False):
        self.DEBUG = DEBUG
        # PRINT DEBUG STATUS NO MATTER WHAT
        print (f"Game Data Handler Debug = {self.DEBUG}")

        self.packs:dict = {} # Used to hold metadata for each datapack

        self.weapons:dict = {}
        self.armor: dict = {}
        self.misc: dict = {}
        self.areas: dict = {}
        self.races: dict = {}
        self.quests: dict = {}
        self.events: dict = {}
        self.npcs: dict = {}
        self.enemies: dict = {}
        self.modifiers: dict = {}
        self.dialogue: dict = {}
        self.effects: dict = {}

        self.logos: list = [] # List of logos
        self.descs: list = [] # List of descriptions

        self.datapackSettings = None
        self.resFolder = None
        self.defaultResources = None

        self.dp("Initializing GameDataHandler")

        self.refreshAssetReferences(datapackSettings, defaultResources)

        print("Done")

    def refreshAssetReferences(self, datapackSettings={}, defaultResources={}):
        ''' Refreshes the asset references '''
        self.clearAssetReferences()

        self.datapackSettings = datapackSettings
        self.resFolder = self.datapackSettings["folder"]
        self.defaultResources = defaultResources

        self.dp(f"Datapack Settings: {datapackSettings}")
        self.dp(f"Default Resources: {defaultResources}")

        self.loadData()

    def loadData(self):
        ''' Loads only the data required to start the game '''
        loadTimeStart = time.time()

        # Grab all of the data pack metadata
        for pack in self.datapackSettings["packsToLoad"]:
            # Check if pack is enabled
            if pack[1]:
                self.prepDatapack(pack)

        loadTimeEnd = time.time()
        # Print time no matter what
        print(f"Initial data loaded in {loadTimeEnd - loadTimeStart} seconds")

        # Load all files if debug to make sure nothing loaded improperly
        if self.DEBUG:
            loadTimeStart = time.time()
            for key in self.weapons.keys():
                self.weapons[key].load()
            for key in self.armor.keys():
                self.armor[key].load()
            for key in self.misc.keys():
                self.misc[key].load()
            for key in self.areas.keys():
                self.areas[key].load()
            for key in self.quests.keys():
                self.quests[key].load()
            for key in self.events.keys():
                self.events[key].load()
            for key in self.npcs.keys():
                self.npcs[key].load()
            for key in self.enemies.keys():
                self.enemies[key].load()
            for key in self.dialogue.keys():
                self.dialogue[key].load()
            loadTimeEnd = time.time()
            print(f"It took {loadTimeEnd-loadTimeStart} seconds")

    def prepDatapack(self, pack):
        packName = pack[0]
        packData = loadJson(f"{self.resFolder}{packName}/meta.json")
        self.packs[packName] = packData

        # Grab any logos and descriptions
        if "gameLogo" in packData.keys():
            self.logos.append(packData["gameLogo"])
        if "gameDesc" in packData.keys():
            for desc in packData["gameDesc"]:
                self.descs.append(desc)

        # Create all needed GameDataObjects for the Datapack:
        folder = self.datapackSettings["folder"]
        itemInjections = {}
        for w in self.packs[packName]["weapons"]:
            datafile = f"{folder}{packName}/weapons/{w}.json"
            self.weapons[w] = GameDataObject(datafile, "weapon")

            # Check if the weapon has a .inject files associated
            injectFile = f"{folder}{packName}/weapons/{w}.inject.json"
            if os.path.exists(injectFile):
                injectData = loadJson(injectFile)

                # Check if the weapon has an injectSeller key
                if "injectSeller" in injectData.keys():
                    for data in injectData["injectSeller"]:
                        if data[0] in itemInjections.keys():
                            itemInjections[data[0]].append([w, data[1]])
                        else:
                            itemInjections[data[0]] = [[w, data[1]]]
            self.dp("\t\tLoaded Weapon %s" % w)
        
        for a in self.packs[packName]["armor"]:
            datafile = f"{folder}{packName}/armor/{a}.json"
            self.armor[a] = GameDataObject(datafile, "armor")

            # Check if the armor has a .inject files associated
            injectFile = f"{folder}{packName}/armor/{a}.inject.json"
            if os.path.exists(injectFile):
                injectData = loadJson(injectFile)

                # Check if the armor has an injectSeller key
                if "injectSeller" in injectData.keys():
                    for data in injectData["injectSeller"]:
                        if data[0] in itemInjections.keys():
                            itemInjections[data[0]].append([a, data[1]])
                        else:
                            itemInjections[data[0]] = [[a, data[1]]]
            self.dp("\t\tLoaded Armor %s" % a)
        for m in self.packs[packName]["misc"]:
            datafile = f"{folder}{packName}/misc/{m}.json"
            self.misc[m] = GameDataObject(datafile, "misc")

            # Check if the misc item has a .inject files associated
            injectFile = f"{folder}{packName}/misc/{m}.inject.json"
            if os.path.exists(injectFile):
                injectData = loadJson(injectFile)

                # Check if the misc item has an injectSeller key
                if "injectSeller" in injectData.keys():
                    for data in injectData["injectSeller"]:
                        if data[0] in itemInjections.keys():
                            itemInjections[data[0]].append([m, data[1]])
                        else:
                            itemInjections[data[0]] = [[m, data[1]]]
            self.dp("\t\tLoaded Misc %s" % m)
        
        for a in self.packs[packName]["areas"]:
            datafile = f"{folder}{packName}/areas/{a}.json"
            self.areas[a] = GameDataObject(datafile, "area")

            # Check if the area has a .inject files associated
            injectFile = f"{folder}{packName}/areas/{a}.inject.json"
            if os.path.exists(injectFile):
                injectData = loadJson(injectFile)

                # Check if the area has an injectArea key
                if "injectArea" in injectData.keys():
                    for aKey in injectData["injectArea"].keys():
                        injection = {
                            "injectType":"area",
                            "areaId":aKey,
                            "chance":injectData["injectArea"][aKey]
                        }
                        self.areas[aKey].addInjection(injection)
            self.dp("\t\tLoaded Area %s" % a)

        # Load the fantasy race data
        for r in self.packs[packName]["races"]:
            datafile = f"{folder}{packName}/races/{r}.json"

            # Sadly, due to poor implementation, we have to load the data first to get the id
            data = GameDataObject(datafile, "race")
            data.load()
            self.races[data.getData()["id"]] = data

        for n in self.packs[packName]["npcs"]:
            self.npcs[n] = GameDataObject(f"{self.resFolder}{packName}/npcs/{n}.json", "npc")
            # self.npcs[n] = loadJson("%s%s/npcs/%s.json" % (folder, pack, n))
            self.dp("\t\tLoaded NPC %s" % n)
        
        for e in self.packs[packName]["enemies"]:
            datafile = f"{folder}{packName}/enemies/{e}.json"
            self.enemies[e] = GameDataObject(datafile, "enemy")

            # Check if the enemy has a .inject files associated
            injectFile = f"{folder}{packName}/enemies/{e}.inject.json"
            if os.path.exists(injectFile):
                injectData = loadJson(injectFile)

                # Check if the enemy has an injectArea key
                if "injectArea" in injectData.keys():
                    for injection in injectData["injectArea"]:
                        injectionEnemy = {
                            "injectType":"enemy",
                            "data":[e, injection[1]],
                            "areaMinEnemyChance":getDataValue("areaMinEnemyChance", injectData, 0),
                            "areaEnemyPointsPerHostility":getDataValue("areaEnemyPointsPerHostility", injectData, 0)
                        }
                        self.areas[injection[0]].addInjection(injectionEnemy)
        
        for q in self.packs[packName]["quests"]:
            datafile = f"{folder}{packName}/quests/{q}.json"
            self.quests[q] = GameDataObject(datafile, "quest")
            self.dp("\t\tLoaded Quest %s" % q)

        for e in self.packs[packName]["events"]:
            datafile = f"{folder}{packName}/events/{e}.json"
            self.events[e] = GameDataObject(datafile, "event")
            
            # Check if the event has a .inject files associated
            injectFile = f"{folder}{packName}/events/{e}.inject.json"
            if os.path.exists(injectFile):
                if "injectArea" in injectData.keys():
                    for aKey in injectData["injectArea"].keys():
                        injectData = {
                            "injectType":"event",
                            "data":[e, injectData["injectArea"][aKey]],
                            "eventChance":getDataValue("areaMinChance", injectData, 0)
                        }
            self.dp("\t\tLoaded Event %s" % e)
        
        for m in self.packs[packName]["modifiers"]:
            datafile = f"{folder}{packName}/modifiers/{m}.json"

            # Due to the way modifiers are implemented, we have to load the data first,
            # since each file contains multiple modifiers
            data = GameDataObject(datafile, "modifier")
            data.load()

            for mod in data.getData().keys():
                self.modifiers[mod] = Modifier(mod, data.getData()[mod])
            
        
        for d in self.packs[packName]["dialogue"]:
            datafile = f"{folder}{packName}/dialogue/{d}.json"
            if d not in self.dialogue:
                self.dialogue[d] = GameDataObject(datafile, "dialogue")
            else:
                # Dialogue already exists, add the new data to the existing object as an injection
                # The data object will handle which data is actually used when the time comes
                self.dialogue[d].addInjection(datafile)
            self.dp("\t\tLoaded Dialogue %s" % d)

        for ef in self.packs[packName]["effects"]:
            datafile = f"{folder}{packName}/effects/{ef}.json"

            # Like the modifiers, we have to load the data first, since each file contains multiple effects
            data = GameDataObject(datafile, "effect")
            data.load()
            
            for effect in data.getData().keys():
                self.effects[effect] = data.getData()[effect]
    
        # Inject items into sellers
        for seller in itemInjections.keys():
            for item in itemInjections[seller]:
                # self.npcs[seller]["itemPool"].append(item)
                self.npcs[seller].addInjection(item)

        # Check if this pack is the starting pack
        if self.datapackSettings["start"] == packName:
            pass

        print(f"\tFinished loading assets for pack {packName}.")
    
    def getGameData(self, category, key, forceReload=False):
        ''' Returns the data for a given category and key '''
        if category == "weapon":
            return self.weapons[key].getData(forceReload or self.DEBUG)
        elif category == "armor":
            return self.armor[key].getData(forceReload or self.DEBUG)
        elif category == "misc":
            return self.misc[key].getData(forceReload or self.DEBUG)
        elif category == "area":
            return self.areas[key].getData(forceReload or self.DEBUG)
        elif category == "race":
            return self.races[key].getData(forceReload or self.DEBUG)
        elif category == "quest":
            return self.quests[key].getData(forceReload or self.DEBUG)
        elif category == "event":
            return self.events[key].getData(forceReload or self.DEBUG)
        elif category == "npc":
            return self.npcs[key].getData(forceReload or self.DEBUG)
        elif category == "enemy":
            return self.enemies[key].getData(forceReload or self.DEBUG)
        elif category == "modifier":
            return self.modifiers[key]
        elif category == "effect":
            return self.effects[key]
        elif category == "dialogue":
            return self.dialogue[key].getData(forceReload or self.DEBUG)
        elif category == "pack":
            return self.packs[key]
        
        raise ValueError(f"Invalid category {category}")
    
    def getListOfKeys(self, category):
        ''' Returns a list of keys for the given category '''
        if category == "weapon":
            return list(self.weapons.keys())
        elif category == "armor":
            return list(self.armor.keys())
        elif category == "misc":
            return list(self.misc.keys())
        elif category == "area":
            return list(self.areas.keys())
        elif category == "race":
            return list(self.races.keys())
        elif category == "quest":
            return list(self.quests.keys())
        elif category == "event":
            return list(self.events.keys())
        elif category == "npc":
            return list(self.npcs.keys())
        elif category == "enemy":
            return list(self.enemies.keys())
        elif category == "modifier":
            return list(self.modifiers.keys())
        elif category == "effect":
            return list(self.effects.keys())
        elif category == "dialogue":
            return list(self.dialogue.keys())
        elif category == "pack":
            return list(self.packs.keys())
    
    def getLogos(self):
        return self.logos
    
    def getDescs(self):
        return self.descs

    def clearAssetReferences(self):
        self.packs:dict = {} # Used to hold metadata for each datapack

        self.weapons:dict = {}
        self.armor: dict = {}
        self.misc: dict = {}
        self.areas: dict = {}
        self.races: dict = {}
        self.quests: dict = {}
        self.events: dict = {}
        self.npcs: dict = {}
        self.enemies: dict = {}
        self.modifiers: dict = {}
        self.dialogue: dict = {}
        self.effects: dict = {}

        self.logos: list = [] # List of logos
        self.descs: list = [] # List of descriptions
    
    def dp(self,msg):
        ''' Debug print. Only prints if self.DEBUG is true '''
        if self.DEBUG:
            print(msg)


class GameDataObject(object):
    def __init__(self, dataFile="", datatype=""):
        self.dataFile:str = dataFile
        self.datatype:str = datatype
        ''' Possible data types include:
            - weapon
            - armor
            - misc
            - area
            - npc
            - enemy
            - quest
            - event
            - dialogue
            - modifier
            - effect '''
        self.injections:list = []
        self.data:dict = None

    def getLoaded(self):
        return self.data != None
    
    def getData(self, forceReload=False):
        # loads data if not yet loaded, or if force reload is enabled
        if forceReload or not self.getLoaded():
            self.load()
        return copy.copy(self.data) # Returns a copy so the original is never modified
    
    def load(self):
        ''' Loads the data from the associated json file'''
        try:
            newData = loadJson(self.dataFile)

            # Depending on the datatype, we may need to do some extra processing
            if self.datatype == "weapon":
                newData = self.loadWeapon(newData)
            elif self.datatype == "armor":
                newData = self.loadArmor(newData)
            elif self.datatype == "misc":
                newData = self.loadMisc(newData)
            elif self.datatype == "area":
                newData = self.loadArea(newData)
            elif self.datatype == "enemy":
                newData = self.loadEnemy(newData)
            elif self.datatype == "quest":
                newData = self.loadQuest(newData)
            elif self.datatype == "event":
                newData = self.loadEvent(newData)
            elif self.datatype == "dialogue":
                newData = self.loadDialogue(newData)
            elif self.datatype == "npc":
                newData = self.loadNpc(newData)
            ''' Modifiers, effects, and races are loaded differently,
                so we don't need to check for those.
            elif self.datatype == "modifier":
                newData = self.loadModifier(newData)
            elif self.datatype == "effect":
                newData = self.loadEffect(newData)
            elif self.datatype == "race":
                newData = self.loadRace(newData)
            '''

            print(f"Loaded data file {self.dataFile}")
        except Exception as e:
            print(f"Something went wrong loading data file {self.dataFile}")
            print(f"Error: {e}")
            newData = None
        self.data = newData
    
    def addInjection(self, injection):
        self.injections.append(injection)

    def unload(self):
        self.data = None
        print(f"Unloaded data file {self.dataFile}")

    def loadArea(self, data):   
        loadedData = data
        
        # Check for injections
        for injection in self.injections:
            if injection["injectType"] == "area":
                loadedData["areas"].append([injection["areaId"]] + injection["chance"])
            elif injection["injectType"] == "enemy":
                loadedData["enemies"].append(injection["data"])
                loadedData["minEnemyChance"] = max(injection["areaMinEnemyChance"],  getDataValue("minEnemyChance", loadedData, 0))
                loadedData["enemyPointsPerHostility"] = max(injection["areaEnemyPointsPerHostility"], getDataValue("enemyPointsPerHostility", loadedData, 0))
            elif injection["injectType"] == "event":
                loadedData["events"].append(injection["data"])
                loadedData["minChance"] = max(injection["eventChance"], getDataValue("minChance", loadedData, 0))
        return loadedData

    def loadNpc(self, data):
        loadedData = data
        # Add any additional processing for npc data here
        return loadedData

    def loadEnemy(self, data):
        loadedData = data
        # Add any additional processing for enemy data here
        return loadedData

    def loadQuest(self, data):
        loadedData = data
        # Add any additional processing for quest data here
        return loadedData

    def loadEvent(self, data):
        loadedData = data
        # Add any additional processing for event data here
        return loadedData

    def loadDialogue(self, data):
        loadedData = data
        
        # Check for injections
        for injection in self.injections:
            # Each injection is a file path to a json file
            # We will load the data from the file, and if it has a "additionalDialogue" flag, we will add it to the dialogue
            # Otherwise, all current dialogue will be replaced
            newData = loadJson(injection)
            if "flags" in newData.keys():
                if "additionalDialogue" in newData["flags"]:
                    for key in newData.keys():
                        if key != "flags":
                            loadedData[key] = newData[key]
                else:
                    loadedData = newData

        return loadedData
    
    ### Below load functions do not have any additional processing, so they
    ###  are are currently left as placeholders, for easier expansion later

    def loadWeapon(self, data):
        loadedData = data
        # Add any additional processing for weapon data here
        return loadedData

    def loadArmor(self, data):
        loadedData = data
        # Add any additional processing for armor data here
        return loadedData

    def loadMisc(self, data):
        loadedData = data
        # Add any additional processing for misc data here
        return loadedData