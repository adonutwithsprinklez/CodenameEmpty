from gameClass import Game

game = Game()
game.initialLoad()

run = True
while game.player.hp > 0:
	game.displayCurrentArea()
	game.reactCurrentArea()
	game.chooseNewArea()
	if game.player.hp <= 0:
		run=False

# print game.currentArea.name
# print game.currentArea.desc
# print game.currentArea.enemy
# print game.currentArea.event
# print game.currentArea.npc