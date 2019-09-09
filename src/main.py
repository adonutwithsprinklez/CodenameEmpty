from gameClass import Game
from jsonDecoder import loadJson, saveJson


# Starts the gameloop
def startGame(game):
	run = True
	while game.player.hp > 0:
		game.displayCurrentArea()
		game.reactCurrentArea()
		game.chooseNewArea()
		if game.player.hp <= 0:
			run=False

def openSettings(game, settingsFile):
	game.openOptionsWindow()
	saveJson(settingsFile, game.settings)
	game.initialLoad(RES_FOLDER, SETTINGS)

def openDataPacks(game, settingsFile):
	game.openDataPacks()
	saveJson(settingsFile, game.settings)
	game.initialLoad(RES_FOLDER, SETTINGS)


# This code runs with main.py is opened
if __name__ == "__main__":
	# Loads some resource stuff
	RES_FOLDER = "res/"
	SETTINGS_FILE = RES_FOLDER + "settings.json"
	SETTINGS = loadJson("{}".format(SETTINGS_FILE))

	# Inital game / menu loading
	game = Game()
	game.initialLoad(RES_FOLDER, SETTINGS)

	appRunning = True
	while appRunning:
		game.displayMainMenu()
		try:
			cmd = int(input())
		except ValueError:
			cmd = -1
		
		if cmd == 1:
			# Actually start the game
			startGame(game)
		elif cmd == 2:
			# Displays the settings menu
			openSettings(game, SETTINGS_FILE)
		elif cmd == 3:
			openDataPacks(game, SETTINGS_FILE)
		elif cmd == 0:
			# Exit the game
			appRunning = False
		else:
			pass #TODO finish incorrect command message

# print game.currentArea.name
# print game.currentArea.desc
# print game.currentArea.enemy
# print game.currentArea.event
# print game.currentArea.npc