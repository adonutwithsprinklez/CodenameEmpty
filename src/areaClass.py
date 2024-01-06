import copy
import random
import math

from dieClass import rollDice
from enemyClass import Enemy
from eventClass import Event
from npcClass import NPC
from textGeneration import generateString
from universalFunctions import getDataValue

class Area(object):
    def __init__(self,areaType,nonrepeatableevents=[],globalEvents=[],areaId="",**kwargs):
        self.name = generateString(areaType)
        self.aId = areaId
        print(f'GENERATING AREA: {self.name}')
        self.desc = generateString(areaType, "desc")
        self.newArea = random.randint(areaType["minNewAreas"],areaType["maxNewAreas"])
        self.newAreaTypes = areaType["areas"]
        self.aType = areaType["aType"]
        self.enemy = []
        self.event = None
        self.npc = []
        self.npcId = []
        self.hostility = random.randint(areaType["hostilityMin"],areaType["hostilityMax"])
        self.enemyMessage = getDataValue("enemyMessage", areaType, None)
        self.revisitable = getDataValue("revisitable", areaType, [])
        self.isSafeToTravelTo = getDataValue("safeToTravel", areaType, [])
        self.transitionSound = getDataValue("transitionSound", areaType, None)
        self.randomizeExits = getDataValue("randomizeAreaOrder", areaType, True)

        self.kwargs = kwargs
        
        if random.randint(1,100) <= areaType["eventChance"] and len(areaType["events"])>0:
            self.event = self.chooseAnEvent(areaType, nonrepeatableevents, globalEvents)
        
        # Enemy Generation/Spawning
        self.needToFight = False
        chance = areaType["enemyChance"]
        try:
            hostilityAffectsEnemyChance = areaType["hostilityAffectsEnemyChance"]
            if hostilityAffectsEnemyChance:
                c = chance*self.hostility
        except:
            hostilityAffectsEnemyChance = False
            c = chance
        if c<0:
            c=0
        print("Enemy Chance: {}".format(str(c)))
        if random.randint(1,100) <= c:
            enemyPoints = self.hostility * areaType["enemyPointsPerHostility"]
            attempts = 1
            currentEnemyDanger = 0
            while currentEnemyDanger < enemyPoints and attempts <= 3:
                currentEnemyDanger = 0
                enemies = []
                possibleEnemies = copy.copy(areaType["enemies"])
                while len(possibleEnemies) > 0:
                    enemiesCheck = copy.copy(possibleEnemies)
                    possibleEnemies = []
                    for enemy in enemiesCheck:
                        if enemy[0] != "group" and enemy[1] <= enemyPoints - currentEnemyDanger:
                            # This enemy choice is not a group and has a low enough danger level
                            possibleEnemies.append(enemy)
                        elif enemy[0] == "group" and enemy[2] <= enemyPoints - currentEnemyDanger:
                            # This enemy choice is a group and has a low enough danger level
                            possibleEnemies.append(enemy)
                    if len(possibleEnemies) > 0:
                        newEnemy = random.choice(possibleEnemies)
                        # check if enemy is a group or not
                        if enemy[0] != "group":
                            # This is not a group, add them to the enemy list normally
                            currentEnemyDanger += newEnemy[1]
                            enemies.append(newEnemy[0])
                        else:
                            # this enemy is apart of a group, add them individually to the list
                            currentEnemyDanger += newEnemy[2]
                            for enemyid in newEnemy[1]:
                                enemies.append(enemyid)
                attempts += 1
            self.enemy = enemies
            self.needToFight = True

        self.idleDialogChance = 0
        numNPCs = rollDice(areaType["npcChance"])
        if numNPCs > 0 and len(areaType["npcs"])>0:
            self.npcId = random.sample(areaType["npcs"][::], k=numNPCs)
            if "idleDialogChance" in areaType.keys():
                self.idleDialogChance = areaType["idleDialogChance"]
            else:
                self.idleDialogChance = 50
        
    def chooseAnEvent(self, areaType, nonrepeatableevents, globalevents):
        areaChoices = copy.copy(areaType["events"])
        for event in globalevents:
            areaChoices.append(event)
        # Remove any non-repeatable events that have already occured
        for event in areaChoices:
            if event[0] in nonrepeatableevents:
                areaChoices.remove(event)
        currentEvent = areaChoices[0]
        highRoll = rollDice(currentEvent[1])
        for event in areaChoices[1:]:
            newRoll = rollDice(event[1])
            if newRoll > highRoll:
                currentEvent = event
                highRoll = newRoll
        return currentEvent[0]

    def load(self,weapons,armor,misc,enemies,races,npcs,events,modifiers,dialogue):
        # Loads in the enemies and events with any objects that they may need
        if self.enemy != []:
            e = []
            for enemy in self.enemy:
                newEnemy = Enemy(enemies[enemy],weapons,armor,misc,modifiers)
                e.append(newEnemy)
            self.enemy = e
        if self.event:
            self.event = Event(events[self.event], self.event)
        if len(self.npcId) > 0:
            print(self.npcId)
            for npcid in self.npcId:
                npc = NPC(npcs[npcid], npcid)
                npc.load(races, dialogue, armor, misc, weapons, modifiers)
                self.npc.append(npc)
    
    def addEnemy(self, enemy):
        self.enemy.append(enemy)
        self.needToFight = True
    
    def foughtEnemies(self):
        self.needToFight = False
        
    
    # GETTERS
    def getName(self):
        return self.name
        
    def getAreaId(self):
        return self.aId
        
    def getAreaType(self):
        return self.aType

    def getAreaDesc(self):
        return self.desc

    def getEnemies(self):
        return self.enemy
    
    def getEnemyMessage(self):
        if (type(self.enemyMessage) is list):
            return random.choice(self.enemyMessage)
        return self.enemyMessage
        
    def getHostility(self):
        return self.hostility
    
    def getEvent(self):
        return self.event
    
    def getNPC(self):
        return self.npc
    
    def getRevisitable(self):
        return self.revisitable
    
    def getIsSafeToTravelTo(self):
        return self.isSafeToTravelTo
    
    def getNeedToFight(self):
        return self.needToFight
    
    def getIdleDialogChance(self):
        return self.idleDialogChance
    
    def getRandomizeExits(self):
        return self.randomizeExits
    
    def getTransitionSound(self):
        if self.transitionSound != None:
            return random.choice(self.transitionSound)
        return None
    
    def __str__(self):
        return "Area ID: " + self.getAreaId() + " | Title: " + self.getName()

    def __eq__(self, comp):
        return comp.getAreaId() == self.getAreaId()