# directed graph of bigrams using just first letter pair data
# what, why, when, where, who, how, yes, no, good, bad
# last edit: 6/18
################CHANGES############

##########TODO##############

######################BUGS#######################
# values in bigrph not stored correctly
#   -- see last line of add()
# question in nextProb
# items in buildgraph not exact
# orderGrph() called from buildGrph() gives duplicates
##############CURRENTLY WORKING ON##########

import heapq
from operator import itemgetter
import string
from decimal import Decimal


def add(grph, lett1,lett2,weight):
	#global bigrph
	#print "lett1:", lett1, "lett2:", lett2, "weight:",weight 
	if lett1 not in grph:
		#print "not in:", lett1
		grph[lett1] = {lett2:weight}
	elif lett2 not in grph[lett1]:
		tmpDict = grph[lett1]
		tmpDict[lett2] = weight
		grph[lett1] = tmpDict
	#print lett1, ':', bigrph[lett1]

	
def adjacent(lett1, lett2):
    global bigrph
    return lett2 in bigrph[lett1]

def get_weight(lett1,lett2):
    global bigrph
    if adjacent(lett1,lett2):
        tmpDict = bigrph[lett1]
        return tmpDict[lett2]
    else: return 0


def orderGrph():
	global bigrph
	newLst = []
	for key in bigrph:
		newLst = sorted(bigrph[key].items(), key=itemgetter(1), reverse=True)		
		#bigrph[key] = dict(newLst)
		print key, ": "
		print newLst
		#print dict(newLst)
		print "#############"
		#print bigrph[key]



def buildGraph(fname,grph):
	fd = open(fname, 'r')
	for line in fd:		
		bits = string.split(line, ',')
		del(bits[len(bits)-1])		
		for i in range(1,len(bits),2):
			add(grph, bits[0], bits[i], Decimal(bits[i+1]))
			

def nxtProb(probDict,lastProbSymb):
	ordLst = sorted(probDict.items(), key=itemgetter(1), reverse=True)
	flag = False
	for symb, freq in ordLst:
		#print symb 
		#print freq
		if lastProbSymb == '':
			return symb
		if flag:
			#print symb
			return symb
		if lastProbSymb in symb:
			#print "lastProbSymb:", lastProbSymb
			#print "sym:", symb
			flag = True		#set flag cuz its the next in the ordered list
	return ''  #came to last item in list - now use huffman
	

def printBigrph(bgrph):
	#global bigrph
	for key in bgrph:
		#print key
		print key, " : ", bgrph[key]
		print "###############"
		
		
		
		
def readFile(fname):
	#fd = open('bgTst.txt', 'r')
	fd = open(fname, 'r')
	#print fd
	#print fd.readline()
	#lst = []
	for line in fd:
		#print line[4]
		#why doesn't this work???????
		#line = line.strip(' ')
		#line = line.rstrip(' ')
		
		bits = string.split(line, ',')
		#print "bits: ", bits
		#bits.append('4')
		del(bits[len(bits)-1])
		#print "end of bits: ", bits[len(bits)-1]
		#print len(bits)
		
		for i in range(1,len(bits),2):
			#print "i: ", i
			#print bits[i]
			#print bits[i+1]
			#print Decimal(bits[i+1])
			add(bits[0], bits[i], Decimal(bits[i+1]))
			#print "a: ", a
			#print "b", b
		#print bits[0]
		#print bits[len(bits)-2]
		#print Decimal(bits[2].strip(' ')) + 1
		#item = [bits[0], bits[1], Decimal(bits[2].strip(' ')) ]
		#lst.append(item)
	#print lst
	return lst
	

# cu,cy, fr, ft, fu, fy, hy, kw,
# takes bigram freq values as input from keyboard and writes to file
# writes in format: e.g. a:a,3,b,5,...\n
def writeFile():
	alpha = map(chr, range(97, 123))
	#alpha = map(chr, range(97, 99))
	fd = open('bgramFreq3.txt', 'w')
	for symb in alpha:
		fd.write('%s,' %symb)
		for symb2 in alpha:
			freq = raw_input("%s,%s freq? " %(symb, symb2))
			#item = '%s,%s,%s' %(symb,symb2,lett)
			fd.write('%s,%s,' %(symb2,freq))
			#print item
		fd.write('\n')
	fd.close()


def nxtProbBgramSymbLst(lastTyped):
	global bigrph
	probBgramLst = []
	tmpLst = bigrph[lastTyped]
	
	#orderd list of first chars of bigram to be returned
	ordLst1 = sorted(tmpLst.items(), key=itemgetter(1), reverse=True)
	for a,b in ordLst1:
		tmpLst = bigrph[a]
		ordLst2 = sorted(tmpLst.items(), key=itemgetter(1), reverse=True)
		item = a + ordLst2[0][0]
		probBgramLst.append(item)
	return probBgramLst

   
bigrph = {}
#adjLst = [[1,2,3],[4,5,6]]
#print 2 in adjLst[0]

bigrphLst = [
		['w','h',9.7],
		['h','a',2.4],
		['a','t',0.8],
		['h','e',3.0],
		['e','n',2.7],
		['e','r',0.1],
		['r','e', 11.6],
		['h','y',0.1],
		['h','o',3.4],
		['o','w',2.7],
		['y','e',0.1],
		['e','s',0.5],
		['g','o',2.3],
		['o','o',4.6],
		['o','d',1.4],
		['b','a',1.1],
		['a','d',1.4]
]


filename = "bgramFreq3.txt"
#readFile()
#writeFile()
bigrphLst = readFile(filename)
buildGraph(filename,bigrph)
#symb = 'w'
#nxtProbSymb = 'b'
#print nxtProbBgramSymbLst(symb)
#print nxtProb(bigrph[symb],'y')
#print nxtProbSymbLst()
#orderGrph()
printBigrph(bigrph)
