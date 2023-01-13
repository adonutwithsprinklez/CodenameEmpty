import random


from dieClass import rollDice


class Player(object):
    def __init__(self):
        self.name = "Player"
        self.hp = 50
        self.energy = 50
        self.level = 1
        self.xp = 0
        self.race = None
        self.perks = []
        self.weapon = None
        self.armor = None
        self.unarmed = 1
        self.gold = 0
        self.inv = []
        self.disp = None
        self.quit = False
        self.tags = []
        self.skills = []
        self.stats = {
            "strength":0,
            "vitality":0,
            "physique":0,
            "intelligence":0
        }

    def playerMenu(self, currentQuests, completedQuests):
        cmd = -1
        while cmd != 0 and not self.quit:
            self.disp.clearScreen()
            self.disp.displayHeader("{} Info ( {} )".format(self.name, self.race.name))
            self.disp.display("Quick Stats:")
            for stat in self.getUserInfo():
                self.disp.display(f'{stat[1]:>15} - {stat[0]}', 0)
            self.disp.display("Wielding:")
            if self.weapon != None:
                self.disp.display("\t%s (%s damage)" % (self.weapon.name, self.weapon.damage),0)
            else:
                self.disp.display("\tYou are not currently wielding a weapon",0)
            self.disp.display("Wearing:")
            for limb in self.race.getLimbsEquippableLimbs():
                if limb.armor:
                    self.disp.display("\t%s - %s (%s defence)" % (limb.name, limb.armor, limb.armor.getDefenceRating()),0)
                else:
                    self.disp.display("\t%s - Nothing" % (limb.name),0)
            #self.disp.display("\t- %s (%s defence)" % (self.armor, self.armor.defence))
            self.disp.closeDisplay()
            self.disp.display("1. View Inventory")
            self.disp.display("2. View Quests", 0)
            self.disp.display("3. View Player Details", 0)
            self.disp.display("4. View Skill Levels", 0)
            self.disp.display("9. Quit Game")
            self.disp.display("0. Exit", 0)
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except:
                cmd = -1
            if cmd == 0:
                pass
            elif cmd == 1:
                self.viewInventory()
            elif cmd == 2:
                self.viewQuests(currentQuests, completedQuests)
            elif cmd == 3:
                self.viewPlayerDetails()
            elif cmd == 4:
                self.viewPlayerLevels()
            elif cmd == 9:
                self.confirmQuit()
            else:
                if not self.disp.window_is_open:
                    self.quit = True
                    return None
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display("That was not a valid response", 1, 1)

    def viewInventory(self):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Inventory")
            self.disp.display("Contents %d / %d" %
                              (len(self.inv), self.getMaxInventorySlots()), 1)
            if len(self.inv) > 0:
                self.disp.display("")
                x = 0
                for item in self.inv:
                    x += 1
                    self.disp.display("     %d. %s" % (x, item.getName()), 0)
            self.disp.display("0. Exit")
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except ValueError:
                # TODO: Clean this up as it should (emphasis on should) no longer be needed
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display(
                    "That was not a valid response.", 1, 0)
                self.disp.closeDisplay()
                input()
                cmd = -1
            if not self.disp.window_is_open:
                self.quit = True
                return None
            self.disp.clearScreen()
            if 0 < cmd <= len(self.inv):
                self.attemptEquip(cmd)

    def attemptEquip(self, cmd):
        if self.inv[cmd-1].t == "w":
            equip = -1
            self.disp.displayHeader("Inspecting %s" % (self.inv[cmd-1].name))
            self.disp.display("Inspecting:")
            self.disp.display("\t%s - %s damage" %
                              (self.inv[cmd-1].name, self.inv[cmd-1].damage), 0)
            self.disp.display("\t" + self.inv[cmd-1].desc, 0)
            self.disp.display("Currently equipped:")
            self.disp.display("\t%s - %s damage" %
                              (self.weapon.name, self.weapon.damage), 0)
            self.disp.display("\t" + self.weapon.desc, 0, 1)
            self.disp.display("1. Equip", 0)
            self.disp.display("2. Drop", 0)
            self.disp.display("Anything else to continue", 0)
        elif self.inv[cmd-1].t == "a":
            self.disp.displayHeader("Equip %s" % (self.inv[cmd-1].getName()))
            self.disp.display("Inspecting: %s - %s defence" % (self.inv[cmd-1].name, self.inv[cmd-1].defence))
            self.disp.display("\tClass - %s" % (self.inv[cmd-1].armorWeight), 0, 0)
            self.disp.display("\tMin size - %s | Max Size - %s" % (self.inv[cmd-1].sizeMin, self.inv[cmd-1].sizeMax), 0, 0)
            self.disp.display("Currently equipped:")
            limbs = self.race.getLimbsOfLimbType(self.inv[cmd-1].limb, True)
            for limb in limbs:
                self.disp.display("\t%s - %s (%s defence)" % (limb.name, limb.armor.getName(), limb.armor.getDefenceRating()), 0)
            self.disp.display("1. Equip", 1)
            self.disp.display("2. Drop", 0)
            self.disp.display("Anything else to continue", 0)
        elif self.inv[cmd-1].t == "consumable":
            self.disp.displayHeader("Examining %s" % (self.inv[cmd-1].name))
            self.disp.display(self.inv[cmd-1].desc)
            self.disp.display("Worth: %d" % self.inv[cmd-1].worth, 1, 1)
            self.disp.display("1. {}".format(self.inv[cmd-1].consumeText), 0)
            self.disp.display("2. Drop", 0)
            self.disp.display("Anything else to continue", 0)
        else:
            self.disp.displayHeader("Examining %s" % (self.inv[cmd-1].name))
            self.disp.display(self.inv[cmd-1].desc)
            self.disp.display("Worth: %d" % self.inv[cmd-1].worth)
            self.disp.display("2. Drop")
            self.disp.display("Anything else to continue", 0)

        self.disp.closeDisplay()
        try:
            # equip = int(input())
            equip = self.disp.get_input(True, True, True)
        except:
            equip = -1
        self.disp.clearScreen()
        if self.inv[cmd-1].t == "w" and equip == 1:
            print(equip)
            self.inv.append(self.weapon)
            self.weapon = self.inv.pop(cmd-1)
        elif self.inv[cmd-1].t == "a" and equip == 1:
            armor = self.inv[cmd-1]
            if self.equipArmor(armor):
                self.inv.pop(cmd-1)
            '''
            self.inv.append(self.armor)
            self.armor = self.inv.pop(cmd-1)
            '''
        elif self.inv[cmd-1].t == "consumable" and equip == 1:
            self.inv[cmd-1].consumableEffect(self)
            self.inv.pop(cmd-1)
        elif equip == 2:
            self.disp.displayHeader("Item dropped")
            self.disp.display("You drop %s." % (self.inv.pop(cmd-1).name))
            self.disp.closeDisplay()
            # input("\nEnter to continue")
            self.disp.wait_for_enter()
            self.disp.clearScreen()
        
    def viewAttemptUnequipArmor(self, armor, limbs):
        self.disp.displayHeader("Unequip Armor")
        self.disp.display("All armor slots of that type are taken. Replace a piece of armor?", 1, 1)
        self.disp.display("Equipping: %s(%s defence)" % (armor, armor.getDefenceRating()), 0, 0)
        self.disp.display("Replace:")
        limbNum = 0
        for limb in limbs:
            limbNum += 1
            self.disp.display("\t%s. %s: %s(%s defence)" %(limbNum, limb.name, limb.armor, limb.armor.getDefenceRating()),0,0)
        self.disp.display("Anything else to cancel", 1)
        self.disp.closeDisplay()
        try:
            # equip = int(input())
            equip = self.disp.get_input(True, True, True)
        except:
            equip = -1
        status = False
        if equip > 0 and equip <= limbNum:
            self.inv.append(limbs[equip-1].armor)
            limbs[equip-1].armor = armor
            status = True
        self.disp.clearScreen()
        return status
    
    def viewPlayerDetails(self):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Details")
            self.disp.display("Player Stats:")
            self.disp.display(f'\tStrength     - {self.getStat("strength")}', 0)
            self.disp.display(f'\tVitality     - {self.getStat("vitality")}', 0)
            self.disp.display(f'\tPhysique     - {self.getStat("physique")}', 0)
            self.disp.display(f'\tIntelligence - {self.getStat("intelligence")}', 0)
            self.disp.display("Equipped Gear:", 1, 0)
            self.disp.display("\t{}".format(
                self.getEquipmentString()), 0)
            self.disp.display("Body:")
            self.disp.display(f'\t{self.getBodyDescription()}', 0)
            self.disp.closeDisplay()
            self.disp.display("0. Exit")
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except:
                cmd = -1
            if cmd == 0:
                pass
            elif not self.disp.window_is_open:
                self.quit = True
                return None
    
    def viewPlayerLevels(self):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Skills")
            self.disp.display("Player Skills:")

            # TODO finish displaying all player skill levels
            
            self.disp.closeDisplay()
            self.disp.display("0. Exit")
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except:
                cmd = -1
            if cmd == 0:
                pass
            elif not self.disp.window_is_open:
                self.quit = True
                return None

    def viewQuests(self, currentQuests, completedQuests):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Journal")
            self.disp.display("Quests:")
            questList = []
            for quest in currentQuests:
                if not quest.hidden:
                    questList.append(quest)
            if len(questList) > 0:
                for quest in questList:
                    self.disp.display("[ ] - {}".format(quest.title))
                    self.disp.display("\t{}".format(quest.desc), 0)
            else:
                self.disp.display("\tNo quests currently started", 0)

            questList = []
            for quest in completedQuests:
                if not quest.hidden:
                    questList.append(quest)
            if len(questList) > 0:
                # revereses the array so that the most recently completed quests
                # come up first
                for quest in questList:
                    self.disp.display("[X] - {}".format(quest.title))
                    self.disp.display("\t{}".format(quest.desc), 0)
            self.disp.display("0. Exit")
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except:
                cmd = -1
            if not self.disp.window_is_open:
                self.quit = True
                return None

    def confirmQuit(self):
        window = True
        while window:
            self.disp.clearScreen()
            self.disp.displayHeader("Quit Confirmation")
            self.disp.display("Are you sure you wish to quit?")
            self.disp.display("0. Yes, Quit")
            self.disp.display("1. No, Don't Quit", 0)
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except:
                cmd = -1
            if cmd == 0:
                self.quit = True
                window = False
            elif cmd == 1:
                self.quit = False
                window = False
            elif not self.disp.window_is_open:
                self.quit = True
                return None
            else:
                # TODO Incorrect input notification
                pass
    
    def giveXP(self, xp):
        ''' Gives the player the passed amount of experience. '''
        self.xp += xp
        if self.xp >= self.getXpNeededForLevelUp():
            self.xp -= self.getXpNeededForLevelUp()
            self.level += 1
    
    def giveHP(self, hp):
        ''' Gives the player HP '''
        self.hp += hp
        if self.hp > self.getMaxHP():
            self.hp = self.getMaxHP()
        
    def equipArmor(self, armor):
        limbs = self.race.getLimbsOfLimbType(armor.limb, True)
        equipped = False
        if len(limbs) > 0:
            for limb in limbs:
                if not equipped and limb.armor == None:
                    limb.armor = armor
                    equipped = True
            if not equipped:
                # Open menu to unequip armor from a limb
                equipped = self.viewAttemptUnequipArmor(armor, limbs)
        return equipped
    
    def equipArmorSet(self, armors):
        for armor in armors:
            equipped = False
            limbs = self.race.getLimbsOfLimbType(armor.limb)
            for limb in limbs:
                if not equipped and not limb.armor:
                    limb.armor = armor
                    equipped = True

    def setRace(self, race):
        # TODO check for equipped gear to make sure the player can still wield it
        self.race = race

    # Class Getters
    def getDodge(self):
        # TODO: Implement getDodge
        return 0

    def getEquipmentString(self):
        # TODO Refactor getEquipmentString
        equipstr = ""
        if self.weapon:
            equipstr += "You are wielding a {}. {} ".format(
                self.weapon, self.weapon.desc)
        else:
            equipstr += "You are wielding your fists as your weapon. "
        limbs = self.race.getLimbsEquippableLimbs()
        armors = []
        for limb in limbs:
            if limb.armor:
                armors.append(limb.armor)
        if len(armors) == 0:
            equipstr += "You are not wearing any kind of protective armor. "
        else:
            armorString = armors.pop(0).getName()
            while len(armors) > 1:
                armorString += ", %s" % armors.pop(0)
            if len(armors) == 1:
                armorString += ", and %s" % armors.pop(0)
            equipstr += "You are wearing {}.".format(armorString)
        return equipstr

    def getUserInfo(self):
        stats = []
        stats.append(("Level", self.level))
        stats.append(("Experience", f'{self.xp} / {self.getXpNeededForLevelUp()}'))
        stats.append(("Health", self.hp))
        stats.append(("Max Health", self.getMaxHP()))
        # stats.append(("Hurt Limbs", len(self.race.getHurtLimbs())))
        stats.append(("Gold", self.gold))
        return stats

    def getHealth(self):
        return int(((1.0*self.hp)/self.getMaxHP())*68 + 0.5)

    def getWeaponDamage(self):
        if self.weapon:
            return self.weapon.getAttack()
        else:
            return 0

    def getWeaponAction(self):
        if self.weapon:
            return self.weapon.getAction()
        else:
            return 0

    def getArmorDefence(self):
        armorTotal = 0
        for limb in self.race.getLimbsEquippableLimbs():
            if limb.armor:
                armorTotal += rollDice(limb.armor.getDefenceRating())
        if armorTotal > 0:
            self.disp.dprint("Player defended with {} armor".format(armorTotal))
        else: 
            armorTotal = 0
        return armorTotal
    
    def getStat(self, stat):
        baseStat = self.race.getStat(stat)
        bonusStat = self.stats[stat]
        # TODO Finish support for perks and for equipped gear
        # for perk in self.getPerks():
        #     if stat in perk
        return baseStat + bonusStat

    def getMaxHP(self):
        baseHealth = self.getStat("vitality") * 10
        bonusHealth = 0
        # TODO add supprot for perks to getMaxHP
        return baseHealth + bonusHealth

    def getMaxInventorySlots(self):
        baseSlots = self.getStat("strength") + int(self.getStat("physique"))
        bonusSlots = 0
        # TODO add support for perks to getMaxInventorySlots
        return baseSlots + bonusSlots
    
    def getBodyDescription(self):
        ''' Returns a description of the player's race. ''' 
        # TODO return a real class object
        return self.race.getDescription()
    
    def getXpNeededForLevelUp(self):
        # TODO improve required xp formula
        if self.level < 10:
            return 100 * self.level
        return ( self.level ** 2 ) * 10
    
    def getStartingArmor(self):
        return self.race.getStartingArmor()
    
    def getStartingWeapons(self):
        return self.race.getStartingWeapons()
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        self.name = name