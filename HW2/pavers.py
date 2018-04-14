import sys

MAX_SIZE = 13
F = [0]*(MAX_SIZE+1)
F1 = [0]*(MAX_SIZE+1)
F2 = [0]*(MAX_SIZE+1)
F3 = [0]*(MAX_SIZE+1)
G = [0]*(MAX_SIZE+1)
G1 = [0]*(MAX_SIZE+1)
G2 = [0]*(MAX_SIZE+1)
G3 = [0]*(MAX_SIZE+1)

maxindex = 0

def comp_tiles():
	F[0],F[1],F[2] = 1, 2, 11
	F1[0],F1[1],F1[2] = 0, 2, 16
	F2[0],F2[1],F2[2] = 0, 1, 8
	F3[0],F3[1],F3[2] = 0, 0, 4
	G[0],G[1],G[2] = 0, 0, 2
	G1[0],G1[1],G1[2] = 0, 0, 1
	G2[0],G2[1],G2[2] = 0, 0, 1
	G3[0],G3[1],G3[2] = 0, 0, 1

	for n in range(2, MAX_SIZE):
		F[n+1] = 2*F[n] + 7*F[n-1] + 4*G[n]
		F1[n+1] = 2*F1[n] + 2*F[n] + 7*F1[n-1] + 8*F[n-1] + 4*G1[n]+2*G[n]
		F2[n+1] = 2*F2[n] + F[n] + 7*F2[n-1] + 4*F[n-1] + 4*G2[n]+2*G[n]
		F3[n+1] = 2*F3[n] + 7*F3[n-1] + 4*F[n-1] + 4*G3[n] + 2*G[n]
		test = 2.0*(n+1)*F[n+1]
		test1 = F1[n+1] + 2.0*F2[n+1] + 3.0*F3[n+1]
		if(abs(test - test1) > 0.0000001*test):
			print("mismatch ", n+1, ":", test, " != ", test1)

		G[n+1] = 2*F[n-1] + G[n]
		G1[n+1] = 2*F1[n-1] + F[n-1] + G1[n]
		G2[n+1] = 2*F2[n-1] + F[n-1] + G2[n] + G[n]
		G3[n+1] = 2*F3[n-1] + F[n-1] + G3[n]

	return 0

def main():
	fileName = sys.argv[-1]
	file = open(fileName, "r")

	line = file.readline().split()
	nprob = int(line[0])
	
	comp_tiles()

	for curprob in range(1, nprob+1):
		line = file.readline().split()
		index = int(line[0])
		n = int(line[1])

		if(index != curprob):
			print("Problem index ", index, "!= expected problem ", curprob)

		if(n == 1):
			print(curprob, "2 2 1 0")
		elif((n < 2) or (n > MAX_SIZE)):
			print("array width ", n, "not in range 2 ..", MAX_SIZE, "problem ", curprob)
		else:
			print(curprob, F[n],  F1[n], F2[n], F3[n])

	file.close()


main()
