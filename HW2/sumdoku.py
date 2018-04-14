import sys
import copy

constraints = [[0 for c in range(9)] for r in range(15)]
valid_masks = [0, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x100]
ALL_MASK = 0X1ff

class SEARCH_STATE():
	def __init__(self):
		self.avail_mask = [[0 for c in range(9)] for r in range(9)]
		self.row_avail_counts = [[0 for c in range(9)] for r in range(9)]
		self.col_avail_counts = [[0 for c in range(9)] for r in range(9)]
		self.box_avail_counts = [[[0 for z in range(9)] for y in range(3)] for x in range(3)]
		self.val_set = [[0 for c in range(9)] for r in range(9)]

states = [SEARCH_STATE() for i in range(81)]

def search_init():
	pss = states[0]
	i = 0
	j = 0
	k = 0
	for i in range(9):
		for j in range(9):
			pss.avail_mask[i][j] = ALL_MASK
			pss.val_set[i][j] = 0
			pss.row_avail_counts[i][j] = 9
			pss.col_avail_counts[i][j] = 9

	for i in range(3):
		for j in range(3):
			for k in range(9):
				pss.box_avail_counts[i][j][k] = 9

#s is a string of <=>, and will be converted to -1 0 1 correspondingly 
#prow is an array of integers
def scan_convert(prow, n, s):
	i = 0
	for i in range(n):
		if(s[i] == '<'):
			prow[i] = -1
		elif(s[i] == '='):
			prow[i] = 0
		elif(s[i] == '>'):
			prow[i] = 1
		else:
			return i

	i += 1
	return i

def scan_constraints(file):
	i = 0
	j = 0
	n = 0
	for i in range(3):
		for j in range(3):
			line = file.readline()
			n = scan_convert(constraints[5*i+2*j], 6, line)

			if(n != 6):
				print("error: scan of first line of region")
			if(j < 2):
				line = file.readline()
				n = scan_convert(constraints[5*i+2*j+1], 9, line)

	return 0

def checkEqual(baseMask, chkMask):
	result = 0
	i = 0
	if(valid_masks[5] & baseMask):
		result |= valid_masks[5]

	for i in range(1,10):
		if(((valid_masks[i] & chkMask) == 0) and (valid_masks[10-i] & baseMask)):
			result |= valid_masks[10-i]
	return result

def checkLess(baseMask, chkMask):
	result = 0
	i = 0
	if(valid_masks[9] & baseMask):
		result |= valid_masks[9]
	for i in range(1,9):
		if((valid_masks[i] & chkMask) != 0):
			break
		elif(valid_masks[9-i] & baseMask):
			result |= valid_masks[9-i]

	return result

def checkGreater(baseMask, chkMask):
	result = 0
	i = 0
	if(valid_masks[1] & baseMask):
		result |= valid_masks[1]

	for i in range(9, 2, -1):
		if((valid_masks[i] & chkMask) != 0):
			break
		elif(valid_masks[11-i] & baseMask):
			result |= valid_masks[11-i]

	return result

def checkConstraint(constraint, baseMask, chkMask):
	if(constraint < 0):
		return checkLess(baseMask, chkMask)
	elif(constraint > 0):
		return checkGreater(baseMask, chkMask)
	else:
		return checkEqual(baseMask, chkMask)

