
import random

from effectClass import Effect, processEffect
from enemyClass import Enemy

# This file is used when putting functions into universalFunctions.py would create a circular import

def fireEvent(event, player, areaController, disp, gameData, debug=False):
    ''' This function is used to handle random events that can occur in the game. '''
    disp.dprint(f"Firing event: '{event.name}'")
    while not event.finished:
        disp.clearScreen()
        disp.displayHeader(f"{event.name}")
        disp.display(f"{event.msg}", 1)
        x = 0
        choices = event.getPossibleActions(player)
        if len(choices) > 0:
            disp.displayHeader("Actions", 1, 1)
            for choice in choices:
                x += 1
                action = choice["action"]
                disp.displayAction(f'{x}. {action}', x, 0)
            disp.closeDisplay()
            try:
                # cmd = int(input())
                cmd = disp.get_input(True)
            except:
                cmd = -1
            if cmd > 0 and cmd <= x:
                for action in choices[cmd-1]["eventDo"]:
                    disp.dprint(f"\t{action[0]}")
                    if action[0] == "say":
                        displayEventAction(areaController, disp, action[1])
                    elif action[0] == "goto":
                        if type(action[1]) == list:
                            event.gotoPart(random.choice(action[1]))
                        else:
                            event.gotoPart(action[1])
                    elif action[0] == "addTag":
                        player.tags.append(event.getTag(action[1]))
                    elif action[0] == "take":
                        event.takeItem(action[1], action[2], player)
                    elif action[0] == "give":
                        for i in range(action[2]):
                            result = event.giveItem(action[1], action[2], player, gameData)
                            if debug and not result:
                                raise Exception("Something went wrong when processing an event's 'give' command.")
                    elif action[0] == "spawnEnemy":
                        for enemyid in action[1]:
                            areaController.addEnemyToCurrentArea(Enemy(enemyid, gameData))
                    elif action[0] == "addArea":
                        areaController.addExitToAreaFromEvent(action[1])
                    elif action[0] == "addFlag":
                        if action[1] not in player.flags:
                            player.flags.append(action[1])
                    elif action[0] == "removeFlag":
                        if action[1] in player.flags:
                            player.flags.remove(action[1])
                    elif action[0] == "setName":
                        event.setName(action[1])
                    elif action[0] == "addEffect":
                        newEffect = Effect(action[1], gameData.getGameData("effect", action[1]))
                        player.effects.append(newEffect)
                        newEffect = player.effects[-1]
                        messages = processEffect(newEffect, player, gameData)
                        for message in messages:
                            displayEventAction(areaController, disp, message)
                    elif action[0] == "finish":
                        event.finish()
        else:
            disp.closeDisplay()
            event.finish()
            #input("\nEnter to continue")
            disp.wait_for_enter()
    disp.dprint(f"Event '{event.name}' finished")

def displayEventAction(areaController, disp, message):
    disp.clearScreen()
    event = areaController.getCurrentAreaEvent()
    if event:
        disp.displayHeader(event.name)
    else:
        disp.displayHeader("Event")
    if type(message) == list:
        for line in message:
            disp.display(line)
    else:
        disp.display(message)
    disp.closeDisplay()
    disp.wait_for_enter()