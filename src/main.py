from gameClass import Game
from jsonDecoder import loadJson, saveJson


# Starts the gameloop
def startGame(game):
	game.loadPlayer()
	while True:
		game.displayCurrentArea()
		game.reactCurrentArea()
		if game.player.quit:
			return None
		game.chooseNewArea()
		if game.player.quit:
			return None
		if game.player.hp <= 0:
			# TODO have actual end of game code due to player death
			return False

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