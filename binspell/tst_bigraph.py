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
import csv
from Trigraph import * 


def add(grph, symb1,symb2,weight):
	#global bigrph
	#print "symb1:", symb1, "symb2:", symb2, "weight:",weight 
	if symb1 not in grph:
		#print "not in:", symb1
		grph[symb1] = {symb2:weight}
	elif symb2 not in grph[symb1]:
		tmpDict = grph[symb1]
		tmpDict[symb2] = weight
		grph[symb1] = tmpDict
	return grph
	#print symb1, ':', bigrph[symb1]

	
def adjacent(symb1, symb2):
    global bigrph
    return symb2 in bigrph[symb1]

def get_weight(symb1,symb2):
    global bigrph
    if adjacent(symb1,symb2):
        tmpDict = bigrph[symb1]
        return tmpDict[symb2]
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

def buildWrdbGrph(fname,grph):
	bgrams = csv.reader(open('written-bigrams-freq.txt'),delimiter=' ')	
	#wrdLst = readWordFile(fname)
	#print wrdLst
	count = 0
	for row in bgrams:
		#bits = string.split(row,',')
		if count < 5:
			grph = add(grph,row[0],row[1],Decimal(row[2]))
			#print row
			#print row[0]
			#print row[1]
			#print Decimal(row[2])
			#print #
		count += 1
	print printBigrph(grph)
			



def buildWrdUGrph(fname,grph):
	ugrams = csv.reader(open('unigram_wrd.txt'),delimiter=' ')	
	#wrdLst = readWordFile(fname)
	#print wrdLst
	count = 0
	for row in ugrams:
		#bits = string.split(row,',')
		if count < 5:
			grph[row[0]] = Decimal(row[1])
			#print row
			#print row[0]
			#print row[1]
			#print Decimal(row[2])
			#print #
		count += 1
	print grph


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
	bgrams = csv.reader(open('written-bigrams-freq.txt'),delimiter=' ')
	count = 0
	for row in brams:
		if count < 5:
			print row
		count += 1
	#fd = open('bgTst.txt', 'r')
	#fd = open(fname, 'r')
	#print fd
	#print fd.readline()
	#lst = []
	#for line in fd:
		#print line[4]
		#why doesn't this work???????
		#line = line.strip(' ')
		#line = line.rstrip(' ')
		
		#bits = string.split(line, ',')
		#print "bits: ", bits
		#bits.append('4')
		#del(bits[len(bits)-1])
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


def readWordFile(fname):
	bgrams = csv.reader(open('written-bigrams-freq.txt'),delimiter=' ')
	count = 0
	for row in bgrams:
		#if count < 5:
			#print row
		count += 1
	return bgrams
	

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




def cleanRow(row):
	row[0] = row[0][0:-1]	#strip just the last xtra white-space off row[0]
	row[1] = row[1].strip(' ')	#strip all xtra white-space off row[1]
	row = row[0:-1]			#strip end of row to get ['trigram','value']
	return row


def buildTgrams(flname):
	#print "in buildTgrams"
	tgrams = csv.reader(open(flname),delimiter='-')
	count = 0
	for row in tgrams:
		if count < 5:
			#print row
			row = cleanRow(row)
			#print row
			#print #
		count += 1


#fname = "trgramsWithSpc.txt"
#buildTgrams(fname)

#filename = "written-bigrams-freq.txt"
#buildWrdUGrph(filename,{})
#buildWrdbGrph(filename,{})
#readWordFile(filename)
#filename = "bgramFreq3.txt"
#readFile()
#writeFile()
#bigrphLst = readFile(filename)
#buildGraph(filename,bigrph)
#symb = 'w'
#nxtProbSymb = 'b'
#print nxtProbBgramSymbLst(symb)
#print nxtProb(bigrph[symb],'y')
#print nxtProbSymbLst()
#orderGrph()
#printBigrph(bigrph)




x = Trigraph()
