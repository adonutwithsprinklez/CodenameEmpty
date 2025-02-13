

from random import choice

from eventClass import Event
from gameDataHandler import GameDataHandler
from miscFunctions import fireEvent
from textGeneration import generateStringWithVariables, replaceVariablesInString
from universalFunctions import getDataValue, evaluate_rule


class QuestStepCondition(object):
    ''' Just a simple data holder for information quest steps '''
    def __init__(self, condition, query=None):
        if not query:
            query = {}
        
        self.flag = condition[0]
        self.check = condition[1]
        self.value = condition[2]
        self.recheck = False

        # check there is a 4th value
        # if there is a 4th value check if it is + or -
        # if it is +, add the value to the query value (if it exists)
        # if it is -, subtract the value from the query value (if it exists)
        if len(condition) > 3:
            for con in condition[3:]:
                if con == "+":
                    if self.flag in query.keys():
                        self.value += query[self.flag]
                elif con == "-":
                    if self.flag in query.keys():
                        self.value = query[self.flag] - self.value
                    else:
                        self.value = 0 - self.value
                elif con == "recheck":
                    # This condition will recheck the condition every tick
                    # Meaning any step that has this condition will only evaluate
                    # to true if all other conditions are met and this one is met
                    # at that specific tick
                    self.recheck = True

        self.fulfilled = False
    
    def check_condition(self, query=None)->bool:
        ''' Returns True if fulfilled '''
        if (self.fulfilled or not query) and not self.recheck:
            return self.fulfilled
        return self._check_fulfilled(query)
    
    def _check_fulfilled(self, query)->bool:
        if self.flag is None:
            return False
        elif self.flag in query.keys():
            self.fulfilled = evaluate_rule(self.value, self.check, query[self.flag])
            return self.fulfilled
        if self.recheck:
            self.fulfilled = False
        return self.fulfilled
    
    def __str__(self):
        return f"{self.flag} {self.check} {self.value} - {self.fulfilled}"


class QuestStep(object):
    def __init__(self, stepData, query=None):
        checks = getDataValue("checks", stepData, {})
        self.checks:dict = {}
        for check in checks.keys():
            self.checks[check] = []
            for condition in checks[check]:
                self.checks[check].append(QuestStepCondition(condition, query))
        self.reactions:dict = getDataValue("reactions", stepData, {})
        self.setDesc:str = getDataValue("setDesc", stepData, None)

        self.response:str = None
    
    def check_conditions(self, query=None)->bool:
        for condition in self.checks:
            for c in self.checks[condition]:
                c.check_condition(query)
        # See if any of the possible checks are fulfilled
        # Set response to the first one that has a fulfilled condition
        for condition in self.checks.keys():
            success = all([c.fulfilled for c in self.checks[condition]])
            if success:
                self.response = condition
                return True
        return False


