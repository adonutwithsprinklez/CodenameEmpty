
from areaClass import Area
from dieClass import rollDice


class AreaController(object):
    ''' This class generates and stores all needed data for the world. Whenever
        a new area needs generated or reloaded this class will handle it. '''
    def __init__(self, areaData=None, startingAreaID=None, weapons=None,
    armor=None, misc=None, enemies=None, races=None, npcs=None, events=None, modifiers=None, dialogue=None, DEBUG = 0):
        self.currentArea = None

        self.savedAreas = {
            "important":[],
            "local":[],
            "conditional":[]
        }

        self.areaData = areaData

        self.initializeStartingArea(startingAreaID, weapons, armor, misc, enemies, races, npcs, events, modifiers, dialogue)

    def initializeStartingArea(self, startingAreaID=None, weapons=None, armor=None, misc=None,
                               enemies=None, races=None, npcs=None, events=None, modifiers=None, dialogue=None):
        ''' Generates the starting area for the game. '''
        self.generateArea(startingAreaID, weapons, armor, misc, enemies, races, npcs, events, modifiers, dialogue)
        self.currentArea.enemy = [] # Make sure no enemies spawn in the starting area
        self.currentArea.foughtEnemies()

    def generateArea(self, areaType=None, weapons=None, armor=None, misc=None, enemies=None,
                     races=None, npcs=None, events=None, modifiers=None, dialogue=None):
        ''' Generates an area of the specified type then sets it as the current area '''
        self.setAndLoadCurrentArea(Area(self.areaData[areaType], [], [], areaType), weapons, armor, misc,
                                        enemies, races, npcs, events, modifiers, dialogue)
    
    def loadCurrentArea(self, weapons=None, armor=None, misc=None, enemies=None, races=None, npcs=None,
                        events=None, modifiers=None, dialogue = None):
        ''' Calls the current area's "load" function '''
        self.currentArea.load(weapons, armor, misc, enemies, races, npcs, events, modifiers, dialogue)
    
    def setAndLoadCurrentArea(self, area, weapons=None, armor=None, misc=None, enemies=None, races=None, 
                              npcs=None, events=None, modifiers=None, dialogue=None):
        ''' Sets the current area and loads it in a single call'''
        self.setCurrentArea(area)
        self.loadCurrentArea(weapons, armor, misc, enemies, races, npcs, events, modifiers, dialogue)
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

    def getCurrentAreaExits(self, repeatableEvents, globalRandomEvents):
        ''' Generates a list of exits for the user to travel to next, based on the current area '''
        print("")
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

        # Check if all requirements are met for areas to spawn:
        # TODO

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
            generatedArea = Area(self.areaData[newArea[0]], repeatableEvents,
                                 globalRandomEvents, newArea[0])
            usedAreas.append(newArea[0])
            choices.append(generatedArea)
        return choices

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
