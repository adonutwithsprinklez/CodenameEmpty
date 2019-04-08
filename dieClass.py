import random

def rollDice(dieRolls):
	total = 0
	for dice in dieRolls.split(";"):
		if dice != 0 and dice != "0":
			multiplyer = 1
			if "-" == dice[0]:
				multiplyer = -1
				dice = dice[1:]
			bonus = 0
			if "+" in dice:
				dice,bonus = dice.split("+")
				bonus = int(bonus)
			elif "-" in dice:
				dice,bonus = dice.split("-")
				bonus = int(bonus) * -1
			numDice, diceSize = dice.split("d")
			for i in range(int(numDice)):
				total += multiplyer * random.randint(1,int(diceSize))
			total+=bonus
		else:
			total += 0
	return total

def maxRoll(dieRolls):
	total = 0
	for dice in dieRolls.split(";"):
		if 0 != dice and "0" != dice and "-" != dice[0]:
			bonus = 0
			if "+" in dice:
				dice,bonus = dice.split("+")
				int(bonus)
			elif "-" in dice:
				dice,bonus = dice.split("-")
				bonus= int(bonus) * -1
			numDice, diceSize = dice.split("d")
			total += int(numDice) * int(diceSize) + int(bonus)
		if dice[0] == "-":
			dice = dice[1:]
			bonus = 0
			if "+" in dice:
				dice,bonus = dice.split("+")
				int(bonus)
			elif "-" in dice:
				dice,bonus = dice.split("-")
				bonus= int(bonus) * -1
			numDice, diceSize = dice.split("d")
			total += int(numDice) * int(diceSize) + int(bonus) * -1
		else:
			total += 0
	return total