class Quest(object):
    ''' The Quest class will be the base class for all quests. It will have
    the basic information that all quests will need. '''
    quest_number:int = 0
    def __init__(self, questId, query=None):
        self.quest_number = 1 + Quest.quest_number
        Quest.quest_number += 1
        self.id:str = questId # Used to identify the quest
        # Quest uuid is used to identify the specific instance of the quest,
        # in case it is repeatable. It is able to be retrieved using
        # get_quest_uuid()
        
        quest_data = GameDataHandler().getGameData("quest", self.id)

        # Generate any random variables that are needed
        # print(f"\tGenerating Quest '{self.id}'")
        randomVariables = getDataValue("randomVariables", quest_data, {})
        self.customVariables = {}
        for var in randomVariables.keys():
            newVar = generateStringWithVariables(randomVariables[var], "value")
            self.customVariables[var] = newVar
            # print(f"\t\tVariable '{var}': '{newVar}'")

        self.title = getDataValue("title", quest_data, "Quest")
        self.title = replaceVariablesInString(self.title, self.customVariables)
        # print(f"\t\tTitle: {self.title}")
        self.desc = getDataValue("desc", quest_data, "No description available.")
        self.desc = replaceVariablesInString(self.desc, self.customVariables)
        # print(f"\t\tDescription: {self.desc}")
        self.hidden = getDataValue("hidden", quest_data, False)


        self.enabled = getDataValue("enabledByDefault", quest_data, False)
        self.started = False
        self.completed = False
        self.failed = False

        self.repeatable = getDataValue("repeatable", quest_data, False)

        self.spawnConditions = []
        sc = getDataValue("spawnConditions", quest_data, [])
        for condition in sc:
            self.spawnConditions.append(QuestStepCondition(condition, query))
        self.do:str = getDataValue("do", quest_data, None)

        self.currentStep = choice(getDataValue("initialStep", quest_data, []))
        self.step = QuestStep(getDataValue(self.currentStep, quest_data, {}), query)
    
    def check_spawn_conditions(self, query=None)->bool:
        for condition in self.spawnConditions:
            condition.check_condition(query)
        if all([condition.fulfilled for condition in self.spawnConditions]):
            # Reset the current step
            self.step = QuestStep(getDataValue(self.currentStep, GameDataHandler().getGameData("quest", self.id), {}), query)
            self.started = True
            if self.step.setDesc:
                self.desc = self.step.setDesc
            return True
        return False
    
    def check_step_conditions(self, query=None)->bool:
        self.step.check_conditions(query)
        if self.step.response:
            return True
        return False
    
    def get_current_step(self)->str:
        if not self.enabled:
            return None
        return self.currentStep

    def get_quest_number(self)->int:
        return self.quest_number
    
    def get_enabled(self)->bool:
        return self.enabled
    
    def get_repeatable(self)->bool:
        return self.repeatable
    
    def get_id(self)->str:
        return self.id
    
    def get_quest_uuid(self)->str:
        return f"{self.get_id()}_{self.get_quest_number()}"
    
    def get_started(self)->bool:
        return self.started
    
    def get_completed(self)->bool:
        return self.completed
    
    def get_failed(self)->bool:
        return self.failed
    
    def get_success(self)->bool:
        return self.get_completed() and not self.get_failed()



