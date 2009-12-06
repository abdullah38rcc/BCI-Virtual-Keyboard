# bigraph class
# last edit: 7/28
################CHANGES############
# 
##########TODO##############
# change variable and method names to be more clear
######################BUGS#######################
# 
##############CURRENTLY WORKING ON##########
# 

from operator import itemgetter
import string
from decimal import Decimal



class Bigraph:
	
	def __init__(self):
		self._joint1 = {}					# list of bigram joint probs for beginning of word: [(char1,char2),prob]
		self._conditional1 = {}				# dict of bigram conditional probs for beginnning of word
		self._prior = {}

		self._joint2 = {}					# list of bigram joint probs for other positions in word
		self._conditional2 = {}				# dict of bigram conditional probs for other positions in word

		self._topList = []					# list of top 3 most next most probable letters
		self._f1name = 'bgramFreq1.txt'
		self._f2name = 'bgramFreq2.txt'

		#self._test()
		self._start()
		#self._buildGraph(self._f1name, self._conditional1)
		#self._buildGraph(self._f2name, self._bigrph2)

#########-----------no longer used-----------#############
		self._suggSymbList = []
		self._bigrphLst = [
				[('w','h'),9.7],
				[('h','a'),2.4],
				[('a','t'),0.8],
				[('h','e'),3.0],
				[('e','n'),2.7],
				[('e','r'),0.1],
				[('r','e'), 11.6],
				[('h','y'),0.1],
				[('h','o'),3.4],
				[('o','w'),2.7],
				[('y','e'),0.1],
				[('e','s'),0.5],
				[('g','o'),2.3],
				[('o','o'),4.6],
				[('o','d'),1.4],
				[('b','a'),1.1],
				[('a','d'),1.4],
				[(' ','a'),2.2],
				[(' ', 'c'),0.4],
				[(' ','e'),0.03]
		]



	def _test(self):
		#print "testing"
		freqs = self._bigrphLst
		val = 1

		freqs = self._addN(freqs,val)  #get rid of all zeros
		self._prior = self._getPrior(freqs)
		temp = self._normalize(dict(freqs))
		freqs = list((key,temp[key]) for key in temp)  #flatten out dict to pass to graph
		self._joint1 = self._buildGraph(freqs)
		#self._print(self._joint1)
		for key in self._joint1:	#build graph of conditional probs
			self._conditional1[key] =  self._conditionalOn(self._joint1[key])
		#print "conditional graph:"
		self._print(self._conditional1)

		freqs = self._bigrphLst
		freqs = self._addN(freqs,val)  #get rid of all zeros
		temp = self._normalize(dict(freqs))
		freqs = list((key,temp[key]) for key in temp)  #flatten out dict to pass to graph
		self._joint2 = self._buildGraph(freqs)
		#self._print(self._joint2)
		for key in self._joint2:	#build graph of conditional probs
			self._conditional2[key] =  self._conditionalOn(self._joint2[key])
		self._print(self._conditional2)



	def _start(self):
		val = 1	#flatten out distribution
		freqs = self._readFile(self._f1name)
		#print lst
		freqs = self._addN(freqs,val)  #get rid of all zeros
		self._prior = self._getPrior(freqs)
		#print "prior:"
		#print self._prior
		temp = self._normalize(dict(freqs))
		freqs = list((key,temp[key]) for key in temp)  #flatten out dict to pass to graph
		self._joint1 = self._buildGraph(freqs)
		#self._print(self._joint1)
		for key in self._joint1:	#build graph of conditional probs
			self._conditional1[key] =  self._conditionalOn(self._joint1[key])
		#self._conditional1.update(self._prior)
		#print "self._conditional1[" "] :", self._conditional1[" "]
		#print "conditional1 graph:"
		#self._print(self._conditional1)
		#print ##

		freqs = self._readFile(self._f2name)
		freqs = self._addN(freqs,val)  #get rid of all zeros
		temp = self._normalize(dict(freqs))
		freqs = list((key,temp[key]) for key in temp)  #flatten out dict to pass to graph
		self._joint2 = self._buildGraph(freqs)
		#self._print(self._joint2)
		for key in self._joint2:	#build graph of conditional probs
			self._conditional2[key] =  self._conditionalOn(self._joint2[key])
		#print "conditional2"
		#self._print(self._conditional2)



