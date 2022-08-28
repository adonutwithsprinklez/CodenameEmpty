
'''
CALL startApplication INSTEAD OF RUNNING THIS FILE DIRECTLY UNLESS
YOU KNOW WHAT YOU ARE DOING!!!

Only run this file if the game's resources are already decompressed.
If the game's resources are zipped then the game will fail to launch.
'''

import os
import shutil

from gameClass import Game
from jsonDecoder import loadJson, saveJson


GAME_VERSION = 0.1
MIN_DATA_PACK_VERSION = 0.1
MIN_SAVE_VERSION = 0.1

RES_FOLDER = None
SETTINGS_FILE = None
SETTINGS = None


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
	global RES_FOLDER, SETTINGS
	game.openOptionsWindow()
	saveJson(settingsFile, game.settings)
	game.initialLoad(RES_FOLDER, SETTINGS)

def openDataPacks(game, settingsFile):
	global RES_FOLDER, SETTINGS
	game.openDataPacks()
	saveJson(settingsFile, game.settings)
	game.initialLoad(RES_FOLDER, SETTINGS)

def startApplication():
	global GAME_VERSION, MIN_SAVE_VERSION, MIN_SAVE_VERSION
	global RES_FOLDER, SETTINGS, SETTINGS_FILE

	# Loads some resource stuff
	RES_FOLDER = "res/"
	SETTINGS_FILE = RES_FOLDER + "settings.json"
	SETTINGS = loadJson("{}".format(SETTINGS_FILE))

	# TODO Rewrite this bs
	'''
	if __name__ != "__main__":
		# Unpack the datapack zip folders if needed
		print("Prepping datapacks...")
		subfolders = [ f.name for f in os.scandir(RES_FOLDER) if f.is_dir() ]
		for file in os.listdir(RES_FOLDER):
			if file.endswith(".zip"):
				print("\tPrepping datapack '{}'".format(os.path.join(RES_FOLDER, file)))
				if file.split(".zip")[0] in subfolders:
					print ("\t\tDatapack already loaded.")
				else:
					print ("\t\tDecompressing datapack...")
					shutil.unpack_archive(RES_FOLDER + file, RES_FOLDER + file.split(".zip")[0])
	'''
	if __name__ != "__main__":
		pass

	# Inital game / menu loading
	game = Game()
	game.initialLoad(RES_FOLDER, SETTINGS)

	appRunning = True
	while appRunning and game.disp.window_is_open:
		game.displayMainMenu()
		try:
			# cmd = int(input())
			cmd = game.disp.get_input(True)
			print(cmd)
		except ValueError:
			cmd = -1
		except:
			cmd = -1
			appRunning = False
		
		if cmd == 1:
			# Actually start the game
			startGame(game)
		elif cmd == 2:
			# Displays the settings menu
			openSettings(game, SETTINGS_FILE)
		elif cmd == 3:
			# Displays the data pack menu
			openDataPacks(game, SETTINGS_FILE)
		elif cmd == 0:
			# Exit the game
			appRunning = False
		else:
			pass #TODO finish incorrect command message
	
	# Shutdown the app window
	game.shutdown_game()

	# TODO REMOVE THIS BULLSHIT
	'''
	if __name__ != "__main__":
		# Delete the uncompressed datapack folders
		subfolders = [ f.name for f in os.scandir(RES_FOLDER) if f.is_dir() ]
		for folder in subfolders:
			shutil.rmtree(RES_FOLDER+folder)
	'''

# This code runs with main.py is opened
if __name__ == "__main__":
	startApplication()