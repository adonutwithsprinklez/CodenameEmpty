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
        self.weapon = []
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
                    self.disp.display("     %d. %s" %
                                      (x, item.name), 0)
            self.disp.display("0. Exit")
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except ValueError:
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display(
                    "That was not a valid response.", 1, 0)
                self.disp.closeDisplay()
                input()
                cmd = -1
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
            self.disp.displayHeader("Equip %s" % (self.inv[cmd-1].name))
            self.disp.display("%s - %d defence" %
                              (self.inv[cmd-1].name, self.inv[cmd-1].defence))
            self.disp.display(self.inv[cmd-1].desc, 0)
            self.disp.display("Currently equipped:")
            self.disp.display("%s - %d defence" %
                              (self.armor.name, self.armor.defence), 0)
            self.disp.display(self.armor.desc, 0, 1)
            self.disp.display("1. Equip", 0)
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
            equip = self.disp.get_input(True)
        except:
            equip = -1
        self.disp.clearScreen()
        if self.inv[cmd-1].t == "w" and equip == 1 or self.inv[cmd-1].t == "a" and equip == 1:
            print(equip)
            try:
                self.inv.append(self.weapon)
                self.weapon = self.inv.pop(cmd-1)
            except:
                self.inv.append(self.armor)
                self.armor = self.inv.pop(cmd-1)
        elif equip == 2:
            self.disp.displayHeader("Item dropped")
            self.disp.display("You drop %s." % (self.inv.pop(cmd-1).name))
            self.disp.closeDisplay()
            # input("\nEnter to continue")
            self.disp.get_input()
            self.disp.clearScreen()

    def playerMenu(self, currentQuests, completedQuests):
        cmd = -1
        while cmd != 0 and not self.quit:
            self.disp.clearScreen()
            self.disp.displayHeader("{} Info ( {} )".format(self.name, self.race.name))
            self.disp.display("Quick Stats:")
            for stat in self.getUserInfo():
                self.disp.display(f'{stat[1]:>15} - {stat[0]}', 0)
            self.disp.display("Equipped Gear:", 1, 0)
            self.disp.display("\t{}".format(
                self.getEquipmentString()), 0)
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
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display("That was not a valid response", 1, 1)
    
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

    def viewQuests(self, currentQuests, completedQuests):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Journal")
            self.disp.display("Quests:")
            if len(currentQuests) > 0:
                for quest in currentQuests:
                    self.disp.display("[ ] - {}".format(quest.title))
                    self.disp.display("\t{}".format(quest.desc), 0)
            else:
                self.disp.display("\tNo quests currently started", 0)
            if len(completedQuests) > 0:
                # revereses the array so that the most recently completed quests
                # come up first
                for quest in completedQuests:
                    self.disp.display("[X] - {}".format(quest.title))
                    self.disp.display("\t{}".format(quest.desc), 0)
            self.disp.display("0. Exit")
            self.disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = self.disp.get_input(True)
            except:
                cmd = -1

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
            else:
                # TODO Incorrect input notification
                pass

    def setRace(self, race):
        # TODO check for equipped gear to make sure the player can still wield it
        self.race = race
    
    def giveXP(self, xp):
        ''' Gives the player the passed amount of experience. '''
        self.xp += xp
        if self.xp >= self.getXpNeededForLevelUp():
            self.xp -= self.getXpNeededForLevelUp()
            self.level += 1

    # Class Getters
    def getEquipmentString(self):
        # TODO redo this whole part
        equipstr = ""
        if self.weapon:
            equipstr += "You are wielding a {}. {} ".format(
                self.weapon, self.weapon.desc)
        else:
            equipstr += "You are wielding your fists as your weapon. "
        if self.armor:
            equipstr += "You are wearing {}. {} ".format(
                self.armor, self.armor.desc)
        else:
            equipstr += "You are not wearing any kind of protective armor. "
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
            return rollDice(self.weapon.damage)
        else:
            return 0

    def getWeaponAction(self):
        if self.weapon:
            return self.weapon.getAction()
        else:
            return 0

    def getArmorDefence(self):
        if self.armor:
            armor = rollDice(self.armor.defence)
            self.disp.dprint("Player defended with {} armor".format(armor))
            return armor
        else:
            return 0
    
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
        # TODO add supprot for perks
        return baseHealth + bonusHealth

    def getMaxInventorySlots(self):
        baseSlots = self.getStat("strength") + int(self.getStat("physique"))
        bonusSlots = 0
        # TODO add support for perks
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