def check_constraints(pss):
	i = 1
	row = 1
	col = 1
	baseConsRow = 1
	baseConsCol = 1
	scan_count = 1
	change_count = 1

	baseMask = 0
	chkMask = 0
	resultMask = 0
	totResult = 0

	scan_count = 0


	#indexCount = 0
	while(change_count > 0):

		scan_count += 1
		change_count = 0

		baseConsRow = 0
		for row in range(9):

			baseConsCol = 0
			for col in range(9):


				if(pss.val_set[row][col] == 0):
					baseMask = pss.avail_mask[row][col]
					totResult = 0

					if((col % 3) != 0):
						chkMask = pss.avail_mask[row][col-1]
						resultMask = checkConstraint(constraints[baseConsRow][baseConsCol-1], baseMask, chkMask)
						if(resultMask != 0):
							baseMask &= ~resultMask
							#print("baseMask = ", baseMask)
							change_count += 1
							totResult |= resultMask
							#print("a")
					if((col % 3) != 2):
						chkMask = pss.avail_mask[row][col+1]
						#print("baseConsRow = ", baseConsRow, " and baseConsCol = ", baseConsCol)
						resultMask = checkConstraint(constraints[baseConsRow][baseConsCol], baseMask, chkMask)
						if(resultMask != 0):
							baseMask &= ~resultMask
							change_count += 1
							totResult |= resultMask
							#print("b")


					if((row % 3) != 0):
						chkMask = pss.avail_mask[row-1][col]
						resultMask = checkConstraint(constraints[baseConsRow-1][col], baseMask, chkMask)
						if(resultMask != 0):
							baseMask &= ~resultMask
							change_count += 1
							totResult |= resultMask
							#print("c")
					if((row % 3) != 2):
						chkMask = pss.avail_mask[row+1][col]
						resultMask = checkConstraint(constraints[baseConsRow+1][col], baseMask, chkMask)
						if(resultMask != 0):
							baseMask &= ~resultMask
							change_count += 1
							totResult |= resultMask
							#print("d")

					#print("baseMask = ", baseMask)
					if(baseMask == 0):
						return -1

					pss.avail_mask[row][col] = baseMask
					if(totResult != 0):
						for i in range(9):
							if(valid_masks[i] & totResult):
								#print(row/3)
								pss.col_avail_counts[col][i-1] -= 1
								pss.row_avail_counts[row][i-1] -= 1
								pss.box_avail_counts[(row//3)][(col//3)][i-1] -= 1

				if((col % 3) != 2):
					baseConsCol += 1

			if((row % 3) != 2):
				baseConsRow += 2
			else:
				baseConsRow += 1
		#print("change_count = ", change_count)


	return 0			

STYP_ROW = 1
STYP_COL = 2
STYP_BOX = 3

class SOLVE_DATA():
	def __init__(self):
		self.solve_type = 0
		self.solve_val = 0
		self.solve_row = 0
		self.solve_col = 0
		self.solve_cnt = 0
		self.solve_index = 0
		self.test_row = 0
		self.test_col = 0

def GetSolveStep(pss, psd):
	i = 0
	j = 0
	k = 0
	psd.solve_cnt = 10
	for i in range(9):
		for j in range(9):
			if(pss.row_avail_counts[i][j] < psd.solve_cnt):
				psd.solve_cnt = pss.row_avail_counts[i][j]
				psd.solve_type = STYP_ROW
				psd.solve_row = i
				psd.solve_val = j+1

	#print("223: ",psd.solve_cnt)

	for i in range(9):
		for j in range(9):
			if(pss.col_avail_counts[i][j] < psd.solve_cnt):

				psd.solve_cnt = pss.col_avail_counts[i][j]
				psd.solve_type = STYP_COL
				psd.solve_col = i
				psd.solve_val = j+1

	#print("233:", psd.solve_cnt)

	for i in range(3):
		for j in range(3):
			for k in range(9):
				if(pss.box_avail_counts[i][j][k] < psd.solve_cnt):
					psd.solve_cnt = pss.box_avail_counts[i][j][k]
					psd.solve_type = STYP_BOX
					psd.solve_row = i
					psd.solve_col = j
					psd.solve_val = k+1

	#print("245:",psd.solve_cnt)
	if(psd.solve_cnt == 0):
		return -1
	else:
		return 0

def FindNextTest(pss, psd):
	i = 0
	j = 0
	starti = 0
	startj = 0

	mask = valid_masks[psd.solve_val]
	if(psd.solve_index >= psd.solve_cnt):

		#print("a")
		return -1

	if(psd.solve_type == STYP_ROW):
		if(psd.solve_index == 0):
			startj = 0
		else:
			startj = psd.test_col+1

		i = psd.solve_row
		for j in range(startj, 9):
			if(pss.avail_mask[i][j] & mask):
				psd.test_col = j
				psd.test_row = i
				psd.solve_index += 1
				return 0
		#print("b")
		return -1

	elif(psd.solve_type == STYP_COL):
		if(psd.solve_index == 0):
			starti = 0
		else:
			starti = psd.test_row+1

		j = psd.solve_col
		for i in range(starti, 9):
			if(pss.avail_mask[i][j] & mask):
				psd.test_col = j
				psd.test_row = i
				psd.solve_index += 1
				return 0
		#print("c")
		return -1

	elif(psd.solve_type == STYP_BOX):
		if(psd.solve_index == 0):
			starti = 0
			startj = 0
		else:
			starti = psd.test_row - 3*psd.solve_row
			startj = psd.test_col+1 - 3*psd.solve_col

		for i in range(starti, 3):
			for j in range(startj, 3):
				if(pss.avail_mask[i + 3*psd.solve_row][j+ 3*psd.solve_col] & mask):
					psd.test_col = j + 3*psd.solve_col
					psd.test_row = i + 3*psd.solve_row
					psd.solve_index += 1
					return 0

		#print("d")
		return -1

	else:
		print("bad solve type")
		return -1

def ApplyChoice(pss, row, col, val):
	i = 0
	j = 0
	boxr = 0
	boxc = 0

	mask = valid_masks[val]
	if(pss.val_set[row][col] != 0):
		print('error: ApplyChoice')
		return -1

	pss.val_set[row][col] = val

	boxr = int(row/3)
	boxc = int(col/3)

	for j in range(9):
		if(pss.avail_mask[row][j] & mask):
			pss.box_avail_counts[boxr][int(j/3)][val-1] -= 1
			pss.col_avail_counts[j][val-1] -= 1
		pss.avail_mask[row][j] &= ~mask

	for i in range(9):
		if(pss.avail_mask[i][col] & mask):
			pss.box_avail_counts[int(i/3)][boxc][val-1] -= 1
			pss.row_avail_counts[i][val-1] -= 1
		pss.avail_mask[i][col] &= ~mask

	boxr = int(row/3)
	boxc = int(col/3)

	for i in range(3*boxr, 3*(boxr+1)):
		for j in range(3*boxc, 3*(boxc+1)):
			if(pss.avail_mask[i][j] & mask):
				pss.col_avail_counts[j][val-1] -= 1
				pss.row_avail_counts[i][val-1] -= 1
			pss.avail_mask[i][j] &= ~mask

	for i in range(1,10):
		if((i != val) and (pss.avail_mask[row][col] & valid_masks[i]) != 0):
			pss.box_avail_counts[int(row/3)][int(col/3)][i-1] -= 1
			pss.col_avail_counts[col][i-1] -= 1
			pss.row_avail_counts[row][i-1] -= 1

	pss.avail_mask[row][col] = mask
	pss.row_avail_counts[row][val-1] = 32
	pss.col_avail_counts[col][val-1] = 32
	pss.box_avail_counts[boxr][boxc][val-1] = 32

	return 0

def Solve(level):
	#print(level)
	pssnxt = states[level]
	pss = states[level]

	sd = SOLVE_DATA()
	i = 0
	j = 0
	if(GetSolveStep(pss, sd) != 0):
		return -1

	sd.solve_index = 0
	while(FindNextTest(pss, sd) == 0):

		if(level == 80):
			pss.val_set[sd.test_row][sd.test_col] = sd.solve_val
			return 0
		else:
			#pssnxt = states[level+1]
			states[level+1] = copy.deepcopy(pss)
			pssnxt = states[level+1]

			if(ApplyChoice(pssnxt, sd.test_row, sd.test_col, sd.solve_val) == 0):
				if(check_constraints(pssnxt) == 0):
					if(Solve(level + 1) == 0):

						for i in range(9):
							for j in range(9):
								pss.val_set[i][j] = pssnxt.val_set[i][j]
						return 0

	return -1

def printAvailMusk():
	for i in range(9):
			for j in range(9):
				print(states[0].avail_mask[i][j], end = " ")
			print("")
	print("\n")

def printRowAvailCounts():
	for i in range(9):
			for j in range(9):
				print(states[0].row_avail_counts[i][j], end = " ")
			print("")
	print("\n")

def printColAvailCounts():
	for i in range(9):
			for j in range(9):
				print(states[0].col_avail_counts[i][j], end = " ")
			print("")
	print("\n")

def prinBoxAvailCounts():
	for i in range(3):
			for j in range(3):
				for k in range(9):
					print(states[0].box_avail_counts[i][j][k], end = " ")
			print("")
	print("\n")


def printConstraints():
	for i in range(15):
			for j in range(9):
				print(constraints[i][j], end = " ")
			print("")
	print("\n")

def main():
	nprob = 0
	curprob = 0
	index = 0
	ret = 0
	i = 0
	j = 0
	fileName = sys.argv[-1]
	file = open(fileName, "r")

	line = file.readline().split()
	nprob = int(line[0])
	
	for curprob in range(1, nprob+1):
		line = file.readline().split()
		index = int(line[0])


		search_init()
		
		ret = scan_constraints(file)


		resultOfCheckConstraints = check_constraints(states[0])


		'''printRowAvailCounts()
		printColAvailCounts()
		prinBoxAvailCounts()'''

		if(Solve(0) !=0):
			print("error: problem index has no solution")
			#return -9

		print(index)
		for i in range(9):
			for j in range(9):
				print(states[0].val_set[i][j], end = " ")
			print("")


	file.close()
	return 0



main()