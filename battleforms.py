from enum import IntEnum, unique

class BattleFormData():
	def __init__(self, enumid, name, flowsintolist):
		self.enumid = enumid
		self.name = name
		self.flows = flowsintolist[:]

	def __str__(self):
		return self.name

@unique
class BattleFormEnum(IntEnum):
	oceanking = 1
	mountainman = 2
	forestguardian = 3
	thundergod = 4
	sunemporer = 5
	moonempress = 6
	freespirit = 7
	justlaw = 8
	eternalsky = 9
	motherslove = 10
	fathomlessabyss = 11
	stillmind = 12

'''
~~~~~~~ FORM NOTES ~~~~~~~~~~

- flow only matters when changing forms -- forms essentially flow into themselves (not explicitly)
- if you don't flow, your priority drops by 1. If your 
attack move has +1 priority, it's instead zero.
- pokemon types average 3.5 super effective per type (between 2 and 5), out of ~16
	-> FLOWSTO range from 2 to 5
- pokemon types range from 1 to 7 weaknesses
	-> FLOWSFROM range from 1 to 7



~~~~~~ LOOPS ? ~~~~~~~~~~~~~~~~~

0) all forms into themselves

'''

BATTLEFORM_DICT = {}

BATTLEFORM_DICT[BattleFormEnum.oceanking] = BattleFormData(
	BattleFormEnum.oceanking,
	'Ocean King',
	[
		BattleFormEnum.eternalsky,
		BattleFormEnum.fathomlessabyss,
		BattleFormEnum.forestguardian
	])
BATTLEFORM_DICT[BattleFormEnum.mountainman] = BattleFormData(
	BattleFormEnum.mountainman,
	'Mountain Man',
	[
		BattleFormEnum.oceanking
	])
BATTLEFORM_DICT[BattleFormEnum.forestguardian] = BattleFormData(
	BattleFormEnum.forestguardian,
	'Forest Guardian',
	[
	])
BATTLEFORM_DICT[BattleFormEnum.thundergod] = BattleFormData(
	BattleFormEnum.thundergod,
	'Thunder God',
	[
		BattleFormEnum.oceanking,
		BattleFormEnum.mountainman,
		BattleFormEnum.forestguardian
	])
BATTLEFORM_DICT[BattleFormEnum.sunemporer] = BattleFormData(
	BattleFormEnum.sunemporer,
	'Sun Emporer',
	[
		BattleFormEnum.forestguardian
	])
BATTLEFORM_DICT[BattleFormEnum.moonempress] = BattleFormData(
	BattleFormEnum.moonempress,
	'Moon Empress',
	[
		BattleFormEnum.oceanking,
		BattleFormEnum.motherslove
	])
BATTLEFORM_DICT[BattleFormEnum.freespirit] = BattleFormData(
	BattleFormEnum.freespirit,
	'Free Spirit',
	[
		BattleFormEnum.stillmind,
		BattleFormEnum.motherslove
	])
BATTLEFORM_DICT[BattleFormEnum.justlaw] = BattleFormData(
	BattleFormEnum.justlaw,
	'Just Law',
	[
		BattleFormEnum.freespirit
	])
BATTLEFORM_DICT[BattleFormEnum.eternalsky] = BattleFormData(
	BattleFormEnum.eternalsky,
	'Eternal Sky',
	[
		BattleFormEnum.thundergod
	])
BATTLEFORM_DICT[BattleFormEnum.motherslove] = BattleFormData(
	BattleFormEnum.motherslove,
	'Mother\'s Love',
	[
	])
BATTLEFORM_DICT[BattleFormEnum.fathomlessabyss] = BattleFormData(
	BattleFormEnum.fathomlessabyss,
	'Fathomless Abyss',
	[
	])
BATTLEFORM_DICT[BattleFormEnum.stillmind] = BattleFormData(
	BattleFormEnum.stillmind,
	'Still Mind',
	[
	])


def analyze():
	textlength = 16
	print()
	print('FLOWSTO\t\tFLOWSFROM\tLOOPS\t\tNAME')
	row = 0
	allLoops = detectloops()
	for key in BATTLEFORM_DICT:
		if row%3==0:
			print('.   '*textlength)
		row += 1

		form = BATTLEFORM_DICT[key]
		flowsto = len(form.flows)
		flowsfrom = 0
		for key2 in BATTLEFORM_DICT:
			fromform = BATTLEFORM_DICT[key2]
			if (form.enumid in fromform.flows):
				flowsfrom += 1

		loops = 0
		for loop in allLoops:
			if key in loop:
				loops += 1

		print('%d\t\t%d\t\t%d\t\t%s' % (flowsto, flowsfrom, loops, form.name))
	print('.   '*textlength)
	print()
	print('LOOPS')
	print()
	for i in range(len(allLoops)):
		print('~~~ #%d ~~~' % i)
		printloop(allLoops[i])
		print()

	print('.   '*textlength)

def printloop(loop):
	result = ''
	for i in range(len(loop)):
		node = loop[i]
		result += '%s ->' % BATTLEFORM_DICT[node].name
		result += '\n' + '  '*(i+1)
	result += '...'
	print(result)

def cycleequal(cyc1, cyc2):
	length = len(cyc1)
	len2 = len(cyc2)
	if (length == 0 or len2 == 0 or length != len2):
		return False
	shift = -1
	try:
		shift = cyc2.index(cyc1[0])
	except:
		pass
	if (shift < 0):
		return False
	for i in range(len(cyc1)):
		shiftedindex = (shift+i)%length
		if (cyc2[shiftedindex] != cyc1[i]):
			return False
	return True

# build tree, keep track of flows, parents, and form. 
# If flow is in parents, remove. If flow is form, add to loop.
def detectloops():
	loops = []
	for head in BATTLEFORM_DICT.values():
		tree = buildtree([head.enumid])
		loops.extend(tree)

	repeatloops = {}
	for i in range(len(loops)):
		repeatloops[i] = []
		for j in range(len(loops)):
			if i != j:
				if (cycleequal(loops[i], loops[j])):
					repeatloops[i].append(j)

	result = []
	repeat = []
	for key in repeatloops:
		if (key not in repeat):
			result.append(loops[key])
			repeat.extend(repeatloops[key])

	return result

def buildtree(path):
	result = []
	parent = path[-1]
	children = BATTLEFORM_DICT[parent].flows
	for child in children:
		childindex = -1
		try:
			childindex = path.index(child)
		except:
			pass
		if childindex >= 0:
			result.append(path[childindex:])
		else:
			result.extend(buildtree(path+[child]))
	return result


if __name__=='__main__':
	analyze()