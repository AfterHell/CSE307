import sys

MAX_NODES = 20
MAX_QUERIES = 10

Adjacent = [[0.0 for c in range(MAX_NODES + MAX_QUERIES)] for r in range(MAX_NODES+1)]
query1 = [0 for i in range(MAX_QUERIES)]
query2 = [0 for i in range(MAX_QUERIES)]

def Adjacentinit(nnodes, nqueries):
	for i in range(0, nnodes+1):
		for j in range(0, nnodes + nqueries):
			Adjacent[i][j] = 0.0

	for i in range(0, nnodes):
		Adjacent[nnodes][i] = 1.0

	return 0

#pb is a string here, and we need to convert it to a list of chars to manipulate them
def ScanEdgeData(nnodes, pb):
	node = 0
	count = 0

	line = pb.split()
	node = int(line[0])
	count = int(line[1])		#count is the second number of each line

	Adjacent[node-1][node-1] += count
	for i in range(count):
		val = int(line[i+2])

		Adjacent[node-1][val-1] = -1.0
		Adjacent[val-1][node-1] = -1.0
		Adjacent[val-1][val-1] += 1.0

	return count

def FindMaxRow(nnodes, nqueries, currow):
	max1 = abs(Adjacent[currow][currow])
	maxrow = currow
	for i in range(currow+1, nnodes+1):
		tmp = abs(Adjacent[i][currow])
		if(tmp > max1):
			max1 = tmp
			maxrow = i
	return maxrow

def SwapRows(maxrow, currow, nnodes, nqueries):
	ncols = nnodes + nqueries
	for i in range(ncols):
		tmp = Adjacent[currow][i]
		Adjacent[currow][i] = Adjacent[maxrow][i]
		Adjacent[maxrow][i] = tmp

def Eliminate(currow, nrows, ncols):
	i = j = 0
	factor = 0.0
	for i in range(nrows):
		if(i == currow):
			continue
		factor = Adjacent[i][currow]
		for j in range(currow, ncols):
			Adjacent[i][j] -= factor*Adjacent[currow][j]

	return 0

def DumpMatrix(nrows, ncols):
	for i in range(nrows):
		for j in range(ncols):
			print(format(Adjacent[i][j], '.2f'), end = " ")
		print("")
	print("")

def SolveMatrix(nnodes, nqueries):
	ncols = nnodes+nqueries
	nrows = nnodes+1
	for currow in range(nnodes):
		maxrow = FindMaxRow(nnodes, nqueries, currow)
		if(maxrow != currow):
			SwapRows(maxrow, currow, nnodes, nqueries)
		pivot = Adjacent[currow][currow]
		if(abs(pivot) < 0.001):
			return -1
		pivot = 1.0/pivot

		for i in range(currow, ncols):
			Adjacent[currow][i] *= pivot

		Eliminate(currow, nrows, ncols)
		#DumpMatrix(nrows, ncols)

	return 0



def main():
	nprob = curprob = index = nnodes = nqueries = nedges = 0
	i = edgecnt = edgelines = queryno = 0
	dist = 0.0

	fileName = sys.argv[-1]
	file = open(fileName, "r")

	nprob = int(file.readline())
	#print("Number of problems: ", nprob)

	for curprob in range(1, nprob+1):
		line = file.readline().split()
		index, nnodes, nqueries, nedges = int(line[0]), int(line[1]), int(line[2]), int(line[3])
		Adjacentinit(nnodes, nqueries)
		edgecnt = edgelines = 0

		while(edgecnt < nedges):
			line = file.readline()
			i = ScanEdgeData(nnodes, line)
			if(i < 0):
				print("ScanEdgeData problem")
			edgelines += 1
			edgecnt += i

		for i in range(nqueries):
			line = file.readline().split()
			queryno, query1[i], query2[i] = int(line[0]), int(line[1]), int(line[2])

			if((i+1) != queryno):
				print("error: read query num != expected problem")

			if((query1[i] < 1) or (query1[i] > nnodes) or (query2[i] < 1)
			or (query2[i] > nnodes) or (query1[i] == query2[i])):
				print("bad query1 and query2")

			Adjacent[query1[i]-1][nnodes+i] = 1.0
			Adjacent[query2[i]-1][nnodes+i] = -1.0

		#DumpMatrix(nnodes+1, nnodes+nqueries)
		i = SolveMatrix(nnodes, nqueries)
		if(i != 0):
			print("error: return from SolveMatrix problem")
		else:
			print(curprob, end = " ")
			for i in range(nqueries):
				dist = abs(Adjacent[query1[i]-1][nnodes+i] - Adjacent[query2[i]-1][nnodes+i])
				print(format(dist, '.3f'), end = " ")
			print("")


	file.close()
	return 0





main()

