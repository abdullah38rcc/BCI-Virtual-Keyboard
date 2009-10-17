##############non_working version#########
#huffman using recursive alg 2


import heapq
 
def makeHuffTree(symbolTupleList):
	trees = list(symbolTupleList)
 
	heapq.heapify(trees)
	while len(trees) > 1:
		childR, childL = heapq.heappop(trees), heapq.heappop(trees)
		#print "childL:",childL
		#print "childR",childR
		#print "##########"
		parent = (childL[0] + childR[0], childL, childR)
		#print "parent:", parent
		#print "##########"
		heapq.heappush(trees, parent)
 
	return trees[0]
 
def printHuffTree(huffTree, prefix = 0, codes = {}):
    if len(huffTree) == 2:
		if prefix == 0:
			codes[huffTree[1]] = 0
		else:
			codes[huffTree[1]] = prefix
		print codes
		print "#########"
 
    else:
		#print "in else"
		#print "prefix:", prefix
		#print "huffTree[1]:",huffTree[1]
		#print "++++++++"
		#print "huffTree[2]:",huffTree[2]
		#print "#########################"

		printHuffTree(huffTree[1], prefix + 1)
		printHuffTree(huffTree[2], prefix + 1)
 
if False:
	exampleData = [
		(8 , 'e'),   
		(6 , 't'),   
		(5 , 'a'),   
		(2 , 'i')  
	]


if True:
	exampleData = [
	   (0.124167  , 'e'),   
	   (0.0969225 , 't'),   
	   (0.0820011 , 'a'),   
	   (0.0768052 , 'i'),   
	   (0.0764055 , 'n'),   
	   (0.0714095 , 'o'),   
	   (0.0706768 , 's'),   
	   (0.0668132 , 'r'),   
	   (0.0448308 , 'l'),   
	   (0.0363709 , 'd'),   
	   (0.0350386 , 'h'),   
	   (0.0344391 , 'c'),   
	   (0.028777  , 'u'),   
	   (0.0281775 , 'm'),   
	   (0.0235145 , 'f'),   
	   (0.0203171 , 'p'),   
	   (0.0189182 , 'y'),   
	   (0.0181188 , 'g'),   
	   (0.0135225 , 'w'),   
	   (0.0124567 , 'v'),   
	   (0.0106581 , 'b'),   
	   (0.00393019, 'k'),   
	   (0.00219824, 'x'),   
	   (0.0019984 , 'j'),   
	   (0.0009325 , 'q'),   
	   (0.000599  , 'z')   
	 ]

 
 
if __name__ == '__main__':
    huffTree = makeHuffTree(exampleData)
	
    printHuffTree(huffTree)
 
