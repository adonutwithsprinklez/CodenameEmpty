
from armorClass import Armor
from ApplicationWindowClass import ApplicationWindow
from dieClass import rollDice
from raceClass import Race
from weaponClass import Weapon


NPC_CONVERSATION_EQUIVALENTS = {
    "shopkeep":"Shop",
    "merchant":"Shop",
    "healer":"Heal",
    "doctor":"Heal"
}


class Player(object):
    def __init__(self):
        """
        Initializes a new instance of the Player class.
        """
        self.name:str = "Player"
        self.hp:int = 50
        self.energy:int = 50
        self.level:int = 1
        self.xp:int = 0
        self.race:Race = None
        self.perks:list = []
        self.weapon:Weapon = None
        self.armor:Armor = None
        self.unarmed:int = 1
        self.gold:int = 0
        self.inv:list = []
        self.disp:ApplicationWindow = None
        self.quit:bool = False
        self.tags:list = []
        self.skills:list = []
        self.flags:list = []
        self.dialogueFlags:list = []
        self.stats:dict[str, int] = {
            "strength": 0,
            "vitality": 0,
            "physique": 0,
            "intelligence": 0
        }

    def playerMenu(self, currentQuests, completedQuests):
        """
        Displays the player menu and handles user input for various actions.

        Parameters:
        - currentQuests (list): A list of current quests.
        - completedQuests (list): A list of completed quests.

        Returns:
        - None
        """
        cmd = -1
        while cmd != 0 and not self.quit:
            self.disp.clearScreen()
            self.disp.displayHeader(f"Player Info: <cyan>{self.name}<cyan>")
            self.disp.display("<h2>Quick Stats:<h2>")
            for stat in self.getUserInfo():
                self.disp.display(f'{stat[1]:>15} - {stat[0]}', 0)
            self.disp.display("<h2>Wielding:<h2>")
            if self.weapon != None:
                self.disp.display("\t<i>%s<i> (%s damage)" % (self.weapon.name, self.weapon.damage),0)
            else:
                self.disp.display("\tYou are not currently wielding a weapon",0)
            self.disp.display("<h2>Wearing:<h2>")
            for limb in self.race.getLimbsEquippableLimbs():
                if limb.getArmor():
                    self.disp.display("\t%s - <i>%s<i> (%s defence)" % (limb.name, limb.getArmor(), limb.armor.getDefenceRating()),0)
                else:
                    self.disp.display("\t%s - Nothing" % (limb.name),0)
            #self.disp.display("\t- %s (%s defence)" % (self.armor, self.armor.defence))
            self.disp.closeDisplay()
            self.disp.displayAction("1. View Inventory", 1, 0)
            self.disp.displayAction("2. [<red>DISABLED<red>] View Equipment", 2, 0)
            self.disp.displayAction("3. View Quests", 3, 0)
            self.disp.displayAction("4. View Player Details", 4, 0)
            self.disp.displayAction("5. View Skill Levels", 5, 0)
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
            elif cmd == 3:
                self.viewQuests(currentQuests, completedQuests)
            elif cmd == 4:
                self.viewPlayerDetails()
            elif cmd == 5:
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
        """
        This method presents the player's inventory on the screen and provides options for interacting with the items.
        The inventory contents are displayed along with the total number of items and the maximum number of inventory slots.
        The player can choose to exit the inventory or select a specific item to equip.

        Returns:
            None
        """
        cmd = -1
        while cmd != 0:
            self.disp.clearScreen()
            self.disp.displayHeader("Inventory")
            self.disp.display("Contents %d / %d" % (len(self.inv), self.getMaxInventorySlots()), 1, 1)
            if len(self.inv) > 0:
                x = 0
                for item in self.inv:
                    x += 1
                    self.disp.displayAction("     %d. %s" % (x, item.getName()), x, 0)
            self.disp.displayAction("0. Exit", 0)
            self.disp.closeDisplay()
            try:
                cmd = self.disp.get_input(True)
            except ValueError:
                self.disp.clearScreen()
                self.disp.displayHeader("Error")
                self.disp.display("That was not a valid response.", 1, 0)
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
        """
        Attempts to equip an item from the player's inventory based on the given command.

        Args:
            cmd (int): The index of the item to equip.

        Returns:
            None
        """
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
        """
        Displays the unequip armor menu and allows the player to replace a piece of armor.

        Args:
            armor (Armor): The armor to be equipped.
            limbs (list): The list of limbs to choose from.

        Returns:
            bool: True if the armor was successfully replaced, False otherwise.
        """
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
        """
        Displays the player's skill levels and allows the user to exit the view.

        Returns:
            None
        """
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
        """
        Displays the player's quests in the journal.

        Args:
            currentQuests (list): A list of current quests.
            completedQuests (list): A list of completed quests.

        Returns:
            None
        """
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
        """
        Displays a quit confirmation window and handles user input.

        Returns:
            None
        """
        window = True
        while window:
            self.disp.clearScreen()
            self.disp.displayHeader("Quit Confirmation")
            self.disp.display("Are you sure you wish to quit?")
            self.disp.displayAction("<green>1. No, Don't Quit<green>", 1)
            self.disp.displayAction("<red>0. Yes, Quit<red>", 0)
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
        """
        Perform a conversation with an NPC.

        Args:
            npc (NPC): The NPC to converse with.
            query (dict): The query parameters for the conversation.

        Returns:
            None
        """
        action = "greeting"
        conversing = True
        newDialogLine = True
        npcProfessions = npc.getProfessions()
        itemsGiven = []
        itemsTaken = []

        while conversing:
            if newDialogLine:
                itemsGiven = []
                itemsTaken = []
                playerQuery = self.getPlayerQuery()
                fullQuery = {**query, **playerQuery}
                fullQuery["isAction"] = action
                npcDialogueLine = npc.getDialogueLine(fullQuery)

                if "addPlayerFlags" in npcDialogueLine.keys():
                    for flag in npcDialogueLine["addPlayerFlags"]:
                        if flag not in self.flags:
                            self.flags.append(flag)

                if "removePlayerFlags" in npcDialogueLine.keys():
                    for flag in npcDialogueLine["removePlayerFlags"]:
                        if flag in self.flags:
                            self.flags.remove(flag)

                if "givePlayerItems" in npcDialogueLine.keys():
                    for item in npcDialogueLine["givePlayerItems"]:
                        if item[0] == "gold":
                            gold = rollDice(item[1])
                            self.gold += gold
                            itemsGiven.append(f"{gold} gold")
                        else:
                            # TODO: generate item and give to player
                            pass

                    if "takePlayerItems" in npcDialogueLine.keys():
                        for item in npcDialogueLine["takePlayerItems"]:
                            if item[0] == "gold":
                                gold = rollDice(item[1])
                                self.gold -= gold
                                itemsTaken.append(f"{gold} gold")
                            else:
                                # TODO: take item from player
                                pass

                dialogueLine = f"{npc.getName()} - {npcDialogueLine['dialogue']}"
                playerQuery = self.getPlayerQuery()
                fullQuery = {**query, **playerQuery}
                fullQuery["isAction"] = action
                otherDialogueOptions = npc.getOtherDialogueOptions(fullQuery)
                newDialogLine = False

                self.disp.clearScreen()
                self.disp.displayHeader(f"Conversing with {npc.getName()}")

                for item in itemsGiven:
                    self.disp.display(f"<green>You receive {item}<green>")

                for item in itemsTaken:
                    self.disp.display(f"<red>You lose {item}<red>")

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
                        if conversationOption == "heal":
                            action = self.healMenu(npc, query)
                            newDialogLine = True
            elif 1 + npcProfessionCount < cmd <= 1 + len(otherDialogueOptions) + npcProfessionCount:
                action = otherDialogueOptions[cmd-2-npcProfessionCount]["isAction"]
                if "npcFlagActions" in otherDialogueOptions[cmd-2-npcProfessionCount].keys():
                    for flagAction in otherDialogueOptions[cmd-2-npcProfessionCount]["npcFlagActions"]:
                        npc.modifyDialogueFlag(flagAction)
                newDialogLine = True

        # End conversation
        playerQuery = self.getPlayerQuery()
        fullQuery = {**query, **playerQuery}
        fullQuery["isAction"] = "goodbye"

        self.disp.clearScreen()
        self.disp.displayHeader(f"Conversing with {npc.getName()}")
        npcDialogueLine = npc.getDialogueLine(fullQuery)
        self.disp.display(f"{npc.getName()} - {npcDialogueLine['dialogue']}")

        if "addPlayerFlags" in npcDialogueLine.keys():
            for flag in npcDialogueLine["addPlayerFlags"]:
                if flag not in self.flags:
                    self.flags.append(flag)

        if "removePlayerFlags" in npcDialogueLine.keys():
            for flag in npcDialogueLine["removePlayerFlags"]:
                if flag in self.flags:
                    self.flags.remove(flag)

        if "givePlayerItems" in npcDialogueLine.keys():
            print(npcDialogueLine["givePlayerItems"])
            for item in npcDialogueLine["givePlayerItems"]:
                if item[0] == "gold":
                    gold = rollDice(item[1])
                    self.gold -= gold
                    self.disp.display(f"You receive {gold} gold.")
                else:
                    # TODO: generate item and give to player
                    pass

        if "takePlayerItems" in npcDialogueLine.keys():
            for item in npcDialogueLine["takePlayerItems"]:
                if item[0] == "gold":
                    gold = rollDice(item[1])
                    self.gold -= gold
                    self.disp.display(f"You lose {gold} gold.")
                else:
                    # TODO: take item from player
                    pass

        self.disp.closeDisplay()
        self.disp.wait_for_enter()
    
    def shopMenu(self, npc, query):
        """
        Displays the shop menu and handles player interactions with the shop.

        Args:
            npc (NPC): The NPC object representing the shopkeeper.
            query (dict): The query parameters for the shop menu.

        Returns:
            dict: The updated query parameters after the player finishes interacting with the shop.
        """
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
        """
        Displays the sell menu for the player.

        Parameters:
        - npc: The NPC object representing the shopkeeper.
        - query: Additional query parameters.

        Returns:
        None
        """
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
    
    def healMenu(self, npc, query):
        """
        Displays the healing menu and allows the player to heal themselves.

        Args:
            npc (str): The NPC providing the healing services.
            query (str): The query or request from the player.

        Returns:

        """
        self.disp.clearScreen()
        self.disp.displayHeader(f"Healing with {npc.getName()}")

        # Display available healing options
        self.disp.displayHeader("Your Info")
        self.disp.display(f"Gold: {self.gold}")
        self.disp.display(f"Inventory: {len(self.inv)} / {self.getMaxInventorySlots()}", 0, 1)
        #TODO fix the math behind how much healing costs
        self.disp.displayAction(f"1. Heal full health ({self.getMaxHP()//2} gold)", 1)
        self.disp.displayAction(f"2. Heal half health ({self.getMaxHP()//4} gold)", 2, 0)
        # self.disp.displayAction(f"[<red>DISABLED<red>]3. Heal specific body part", 3)
        self.disp.displayAction("0. Back", 0)
        self.disp.closeDisplay()
        cmd = self.disp.get_input(True, True, True)
        if cmd == 1:
            # Perform full healing
            self.giveHP(self.getMaxHP())
            return "healFull"
        elif cmd == 2:
            # Perform partial healing
            self.giveHP(self.getMaxHP() // 2)
            return "healPart"
        elif cmd == 3:
            # Perform healing for specific body part
            # Implement your logic here
            return "healPart"
        elif cmd == 0:
            # Go back
            return "healCancel"

    def itemInspectMenu(self, item, worth):
        """
        Displays the item inspection menu and allows the player to purchase the item.

        Args:
            item (Item): The item to be inspected and potentially purchased.
            worth (int): The worth or value of the item.

        Returns:
            bool: True if the player confirms the purchase, False otherwise.
        """
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
        self.disp.displayAction(f"0. Back", 0)
        self.disp.closeDisplay()
        cmd = self.disp.get_input(True, True, True)
        if cmd == 1:
            return True
        return False
    
    def getPlayerQuery(self):
        """
        Returns a dictionary containing various attributes of the player.

        Returns:
            dict: A dictionary containing the following player attributes:
                - playerRace: The ID of the player's race.
                - playerGold: The amount of gold the player has.
                - playerLevel: The player's level.
                - playerHealth: The player's current health.
                - playerMaxHealth: The player's maximum health.
                - playerHealthPercent: The player's health percentage.
                - playerXP: The player's experience points.
                - playerXPNeededForLevelUp: The amount of experience points needed for the player to level up.
                - playerPerks: The player's perks.
                - playerDialogueFlags: The player's dialogue flags.
                - playerFlags: The player's flags.
        """
        playerQuery = {
            "playerRace": self.race.getId(),
            "playerGold": self.gold,
            "playerLevel": self.level,
            "playerHealth": self.hp,
            "playerMaxHealth": self.getMaxHP(),
            "playerHealthPercent": self.getHpPercentage(),
            "playerXP": self.xp,
            "playerXPNeededForLevelUp": self.getXpNeededForLevelUp(),
            "playerPerks": self.getPerks(),
            "playerDialogueFlags": self.dialogueFlags,
            "playerFlags": self.flags
        }
        return playerQuery
    
    def giveXP(self, xp):
        """
        Gives the player the specified amount of experience.

        Args:
            xp (int): The amount of experience to give to the player.
        """
        self.xp += xp
        if self.xp >= self.getXpNeededForLevelUp():
            self.xp -= self.getXpNeededForLevelUp()
            self.level += 1
    
    def giveHP(self, hp):
        """
        Increases the player's HP by the specified amount.

        Args:
            hp (int): The amount of HP to add.

        Returns:
            None
        """
        self.hp += hp
        if self.hp > self.getMaxHP():
            self.hp = self.getMaxHP()
        
    def equipArmor(self, armor):
        """
        Equips the specified armor to the player's limbs.

        Args:
            armor (Armor): The armor to be equipped.

        Returns:
            bool: True if the armor was successfully equipped, False otherwise.
        """
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
        """
        Equips a set of armor to the player's limbs.

        Args:
            armors (list): List of armor objects to be equipped.

        Returns:
            None
        """
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
        """
        Returns a string describing the player's equipment.

        Returns:
            str: A string describing the player's equipment.
        """
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
            """
            Returns the player's information as a list of tuples.
            
            Each tuple contains a stat name and its corresponding value.
            
            Returns:
                list: A list of tuples representing the player's information.
            """
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
    
    def getAttackOptions(self):
        """
        Returns a list of attack options available to the player.

        The attack options include the attack information from the player's equipped weapon,
        as well as any limb attacks available based on the player's race.

        Returns:
            list: A list of attack options.
        """
        attackOptions = []
        if self.weapon:
            attackOptions.append(self.weapon.getAttackInfo())
        for option in self.race.getAllLimbAttacks():
            attackOptions.append(option)
        return attackOptions

    def getWeaponDamage(self, i=0):
        """
        Calculates the total damage inflicted by the player's weapon attack.

        Parameters:
        - i (int): Index of the attack option to use. Default is 0.

        Returns:
        - totalDamage (int): Total damage inflicted by the weapon attack.
        """
        totalDamage = 0
        actions = self.getAttackOptions()
        if self.weapon and i == 0:
            totalDamage += self.getStat("strength")
            totalDamage += self.weapon.getAttack()
        else:
            unarmedMultiplier = 1
            totalDamage = rollDice(actions[i][3])
            if "Unarmed Fighter" in self.getPerks():
                unarmedMultiplier += 1
            totalDamage += unarmedMultiplier * self.getStat("strength")
        return totalDamage

    def getWeaponAction(self, i=0):
        """
        Returns the action associated with the player's weapon.

        Parameters:
            i (int): Index of the attack option to retrieve (default is 0).

        Returns:
            str: The action associated with the player's weapon, or the special racial stuff if available.
        """
        if self.weapon and i == 0:
            return self.weapon.getAction()
        else:
            # TODO: Get special racial stuff
            return self.getAttackOptions()[i][2]

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
    
    def getHp(self):
        return self.hp

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