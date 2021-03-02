from sys import argv
from enum import IntEnum, unique
from battleforms import BATTLEFORM_DICT, BattleFormEnum

class GameState(IntEnum):
	mainmenu = 0
	battle = 1

class Battle_Style(IntEnum):
	test = 0

class AttackMove:
	def __init__(self):
		pass

def main(*args):
	print('args: ', args)

	'''
	for key in BATTLEFORM_DICT:
		print(key.value, str(BATTLEFORM_DICT[key]))
	'''

	done = False

	while (not done):
		pass


if __name__=='__main__':
	main(argv[1:])