################################## hmm #######################
	def _getPrior(self,joint):
		#print joint
		raw = self._buildGraph(joint)
		#print "raw:"
		#self._print(raw)
		#print ##
		temp = {}
		prior = {}
		for key in raw:
			temp[key] = sum(raw[key][k] for k in raw[key])
			#print "key:", key
			#print "temp[key]", temp[key]
			#print ## 
		#print temp
		#prior[" "] = self._normalize(temp)
		#print "prior:"
		#self._print(prior)
		#print ##
		#return prior
		return self._normalize(temp)



	# returns conditional prob for every val in dict
	def _conditionalOn(self,joint):
		#print joint
		temp = []
		tot = sum(joint[key] for key in joint)
		return self._mult(joint, tot)



################################### hmm helper functions ############

	#multiplies mplier to every value in dict
	def _mult(self, d, mplier):
		#print "in mult: d:", d
		#print ####
		for key in d:
			#print "val:", d[key]
			#print "mplier:", mplier
			d[key] = d[key] * mplier
		#print "after mult: d:", d
		#print ####
		return d



	# normalize prob graph so that they all sum to one
	#def normalize(self,flist):
	def _normalize(self,d):
		#print "in normalize: d:", 
		#print sum(sum([d[k][key] for key in d[k]]) for k in d)
		tot = sum(d[key] for key in d)
		#print "in normalize: tot:", tot
		return self._mult(d, 1/tot)


	#adds n to every value in list
	def _addN(self,d,n):
		return [(item[0], item[1] + n) for item in d]



#################################### graph fxns #####################

	# build graph of conditional probs from joint list
	def _buildGraph(self,lst):
		#print lst
		grph = {}
		for item in lst:
			#print item[0][0]
			self._add(grph,item[0][0],item[0][1],item[1])
		return grph



	# read in frequency values from a text file into a list
	def _readFile(self, flName):
		#fd = open('bgTst.txt', 'r')
		fd = open(flName, 'r')
		#print fd
		#print fd.readline()
		lst = []
		for line in fd:
			#print line
			bits = string.split(line, ',')
			#print Decimal(bits[2].strip(' ')) + 1
			del(bits[-1])
			#print "bits:", bits
			#print ####
			for i in range(1,len(bits),2):
			    item = [(bits[0], bits[i]), Decimal(bits[i+1]) ]
			    #print item
			    lst.append(item)
		#print lst
		return lst



	def _add(self,bgrph,lett1,lett2,weight):
	    #print weight
	    #item = {weight:lett1,lett2}
	    if lett1 not in bgrph:
	        bgrph[lett1] = {lett2:weight}
	    elif lett2 not in bgrph[lett1]:
	        tmp = bgrph[lett1]
	        tmp[lett2] = weight
	        bgrph[lett1] = tmp



	def _adjacent(self,lett1, lett2):
	    return lett2 in self._bigrph[lett1]



	def _get_weight(self,lett1,lett2):
	    if self._adjacent(lett1,lett2):
	        tmp = self._bigrph[lett1]
	        return tmp[lett2]
	    else: return 0



	def _print(self,grph):
		for key in grph:
			#print key
			print "--", key, "--"
			for key2 in grph[key]:
				print key2, " : ", grph[key][key2]
			print "###############"
		print #



#################### no longer used ###################

	# read in frequency values from a text file and build dict with values
	if False:
	    def _buildGraph(self,fname,grph):
	        fd = open(fname, 'r')
	        for line in fd:
	            bits = string.split(line, ',')
	            del(bits[len(bits)-1])
	            for i in range(1,len(bits),2):
	                self._add(grph, bits[0], bits[i], Decimal(bits[i+1]))


	def _setSuggSymbList(self, lastTyped):
		#print "len of lastTyped:", len(str(lastTyped))
		if len(str(lastTyped)) == 1:
			self._topList = sorted(self._bigrph[lastTyped].items(), key=itemgetter(1), reverse=True)
			#print "self._topList:", self._topList
			#print "####################"



	def _nxtProb(self, lastTyped, lastSuggSymb):
		#print "lastTyped: ", lastTyped
		#print "lastSuggSymb:", lastSuggSymb
		if lastSuggSymb == '':  #nuthin suggested yet
			self._setSuggSymbList(lastTyped)
		elif self._topList == []:  #reached end of list
				return ''
		nxtSuggSymb = self._topList[0][0]
		del self._topList[0]
		return nxtSuggSymb	 