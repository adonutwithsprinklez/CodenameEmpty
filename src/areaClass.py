import copy
import random
import math

from dieClass import rollDice
from enemyClass import Enemy
from eventClass import Event
from textGeneration import generateString

class Area(object):
    def __init__(self,areaType,nonrepeatableevents=[],**kwargs):
        self.name = generateString(areaType)
        print(f'GENERATING AREA: {self.name}')
        self.desc = generateString(areaType, "desc")
        self.newArea = random.randint(areaType["minNewAreas"],areaType["maxNewAreas"])
        self.newAreaTypes = areaType["areas"]
        self.aType = areaType["aType"]
        self.enemy = []
        self.event = None
        self.npc = None
        self.hostility = random.randint(areaType["hostilityMin"],areaType["hostilityMax"])

        self.kwargs = kwargs
        
        if random.randint(1,100) <= areaType["eventChance"]:
            self.event = self.chooseAnEvent(areaType, nonrepeatableevents)
        
        # Enemy Generation/Spawning
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

        # Optional Area data tags
        datakeys = areaType.keys()
        self.enemyMessage = None
        if "enemyMessage" in datakeys and len(areaType["enemyMessage"]):
            self.enemyMessage = generateString(areaType, "enemyMessage")

        '''
        chance = areaType["enemyChance"]
        enemies = []
        c = math.pow(15,(self.hostility-2.0)/10.0)
        for enemy, echance in areaType["enemies"]:
            enemies+=[enemy]*echance
        for i in range(0,10):
            if len(self.enemy)<self.hostility:
                x = random.random()*chance
                if x<c:
                    self.enemy.append(random.choice(enemies))
        '''

        # NPC's not yet implemented
        chance = random.randint(0,areaType["npcChance"])
        if chance < 10 and chance != 0 and len(areaType["npcs"])>0:
            self.npc = random.choice(areaType["npcs"])
        
    def chooseAnEvent(self, areaType, nonrepeatableevents):
        areaChoices = areaType["events"][::]
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

    def load(self,weapons,armor,misc,enemies,npcs,events,modifiers):
        # Loads in the enemies and events with any objects that they may need
        if self.enemy != []:
            e = []
            for enemy in self.enemy:
                newEnemy = Enemy(enemies[enemy],weapons,armor,misc,modifiers)
                e.append(newEnemy)
            self.enemy = e
        if self.event:
            self.event = Event(events[self.event], self.event)