class QuestWrangler(object):
    ''' A master class that will handle which quests are active and
    which are not. It will also handle the quest log and all the other
    quest-related things. '''

    quest_list = []

    # Actual quest objects
    enabled_quests = {}
    active_quests = {}
    completed_quests = {}

    game_data = None
    debug = False

    def __init__(self, refresh=False, DEBUG=None):
        if DEBUG is not None:
            QuestWrangler.debug = DEBUG
        if refresh:
            QuestWrangler.quest_list = []
            QuestWrangler.enabled_quests = {}
            QuestWrangler.active_quests = {}
            QuestWrangler.completed_quests = {}

            QuestWrangler.game_data = GameDataHandler()

            for quest in QuestWrangler.game_data.getListOfKeys("quest"):
                self.enable_quest(quest, False)

            self.print_quest_lists(override=False)

    def get_quest_by_id(self, quest_id):
        for quest in QuestWrangler.quest_list:
            if quest == quest_id:
                return quest
        # check the enabled quests
        if quest_id in QuestWrangler.enabled_quests.keys():
            return QuestWrangler.enabled_quests[quest_id]
        # check the active quests
        if quest_id in QuestWrangler.active_quests.keys():
            return QuestWrangler.active_quests[quest_id]
        # check the completed quests
        if quest_id in QuestWrangler.completed_quests.keys():
            return QuestWrangler.completed_quests[quest_id]
        return None
    
    def get_active_quests(self):
        return QuestWrangler.active_quests
    
    def get_completed_quests(self):
        return QuestWrangler.completed_quests
    
    def enable_quest(self, quest_id, force=False):
        # Load the quest data into the quest list an initial time
        newQuest = Quest(quest_id)
        if force:
            if quest_id in QuestWrangler.quest_list:
                QuestWrangler.quest_list.remove(quest_id)
            newQuest.enabled = True

        if not newQuest.get_enabled():
            # Add the quest id to the list
            QuestWrangler.quest_list.append(quest_id)
        else:
            # Otherwise, add the quest to the enabled quests
            QuestWrangler.enabled_quests[quest_id] = newQuest
            # Check if the quest is repeatable and add the id back to possible quests
            if newQuest.get_repeatable():
                QuestWrangler.quest_list.append(quest_id)
    
    def tick(self, player, query=None, areaController=None):

        enable_quests = []

        if query:
            # Check for enabled quests that meet the spawn conditions
            removed = []
            for quest in QuestWrangler.enabled_quests:
                if QuestWrangler.enabled_quests[quest].check_spawn_conditions(query):
                    QuestWrangler.active_quests[quest] = QuestWrangler.enabled_quests[quest]
                    # fire the quest start event (if it exists)
                    if QuestWrangler.active_quests[quest].do:
                        event = Event(QuestWrangler.active_quests[quest].do)
                        fireEvent(event, player, self, areaController)
                    removed.append(quest)
            for quest in removed:
                del QuestWrangler.enabled_quests[quest]

            # Tick all active quests
            removed = []
            for quest in QuestWrangler.active_quests:
                if QuestWrangler.active_quests[quest].check_step_conditions(query):
                    # The quest step has been completed
                    # Fire the step's response
                    q = QuestWrangler.active_quests[quest]
                    response = q.step.response
                    # Check for all possible quest events that can fire
                    if "event" in q.step.reactions[response]:
                        # Fires the specified event
                        event = Event(q.step.reactions[response]["event"])
                        fireEvent(event, player, self, areaController, customVariables=q.customVariables)
                    if "enableQuest" in q.step.reactions[response]:
                        # Enables the specified quest so that it can be started if criteria are met
                        for enable in q.step.reactions[response]["enableQuest"]:
                            enable_quests.append(enable)
                    if "setDesc" in q.step.reactions[response]:
                        # Modifies the current description for the quest in the player's journal
                        newDesc = q.step.reactions[response]["setDesc"]
                        newDesc = replaceVariablesInString(newDesc, q.customVariables)
                        q.desc = newDesc
                    if "giveXp" in q.step.reactions[response]:
                        # Gives the player xp
                        player.giveXP(response["giveXp"])
                    # If items need to be given, it should be done through a quest
                    # event, and not the quest itself.
                    if "setVis" in q.step.reactions[response]:
                        # hide or show the quest in the player's journal
                        # Ideally, should only be used to unhide an initially hidden quest
                        q.hidden = q.step.reactions[response]["setVis"]
                    # Check for next step
                    if "nextStep" in q.step.reactions[response]:
                        q.currentStep = q.step.reactions[response]["nextStep"]
                        q.step = QuestStep(GameDataHandler().getGameData("quest", q.id)[q.currentStep], query)
                    else:
                        # Complete the quest if no next step
                        q.completed = True
                        removed.append(quest)
            for quest in removed:
                # Remove the quest from the active list
                QuestWrangler.completed_quests[quest] = QuestWrangler.active_quests[quest]
                del QuestWrangler.active_quests[quest]
            
            # Confirm all quests are still active, and if not, move them to the completed list
            removed = []
            for quest in QuestWrangler.active_quests:
                pass
            for quest in removed:
                del QuestWrangler.active_quests[quest]

            # Enable any quests that are in the enable_quests list
            for quest in enable_quests:
                self.enable_quest(quest, True)
                if QuestWrangler.debug:
                    print(f"Quest {quest} enabled.")
        
        if QuestWrangler.debug:
            self.print_quest_lists(override=False)
    
    def print_quest_lists(self, **kwargs):
        if not QuestWrangler.debug:
            return
        if "override" in kwargs.keys() and not kwargs["override"]:
            return
        print("Quests:")
        print("\tPossible:")
        for q in QuestWrangler.quest_list:
            print(f"\t\t{q}")
        print("\tEnabled:")
        for q in QuestWrangler.enabled_quests.keys():
            print(f"\t\t{q}")
            for c in QuestWrangler.enabled_quests[q].spawnConditions:
                print(f"\t\t\t{c}")
        print("\tActive:")
        for q in QuestWrangler.active_quests.keys():
            quest = QuestWrangler.active_quests[q]
            print(f"\t\t{q} - {quest.get_current_step()}")
            for c in quest.step.checks.keys():
                for condition in quest.step.checks[c]:
                    print(f"\t\t\t{condition}")

        print("\tCompleted:")
        for q in QuestWrangler.completed_quests.keys():
            print(f"\t\t{q}")
