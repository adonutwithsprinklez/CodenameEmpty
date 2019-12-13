
from areaClass import Area


class AreaController(object):
    def __init__(self, areaData = None, currentXY=(0,0)):
        self.areaMap = {}
        self.x = currentXY[0]
        self.y = currentXY[1]
        self.currentArea = None

        self.areaData = areaData

        self.initializeArea()

    def getArea(self, x=0, y=0):
        if x in self.areaMap.keys():
            if y in self.areaMap[x].keys():
                return self.areaMap[x][y]
            else:
                return None
        else:
            return None
    
    def getCurrentArea(self):
        return self.getArea(self.x, self.y)

    def getTravelLocations(self):
        pass

    def travelTo(self, travelLocation = 0):
        pass

