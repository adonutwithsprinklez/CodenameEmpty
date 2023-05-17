
'''
CALL startApplication INSTEAD OF RUNNING THIS FILE DIRECTLY UNLESS
YOU KNOW WHAT YOU ARE DOING!!!

Only run this file if the game's resources are already decompressed.
If the game's resources are zipped then the game will fail to launch.
'''

import os
import shutil
import sys

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
	game.newGameMenu()
	if game.player == None:
		return False
	game.loadPlayer()
	while True:
		game.displayCurrentArea()
		game.reactCurrentArea()
		if game.player.quit:
			return None
		game.areaHub()
		if game.player.quit:
			# Removes the player object from the game object once done
			game.player = None
			return None
		if game.player.hp <= 0:
			# TODO have actual end of game code due to player death
			# Removes the player object from the game object once done
			game.player = None
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
	# TODO: Implement check to see if datapacks changed, and set game.initialLoad's 
	# third argument to True if they did
	game.initialLoad(RES_FOLDER, SETTINGS)

def startApplication(PATH=None, args=None):
	global GAME_VERSION, MIN_SAVE_VERSION, MIN_SAVE_VERSION
	global RES_FOLDER, SETTINGS, SETTINGS_FILE

	# Loads some resource stuff
	RES_FOLDER = "res/"
	if PATH:
		RES_FOLDER = PATH + "/res/"
	SETTINGS_FILE = RES_FOLDER + "settings.json"
	SETTINGS = loadJson(SETTINGS_FILE)

	# Check for datapacks in the resource folder
	dataPackFolders = []
	for item in os.listdir(RES_FOLDER):
		if item != "engine":
			possibleDirectory = os.path.join(RES_FOLDER, item)
			if os.path.isdir(possibleDirectory):
				dataPackFolders.append(item)
	# Remove from the settings file any datapacks that no longer exist in the res folder
	dps = SETTINGS["DATAPACKSETTINGS"]["packsToLoad"][::]
	for pack in SETTINGS["DATAPACKSETTINGS"]["packsToLoad"]:
		if pack[0] not in dataPackFolders:
			dps.remove(pack)
			# If the removed datapack = the starting datapack,
			# reset the starting datapack to the official one
			if pack[0] == SETTINGS["DATAPACKSETTINGS"]["start"]:
				SETTINGS["DATAPACKSETTINGS"]["packsToLoad"][0][1] = True
				SETTINGS["DATAPACKSETTINGS"]["start"] = "official"
		# Remove datapack from datapackfolders because it is already saved in settings
		elif pack[0] in dataPackFolders:
			dataPackFolders.remove(pack[0])
	# add saved datapacks to settings
	for pack in dataPackFolders:
		dps.append([pack, False])
	SETTINGS["DATAPACKSETTINGS"]["packsToLoad"] = dps
	# Save the settings file
	saveJson(SETTINGS_FILE, SETTINGS)

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

	# Inital game / menu loading
	game = Game()
	game.initialLoad(RES_FOLDER, SETTINGS, True, args)

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
		elif cmd == 3:
			# Displays the settings menu
			openSettings(game, SETTINGS_FILE)
		elif cmd == 4:
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
	if len(sys.argv)>1:
		args = sys.argv[1:]
	startApplication(None, args)