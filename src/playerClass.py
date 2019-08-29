import random


from dieClass import rollDice
from weaponClass import Weapon


class Player(object):
    def __init__(self):
        self.name = "Player name"
        self.hp = 50
        self.level = 1
        self.xp = 0
        self.hpMax = self.hp
        self.weapon = None
        self.armor = None
        self.unarmed = 1
        self.gold = 0
        self.inv = []
        self.maxInv = 10
        self.disp = None

    def viewInventory(self):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Inventory")
            self.disp.display("Contents %d / %d" %
                              (len(self.inv), self.maxInv), 1)
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
                cmd = int(input())
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
            self.disp.display("%s - %s damage" %
                              (self.inv[cmd-1].name, self.inv[cmd-1].damage), 0)
            self.disp.display(self.inv[cmd-1].desc, 0)
            self.disp.display("Currently equipped:")
            self.disp.display("%s - %s damage" %
                              (self.weapon.name, self.weapon.damage), 0)
            self.disp.display(self.weapon.desc, 0, 1)
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
            self.disp.display("2. Drop", 0)
            self.disp.display("Anything else to continue", 0)

        self.disp.closeDisplay()
        try:
            equip = int(input())
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
            input("\nEnter to continue")
            self.disp.clearScreen()
    
    def playerMenu(self, currentQuests, completedQuests):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("{} Info".format(self.name))
            self.disp.display("Stats:")
            for stat in self.getStats():
                self.disp.display(
                    "\t{} - {}".format(stat[0], stat[1]), 0, 0)
            self.disp.display("Currently Equipped:", 1, 0)
            self.disp.display("\t{}".format(
                self.getEquipmentString()), 0)
            self.disp.display("1. View Inventory")
            self.disp.display("2. View Quests",0)
            self.disp.display("0. Exit", 0)
            self.disp.closeDisplay()
            try:
                cmd = int(input())
            except:
                cmd = -1
            if cmd == 0:
                pass
            elif cmd == 1:
                self.viewInventory()
            elif cmd == 2:
                self.viewQuests(currentQuests, completedQuests)
            else:
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display("That was not a valid response",1,1)
            
    
    def viewQuests(self, currentQuests, completedQuests):
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Journal")
            self.disp.display("Current Quests:")
            if len(currentQuests) > 0:
                for quest in currentQuests:
                    self.disp.display("\t{} - {}".format(quest.title, quest.desc),0)
            else:
                self.disp.display("\tNo quests currently started",0)
            if len(completedQuests) > 0:
                self.disp.display("Completed Quests:")
                for quest in completedQuests:
                    self.disp.display("\t{}-{}".format(quest.title,quest.desc),0)
            self.disp.display("0. Exit")
            self.disp.closeDisplay()
            try:
                cmd = int(input())
            except:
                cmd = -1

    def getEquipmentString(self):
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

    def getStats(self):
        stats = []
        stats.append(("Health", self.hp))
        stats.append(("Max Health", self.hpMax))
        return stats

    def getHealth(self):
        return int(((1.0*self.hp)/self.hpMax)*68 + 0.5)

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
