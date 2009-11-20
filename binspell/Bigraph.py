# bigraph class
# last edit: 10/15
################CHANGES############
# _buildEmission()
# _updateEmission()
##########TODO##############
# change variable and method names to be more clear
######################BUGS#######################
#
##############CURRENTLY WORKING ON##########
#

from operator import itemgetter
import string




class Bigraph:

	def __init__(self):
		self._joint1 = {}					# list of bigram joint probs for beginning of word: [(char1,char2),prob]
		self._conditional1 = {}				# dict of bigram conditional probs for beginnning of word
		self._prior = {}					# start of program
		self._prior2 = {}					# when sumthins already been typed

		self._joint2 = {}					# list of bigram joint probs for other positions in word
		self._conditional2 = {}				# dict of bigram conditional probs for other positions in word

		self._emissionProbs = {}					# emission prob dict: [char,prob]

		self._topList = []					# list of top 3 most next most probable letters
		self._f1name = 'bgramFreq1.txt'
		self._f2name = 'bgramFreq2.txt'
		self._f3name = 'bgramFreq3.txt'

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
		#self._print(self._conditional1)

		freqs = self._bigrphLst
		freqs = self._addN(freqs,val)  #get rid of all zeros
		temp = self._normalize(dict(freqs))
		freqs = list((key,temp[key]) for key in temp)  #flatten out dict to pass to graph
		self._joint2 = self._buildGraph(freqs)
		#self._print(self._joint2)
		for key in self._joint2:	#build graph of conditional probs
			self._conditional2[key] =  self._conditionalOn(self._joint2[key])
		#self._print(self._conditional2)



	def _start(self):
		val = 1	#flatten out distribution
		freqs1 = self._readFile(self._f1name)
		freqs2 = self._readFile(self._f2name)
		freqs3 = self._readFile(self._f3name)

		freqs1 = self._addN(freqs1,val)  #get rid of all zeros
		freqs2 = self._addN(freqs2,val)
		freqs3 = self._addN(freqs3,val)

		######### HACK #############
		#add [SPC] and [DEL] to both tables of frequency
		alphabet = map(chr,range(97,123))
		for lett in alphabet:
			sCount = float(2)
			dCount = float(30)
			freqs1.append(((lett,'[SPC]'),sCount))
			freqs1.append(((lett,'[DEL]'),dCount))
			freqs2.append(((lett,'[SPC]'),sCount))
			freqs2.append(((lett,'[DEL]'),dCount))
			#print "in Bigraph: freqs1: ", freqs1
			#print "sCount: ", sCount

		self._joint1 = self._buildGraph(freqs1)						#self._joint1{'a':{'a':prob,'b':prob,etc..}}		
		self._prior = self._getPrior()							#calculate prior
		#print "prior:"
		#print self._prior

		#build 1st table of conditionals
		self._conditional1 = self._joint1
		self._conditional1['[SPC]'] = self._prior
		for key in self._conditional1:
			self._conditional1[key] = self._normalize(self._conditional1[key])	#prob of alphabet given any letter = 1

		self._joint2 = self._buildGraph(freqs2)						#self._joint2{'a':{'a':prob,'b':prob,etc..}}		

		#build 2nd table of conditionals
		for key in self._joint2:
			self._conditional2[key] = self._normalize(self._joint2[key])
		



################################## hmm #######################

	def _buildEmission(self, chosen, notChosen):
		alphabet = map(chr,range(97,123))
		grph = {}
		for item in alphabet:
			for lett in alphabet:
				if item == lett:
					prob = float(0.8)
				else:
					prob = float(0.2/25)
				self._add(grph,item,lett,prob)
		return grph


	#returns dict of prior probs
	def _getPrior(self):
		prior = {}
		#print "in prior: joint1: "
		#self._print(self._joint1)
		for key in self._joint1:
			prior[key] = sum(self._joint1[key][k] for k in self._joint1[key])
		#print "prior b4 normalize:"
		#self._print(prior)
		return self._normalize(prior)



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



	# normalize so that they all sum to one
	# args: dict{'lett':val}
	def _normalize(self,d):
		#print "in normalize: d:",
		#print sum(sum([d[k][key] for key in d[k]]) for k in d)
		tot = sum(d[key] for key in d)
		#print "in normalize: tot:", tot
		mplier = float(1) / float(tot)
		return self._mult(d, mplier)


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
			#print float(bits[2].strip(' ')) + 1
			del(bits[-1])
			#print "bits:", bits
			#print ####
			for i in range(1,len(bits),2):
			    item = [(bits[0], bits[i]), float(bits[i+1]) ]
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



	def _print(self,grph):
		for key in grph:
			#print key
			print key, " : ", grph[key]
			print "-" * 10

