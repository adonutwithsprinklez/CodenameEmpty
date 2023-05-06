from dieClass import rollDice


NPC_CONVERSATION_EQUIVALENTS = {
    "shopkeep":"Shop",
    "merchant":"Shop"
}


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
        self.flags = []
        self.dialogueFlags = []
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
                if limb.getArmor():
                    self.disp.display("\t%s - %s (%s defence)" % (limb.name, limb.getArmor(), limb.armor.getDefenceRating()),0)
                else:
                    self.disp.display("\t%s - Nothing" % (limb.name),0)
            #self.disp.display("\t- %s (%s defence)" % (self.armor, self.armor.defence))
            self.disp.closeDisplay()
            self.disp.displayAction("1. View Inventory", 1)
            self.disp.displayAction("2. View Quests", 2, 0)
            self.disp.displayAction("3. View Player Details", 3, 0)
            self.disp.displayAction("4. View Skill Levels", 4, 0)
            self.disp.displayAction("9. Quit Game", 9)
            self.disp.displayAction("0. Exit", 0, 0)
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
                    self.disp.displayAction("     %d. %s" % (x, item.getName()), x, 0)
            self.disp.displayAction("0. Exit", 0)
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
            self.disp.display("\t%s - %s damage" % (self.inv[cmd-1].name, self.inv[cmd-1].damage), 0)
            self.disp.display("\t" + self.inv[cmd-1].desc, 0)
            self.disp.display("Currently equipped:")
            self.disp.display("\t%s - %s damage" % (self.weapon.name, self.weapon.damage), 0)
            self.disp.display("\t" + self.weapon.desc, 0, 1)
            self.disp.displayAction("1. Equip", 1, 0)
            self.disp.displayAction("2. Drop", 2, 0)
            self.disp.displayAction("0. Back", 0, 0)
        elif self.inv[cmd-1].t == "a":
            self.disp.displayHeader("Equip %s" % (self.inv[cmd-1].getName()))
            self.disp.display("Inspecting: %s - %s defence" % (self.inv[cmd-1].name, self.inv[cmd-1].defence))
            self.disp.display("\tClass - %s" % (self.inv[cmd-1].armorWeight), 0, 0)
            self.disp.display("\tMin size - %s | Max Size - %s" % (self.inv[cmd-1].sizeMin, self.inv[cmd-1].sizeMax), 0, 0)
            self.disp.display("Currently equipped:")
            limbs = self.race.getLimbsOfLimbType(self.inv[cmd-1].limb, True)
            for limb in limbs:
                if limb.armor:
                    self.disp.display("\t%s - %s (%s defence)" % (limb.name, limb.armor.getName(), limb.armor.getDefenceRating()), 0)
                else:
                    self.disp.display("\t%s - None" % (limb.name), 0)
            self.disp.displayAction("1. Equip", 1, 1)
            self.disp.displayAction("2. Drop", 2, 0)
            self.disp.displayAction("0. Back", 0, 0)
        elif self.inv[cmd-1].t == "consumable":
            self.disp.displayHeader("Examining %s" % (self.inv[cmd-1].name))
            self.disp.display(self.inv[cmd-1].desc)
            self.disp.display("Worth: %d" % self.inv[cmd-1].worth, 1, 1)
            self.disp.displayAction("1. {}".format(self.inv[cmd-1].consumeText), 1, 0)
            self.disp.displayAction("2. Drop", 2, 0)
            self.disp.displayAction("0. Back", 0, 0)
        else:
            self.disp.displayHeader("Examining %s" % (self.inv[cmd-1].name))
            self.disp.display(self.inv[cmd-1].desc)
            self.disp.display("Worth: %d" % self.inv[cmd-1].worth)
            self.disp.displayAction("2. Drop", 2)
            self.disp.displayAction("0. Back", 0)

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
            self.disp.displayAction("\t%s. %s: %s(%s defence)" %(limbNum, limb.name, limb.armor, limb.armor.getDefenceRating()), limbNum, 0,0)
        self.disp.displayAction("0. Back", 0, 1)
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
            self.disp.display("\t{}".format(self.getEquipmentString()), 0)
            self.disp.display("Body:")
            self.disp.display(f'\t{self.getBodyDescription()}', 0)
            if len(self.getRace().getPerks()) > 0:
                self.disp.display(f'Racial Perks:')
                for perk in self.getRace().getPerks():
                    self.disp.display(f'\t{perk}', 0)
            self.disp.closeDisplay()
            self.disp.displayAction("0. Exit", 0)
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

            self.disp.displayAction("0. Exit", 0)
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
            self.disp.displayAction("0. Exit", 0)
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
            self.disp.displayAction("<red>0. Yes, Quit<red>", 0)
            self.disp.displayAction("<green>1. No, Don't Quit<green>", 1, 0)
            self.disp.closeDisplay()
            try:
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
        
    def converseNPC(self, npc, query):
        action = "greeting"
        conversing = True
        newDialogLine = True
        npcProfessions = npc.getProfessions()
        otherDialogueOptions = npc.getOtherDialogueOptions()
        while conversing:
            if newDialogLine:
                playerQuery = self.getPlayerQuery()
                fullQuery = {**query, **playerQuery}
                fullQuery["isAction"] = action
                npdDialogueLine = npc.getDialogueLine(fullQuery)
                if "addPlayerFlags" in npdDialogueLine.keys():
                    for flag in npdDialogueLine["addPlayerFlags"]:
                        if flag not in self.flags:
                            self.flags.append(flag)
                if "removePlayerFlags" in npdDialogueLine.keys():
                    for flag in npdDialogueLine["removePlayerFlags"]:
                        if flag in self.flags:
                            self.flags.remove(flag)
                dialogueLine = f"{npc.getName()} - {npdDialogueLine['dialogue']}"
                newDialogLine = False
            self.disp.clearScreen()
            self.disp.displayHeader(f"Conversing with {npc.getName()}")
            if fullQuery["isAction"] == "greeting":
                self.disp.display(f"You greet {npc.prefix}{npc.getName()}.")
            elif fullQuery["isAction"] == "finishShop":
                self.disp.display(f"You stop looking at {npc.prefix}{npc.getName()}'s goods.")
            elif fullQuery["isAction"] == "smalltalk":
                self.disp.display(f"You attempt to strike up some small talk with {npc.prefix}{npc.getName()}.")
            elif fullQuery["isAction"] == "goodbye":
                self.disp.display(f"You say farewell to {npc.prefix}{npc.getName()}.")
            else:
                actionId = fullQuery["isAction"]
                for dialogueOption in otherDialogueOptions:
                    if "isAction" in dialogueOption.keys() and actionId == dialogueOption["isAction"]:
                        self.disp.display(f"{dialogueOption['playerDialogue']}")
                        break
            self.disp.display(dialogueLine, 1, 1)
            self.disp.displayHeader("Conversation Choices")
            self.disp.displayAction("1. Small Talk", 1)
            i = 1
            npcProfessionCount = 0
            for profession in npcProfessions:
                if profession in NPC_CONVERSATION_EQUIVALENTS.keys():
                    i += 1
                    npcProfessionCount += 1
                    self.disp.displayAction(f"{i}. {NPC_CONVERSATION_EQUIVALENTS[profession]}", i, 0)
            for additionalOption in otherDialogueOptions:
                i += 1
                self.disp.displayAction(f"{i}. {additionalOption['option']}", i, 0)
            self.disp.displayAction("0. Goodbye", 0)
            self.disp.closeDisplay()
            cmd = self.disp.get_input(True, True, True)
            if cmd == 0:
                conversing = False
            elif cmd == 1:
                action = "smalltalk"
                newDialogLine = True
            elif 1 < cmd <= npcProfessionCount + 1:
                if npcProfessions[cmd-2] in NPC_CONVERSATION_EQUIVALENTS.keys():
                    conversationOption = NPC_CONVERSATION_EQUIVALENTS[npcProfessions[cmd-2]].lower()
                    if conversationOption == "shop":
                        query = self.shopMenu(npc, query)
                        action = "finishShop"
                        newDialogLine = True
            elif 1 + npcProfessionCount < cmd <= 1 + len(otherDialogueOptions) + npcProfessionCount:
                action = otherDialogueOptions[cmd-2-npcProfessionCount]["isAction"]
                newDialogLine = True
        
        # End conversation
        playerQuery = self.getPlayerQuery()
        fullQuery = {**query, **playerQuery}
        fullQuery["isAction"] = "goodbye"

        self.disp.clearScreen()
        self.disp.displayHeader(f"Conversing with {npc.getName()}")
        npdDialogueLine = npc.getDialogueLine(fullQuery)
        self.disp.display(f"{npc.getName()} - {npdDialogueLine['dialogue']}")
        if "addPlayerFlags" in npdDialogueLine.keys():
            for flag in npdDialogueLine["addPlayerFlags"]:
                if flag not in self.flags:
                    self.flags.append(flag)
        if "removePlayerFlags" in npdDialogueLine.keys():
            for flag in npdDialogueLine["removePlayerFlags"]:
                if flag in self.flags:
                    self.flags.remove(flag)
        self.disp.closeDisplay()
        self.disp.wait_for_enter()
    
    def shopMenu(self, npc, query):
        playerQuery = self.getPlayerQuery()
        fullQuery = {**query, **playerQuery}
        action = "shop"
        shopping = True
        while shopping:
            fullQuery["isAction"] = action
            self.disp.clearScreen()
            self.disp.displayHeader(f"{npc.getName()}'s Shop")
            if fullQuery["isAction"] == "shop":
                self.disp.display(f"You ask to see {npc.prefix}{npc.getName()}'s goods.")
            npdDialogueLine = npc.getDialogueLine(fullQuery)
            self.disp.display(f"{npc.getName()} - {npdDialogueLine['dialogue']}", 1, 1)
            if "addPlayerFlags" in npdDialogueLine.keys():
                for flag in npdDialogueLine["addPlayerFlags"]:
                    if flag not in self.flags:
                        self.flags.append(flag)
            if "removePlayerFlags" in npdDialogueLine.keys():
                for flag in npdDialogueLine["removePlayerFlags"]:
                    if flag in self.flags:
                        self.flags.remove(flag)
            self.disp.displayHeader("Your Info")
            self.disp.display(f"Gold: {self.gold}")
            self.disp.display(f"Inventory: {len(self.inv)} / {self.getMaxInventorySlots()}", 0, 1)
            self.disp.displayHeader(f"{npc.getName()}'s Inventory")
            i = 1
            for item in npc.getGeneratedInventory():
                i+=1
                if i == 2:
                    self.disp.displayAction(f"{i}. {item.getName(True)}", i, 1)
                else:
                    self.disp.displayAction(f"{i}. {item.getName(True)}", i, 0)
            self.disp.displayAction("1. Sell", 1, 1)
            self.disp.displayAction("0. Back", 0, 0)
            self.disp.closeDisplay()
            cmd = self.disp.get_input(True)
            if cmd == 0:
                shopping = False
            elif cmd == 1:
                if len(self.inv) > 0:
                    self.sellMenu(npc, query)
                    action = "finishSell"
                else:
                    action = "shopSellFail"
            elif 1 < cmd <= len(npc.getGeneratedInventory()) + 1:
                cost = npc.getGeneratedInventoryItemValue(cmd - 2)
                buy = self.itemInspectMenu(npc.getGeneratedInventoryItem(cmd - 2), cost)
                if buy:
                    if self.gold >= cost:
                        self.gold -= cost
                        self.inv.append(npc.popItemFromGeneratedInventory(cmd - 2))
                        action = "buyItem"
                    else:
                        action = "buyItemFail"
                else:
                    action = "buyItemCancel"
        return query
    
    def sellMenu(self, npc, query):
        playerQuery = self.getPlayerQuery()
        fullQuery = {**query, **playerQuery}
        action = "shopSell"
        shopping = True
        while shopping:
            fullQuery["isAction"] = action
            self.disp.clearScreen()
            self.disp.displayHeader(f"{npc.getName()}'s Shop")
            if fullQuery["isAction"] == "shop":
                self.disp.display(f"You ask to see {npc.prefix.capitalize()}{npc.getName()}'s goods.")
            npdDialogueLine = npc.getDialogueLine(fullQuery)
            self.disp.display(f"{npc.getName()} - {npdDialogueLine['dialogue']}", 1, 1)
            if "addPlayerFlags" in npdDialogueLine.keys():
                for flag in npdDialogueLine["addPlayerFlags"]:
                    if flag not in self.flags:
                        self.flags.append(flag)
            if "removePlayerFlags" in npdDialogueLine.keys():
                for flag in npdDialogueLine["removePlayerFlags"]:
                    if flag in self.flags:
                        self.flags.remove(flag)
            self.disp.displayHeader("Your Info")
            self.disp.display(f"Gold: {self.gold}", 1, 1)
            self.disp.displayHeader(f"Inventory: {len(self.inv)} / {self.getMaxInventorySlots()}")
            i = 0
            for item in self.inv:
                i += 1
                if i == 1:
                    self.disp.displayAction(f"{i}. {item.getName(True)}", i)
                else:
                    self.disp.displayAction(f"{i}. {item.getName(True)}", i, 0)
            self.disp.displayAction("0. Back", 0)
            self.disp.closeDisplay()
            cmd = self.disp.get_input(True)
            if cmd == 0:
                shopping = False
            elif 1 <= cmd <= len(self.inv):
                sell = self.itemInspectMenu(self.inv[cmd-1], self.inv[cmd-1].worth)
                if sell:
                    action = "sellItem"
                    item = self.inv.pop(cmd-1)
                    self.gold += item.worth
                    npc.addItemToInventory(item)
                else:
                    action = "sellItemCancel"


    def itemInspectMenu(self, item, worth):
        self.disp.clearScreen()
        self.disp.displayHeader(f"Purchasing {item.getName()}")
        self.disp.display(f"ITEM: {item.getName(True, False)}")
        self.disp.display(f"\t- {item.desc}", 0)
        self.disp.display(f"Worth: {worth}", 1, 1)
        if item.t == "a":
            pass
        elif item.t == "w":
            pass
        elif item.t == "consumable":
            pass
        else:
            pass
        self.disp.displayHeader("Your Info")
        self.disp.display(f"Gold: {self.gold}")
        self.disp.display(f"Inventory: {len(self.inv)} / {self.getMaxInventorySlots()}", 0, 1)
        self.disp.displayHeader(f"Options")
        self.disp.displayAction(f"1. Confirm", 1)
        self.disp.displayAction(f"0. Back", 1)
        self.disp.closeDisplay()
        cmd = self.disp.get_input(True, True, True)
        if cmd == 1:
            return True
        return False
    
    def getPlayerQuery(self):
        playerQuery = {
            "playerRace":self.race.getId(),
            "playerGold":self.gold,
            "playerLevel":self.level,
            "playerHealth":self.hp,
            "playerMaxHealth":self.getMaxHP(),
            "playerHealthPercentage":self.getHpPercentage(),
            "playerXP":self.xp,
            "playerXPNeededForLevelUp":self.getXpNeededForLevelUp(),
            "playerPerks":self.getPerks(),
            "playerDialogueFlags":self.dialogueFlags,
            "playerFlags":self.flags
        }
        print(playerQuery)
        return playerQuery
    
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
    
    def getHpPercentage(self):
        return int(((1.0*self.hp)/self.getMaxHP())*100)

    def getWeaponDamage(self):
        if self.weapon:
            return self.weapon.getAttack()
        else:
            # TODO: Get racial stuff
            return 0

    def getWeaponAction(self):
        if self.weapon:
            return self.weapon.getAction()
        else:
            # TODO: Get racial stuff
            return ""

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
    
    def getPerks(self):
        perks = self.perks[::]
        perks.extend(self.getRace().getPerks())
        perks = list(set(perks))
        return perks

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
    
    def getStartingInventory(self):
        return self.race.getStartingInventory()
    
    def getRace(self):
        return self.race
    
    def getName(self):
        return self.name
    
    def setName(self, name):
        # Make sure first letter is capitalized before setting name
        name = name.capitalize()
        self.name = name