import sys
import queue

class Square:
    def __init__(self):
        self.val = '#'
        self.row = 0
        self.col = 0
        self.avail = set()
        
    def __gt__(self, other):
        return len(self.avail) > len(other.avail)


    
class Solution:
    def __init__(self, line, file):
    	##############grid part##########
        r = int(line[1])
        c = int(line[2])
        #print(r, c)
        self.grid = [[Square() for x in range(1, c+3)]for y in range(1, r+3)]
        for i in range(1, r+1):
            line = (file.readline()).split()
            for j in range(1, c+1):
                v = line[j-1]
                self.grid[i][j].val = v
                self.grid[i][j].row = i
                self.grid[i][j].col = j

        #printGrid(self, r, c)    #to be deleted

        ###############blocks part########
        self.to_do = queue.PriorityQueue()

        nblocks = int(file.readline())
        #print(nblocks)
        for i in range(0, nblocks):
            line = (file.readline()).split()	#each line of squares
            blk = set()
            nsquares = int(line[0])
            #print(nsquares, end = " ")
            for j in range(1, nsquares+1):
                blk.add(str(j))

            for j in range(1, nsquares+1):
            	row = int(line[j][1])
            	col = int(line[j][-2])

            	if(self.grid[row][col].val != '-'):
            		blk.remove(self.grid[row][col].val)

            	self.grid[row][col].avail = blk
            	if(self.grid[row][col].val == '-'):
            		self.to_do.put(self.grid[row][col])

            #print(blk)
                
def adjacent_okay(s, val, r, c):
	for dr in range(-1,2):
		for dc in range(-1,2):
			if(s.grid[r+dr][c+dc].val == val):
				return False
	return True
        
def attempt(s):
	if(s.to_do.empty()):
		return True
	curr = s.to_do.get()
	row = curr.row
	col = curr.col
	avail = curr.avail

	#p is element in set avail, which is just val
	for p in avail:
		if(adjacent_okay(s, p, row, col)):
			curr.avail.remove(p)
			s.grid[row][col].val = p

			if(attempt(s)):
				return True
			s.grid[row][col].val = '-'
			curr.avail.add(p)
	s.to_do.put(curr)
	return False


def printGrid(self, r, c):
    for i in range(1, r+1):
        for j in range(1, c+1):
            print("(", self.grid[i][j].val, end = " ")
            print(")", end = " ")
        print("")

def printSquare(s):
	print(s.val, end = "")

def printSolution(s):
	for i in range(1, len(s.grid)-1):
		for j in range(1, len(s.grid[i])-1):
			if(j != 1):
				print(" ",end = "")
			printSquare(s.grid[i][j])

		print("")

                
def main():
    fileName = sys.argv[-1]
    file = open(fileName, "r")
    
    p = int(file.readline())
    #print(p)
    for i in (range(1,p+1)):
        line = (file.readline()).split()
        k = int(line[0])
        print(k)
        soln = Solution(line, file)



        if(attempt(soln)):
            printSolution(soln)
        else:
            print("No Solution.")

    file.close()
        
main()

