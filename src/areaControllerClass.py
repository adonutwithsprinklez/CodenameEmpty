
import copy

from areaClass import Area
from dialogueRules import evaluateDialogueLine
from gameDataHandler import GameDataHandler
from dieClass import rollDice


class AreaController(object):
    ''' This class generates and stores all needed data for the world. Whenever
        a new area needs generated or reloaded this class will handle it. '''
    def __init__(self, startingAreaID=None, DEBUG = 0):
        self.currentArea = None

        self.savedAreas = {
            "important":[],
            "local":[],
            "conditional":[]
        }

        self.areasAddedByEvents = []
        self.areasRemovedByEvents = []

        self.gameData:GameDataHandler = GameDataHandler()

        self.generatedExits = False
        self.currentExits = []
        self.initializeStartingArea(startingAreaID)

    def initializeStartingArea(self, startingAreaID=None):
        ''' Generates the starting area for the game. '''
        self.generateArea(startingAreaID)
        self.currentArea.enemy = [] # Make sure no enemies spawn in the starting area
        self.currentArea.foughtEnemies()

    def generateArea(self, areaType=None):
        ''' Generates an area of the specified type then sets it as the current area '''
        self.setAndLoadCurrentArea(Area(self.gameData.getGameData("area", areaType), [], [], areaType))
    
    def loadCurrentArea(self):
        ''' Calls the current area's "load" function '''
        self.currentArea.load(self.gameData)
        self.generatedExits = False
        self.currentExits = []
        self.areasAddedByEvents = []
        self.areasRemovedByEvents = []
    
    def setAndLoadCurrentArea(self, area):
        ''' Sets the current area and loads it in a single call'''
        self.setCurrentArea(area)
        self.loadCurrentArea()
        for category in self.currentArea.revisitable:
            if self.currentArea not in self.savedAreas[category]:
                self.savedAreas[category].append(self.getCurrentArea())
    
    def setCurrentArea(self, area):
        ''' Sets the current area '''
        self.currentArea = area

    
    def clearEvent(self):
        ''' Wipes any event that is in the current area '''
        self.currentArea.event = None
    
    def addEnemyToCurrentArea(self, enemy):
        ''' Adds the passed enemy to the list of enemies in the current area '''
        self.currentArea.addEnemy(enemy)
    
    def foughtCurrentAreaEnemies(self):
        self.currentArea.foughtEnemies()
    
    def addExitToArea(self, area):
        data = [area, "+1", ["required", "limited"]]
        self.currentArea.newAreaTypes.append(data)
        self.currentArea.newArea += 1
    
    def addExitToAreaFromEvent(self, area):
        data = [area, "+1", ["required", "limited"]]
        self.areasAddedByEvents.append(data)
    
    def removeExitToAreaFromEvent(self, area):
        for areaData in self.areasAddedByEvents:
            if areaData[0] == area:
                self.areasAddedByEvents.remove(areaData)
        self.areasRemovedByEvents.append(area)

    # GETTERS
    # Getters for current Area Data
    def getCurrentArea(self):
        ''' Returns the current area as an Area object '''
        return self.currentArea
    
    def getCurrentAreaName(self):
        ''' Returns the current area name '''
        return self.currentArea.getName()

    def getCurrentAreaId(self):
        ''' Returns the current area ID '''
        return self.currentArea.getAreaId()

    def getCurrentAreaType(self):
        ''' Returns the current area type '''
        return self.currentArea.getAreaType()
    
    def getCurrentAreaDesc(self):
        ''' Returns the current area description '''
        return self.currentArea.getAreaDesc()
    
    def getCurrentAreaHasEnemies(self):
        ''' Returns a bool depending on if the current area has enemies or not '''
        return len(self.currentArea.getEnemies()) > 0
    
    def getCurrentAreaEnemies(self):
        ''' Returns a list of enemies in the current area '''
        return self.currentArea.getEnemies()
    
    def getCurrentAreaEnemyMessage(self):
        ''' Returns a list of enemies in the current area '''
        return self.currentArea.getEnemyMessage()

    def getCurrentAreaHostility(self):
        ''' Returns the current area hostility '''
        return self.currentArea.getHostility()
    
    def getCurrentAreaHasEvent(self, onlyNonFlavorTextEvents = False):
        ''' Returns a bool depending on if the current area has enemies or not '''
        event = self.currentArea.getEvent()
        if event:
            if event.eventType != "flavor" or not onlyNonFlavorTextEvents:
                return True
        return False
    
    def getCurrentAreaNeedToFight(self):
        return self.currentArea.getNeedToFight()

    def getCurrentAreaEvent(self):
        ''' Returns the current area event '''
        return self.currentArea.getEvent()
    
    def getCurrentAreaNPCs(self):
        return self.currentArea.getNPC()
    
    def getCurrentAreaIdleDialogChance(self):
        return self.currentArea.getIdleDialogChance()

    def getCurrentAreaExits(self, query, repeatableEvents, globalRandomEvents):
        ''' If self.generatedExits is False, generates a list of exits for the user to travel to next, based on the current area '''
        if not self.generatedExits:
            self.currentExits = self.generateCurrentAreaExits(query, repeatableEvents, globalRandomEvents)
            self.generatedExits = True
        return self.currentExits
    
    def checkAreaRequirements(self, rules, query)->bool:
        ''' Checks if the area requirements are met '''
        return evaluateDialogueLine(rules, query)

    
    def generateCurrentAreaExits(self, query, nonRepeatableEvents, globalRandomEvents):
        ''' Generates a list of exits for the user to travel to next, based on the current area '''
        choices = [] # This is a list of area IDs to actually generate
        usedAreas = [] # This is to guarantee that no "limited" areas are used more than once

        # Grab all possible areas and throw them into a seperate list. This is to
        # guarantee that they are generated.
        areatypes = self.currentArea.newAreaTypes[::]
        possibleAreas = []

        # Go through the list of areatypes and check if there are any requirements
        for area in areatypes:
            cancel = False
            if len(area)<3:
                area.append([])
            if len(area)>3:
                # Confirm these requirements are met, otherwise remove them from the list
                if not self.checkAreaRequirements(area[3], query):
                    cancel = True
            if "limited" in area[2] and area[0] in usedAreas:
                cancel = True
            if not cancel:
                possibleAreas.append(area)
        
        for i in range(self.currentArea.newArea + len(self.areasAddedByEvents) + 1):
            if len(possibleAreas) == 0:
                break
            currentRoll = 0
            newArea = None
            for area in possibleAreas:
                if "required" in area[2]:
                    newArea = area
                    break
                else:
                    newRoll = rollDice(area[1])
                    if newRoll > currentRoll:
                        currentRoll = newRoll
                        newArea = area
            if newArea:
                choices.append(newArea)
                possibleAreas.remove(newArea)
            

        exits = []
        for area in choices:
            newArea = Area(self.gameData.getGameData("area", area[0]), nonRepeatableEvents, globalRandomEvents, area[2])
            exits.append(newArea)
        return exits
    
    def getCurrentAreaRandomizeExits(self):
        return self.currentArea.getRandomizeExits()
    
    def getCurrentAreaTransitionSound(self):
        return self.currentArea.getTransitionSound()

    # Other Getters
    def getTravelableTypes(self):
        ''' Returns a list of the savedArea types that are not empty. '''
        areaTypes = []
        for key in self.currentArea.getIsSafeToTravelTo():
            areas = self.savedAreas[key][::]
            if self.getCurrentArea() in areas:
                areas.remove(self.getCurrentArea())
            if len(areas) > 0:
                areaTypes.append(key)
        return areaTypes

    def getSavedAreas(self, areaType=None):
        ''' If no argument is passed, then returns a dict with the current saved areas data.
            Otherwise returns a list of all areas saved under that "area type" key '''
        if not areaType:
            return self.savedAreas
        elif areaType in self.savedAreas.keys():
            return self.savedAreas[areaType]
        else:
            return None
