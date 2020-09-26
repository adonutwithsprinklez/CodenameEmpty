
from areaClass import Area


class AreaController(object):
    ''' This class generates and stores all needed data for the world. Whenever
        a new area needs generated or reloaded this class will handle it. '''
    def __init__(self, areaData=None, startingAreaID=None, currentXY=(0, 0),
                 weapons=None, armor=None, misc=None, enemies=None, npcs=None, events=None, modifiers=None,
                 DEBUG = 0):
        self.areaMap = {}
        self.x = currentXY[0]
        self.y = currentXY[1]
        self.currentArea = None

        self.areaData = areaData

        self.initializeStartingArea(
            startingAreaID, weapons, armor, misc, enemies, npcs, events, modifiers)

    def initializeStartingArea(self, startingAreaID=None,
                               weapons=None, armor=None, misc=None, enemies=None, npcs=None, events=None, modifiers=None):
        ''' Generates the starting area for the game. '''
        self.generateArea((self.x, self.y), startingAreaID, weapons,
                          armor, misc, enemies, npcs, events, modifiers)
        self.currentArea = self.loadCurrentArea()
        self.currentArea.enemy = [] # Make sure no enemies spawn in the starting area

    def generateArea(self, xy=(0, 0), areaType=None,
                     weapons=None, armor=None, misc=None, enemies=None, npcs=None, events=None, modifiers=None):
        ''' Generates an area at tthe specified location. '''
        if self.loadArea(xy) == None:
            if not xy[0] in self.areaMap.keys():
                self.areaMap[xy[0]] = {}
            newArea = Area(self.areaData[areaType])
            self.areaMap[xy[0]][xy[1]] = newArea
        self.currentArea = self.areaMap[xy[0]][xy[1]]
        self.currentArea.load(weapons, armor, misc, enemies, npcs, events, modifiers)

    def loadArea(self, xy=(0, 0)):
        ''' Attempts to load the specified area. If the specified area has not
            yet been generated, then it returns None. '''
        if xy[0] in self.areaMap.keys():
            if xy[1] in self.areaMap[xy[0]].keys():
                return self.areaMap[xy[0]][xy[1]]
            else:
                return None
        else:
            return None

    def loadCurrentArea(self):
        ''' If the current area has been generated previously, returns it.
            Otherwise generates a new area. '''
        currentArea = self.loadArea((self.x, self.y))
        if currentArea != None:
            return currentArea
        else:
            # TODO generate a new area
            return None

    def getTravelLocations(self):
        ''' Gets possible travel locations for the player and returns them as a
            list. '''
        pass

    def travelTo(self, travelLocation=0):
        ''' Causes the current location to change into the location that is
            being "travelled" to. '''
        pass
