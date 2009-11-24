# bigraph class
# last edit: 7/11
################CHANGES############
# completed prob tables
##########TODO##############
# change variable and method names to be more clear
######################BUGS#######################
# dict values are totally off - see buildgrph()
##############CURRENTLY WORKING ON##########
#

from operator import itemgetter
import string
from decimal import Decimal



class Bigraph:
	def __init__(self):
		self._joint1 = []					#list of bigram joint probs for beginning of word
		self._cond1 = {}					#dict of bigram conditional probs for beginnning of word
		self._cond1List = []				#list of same
		self._cond2 = {}					#dict of bigram conditional probs for any other place in a word
		self._cond2List = []				#list of same

		self._bigrph2 = {}
		self._suggSymbList = []
		self._f1name = 'bgramFreq1.txt'
		self._f2name = 'bgramFreq2.txt'
		#self._bigrphLst = self._readFile()
		self._start()

		if False:
			self._bigrphLst = [
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



	def _start(self):
		val = 1
		lst = self._readFile(self._f1name)
		#print lst
		lst = self._addN(lst,val)  #get rid of all zeros
		self._joint1 = self._normalize(lst)
		#print self._joint1
		#self.cond1 = self._conditionalOn(self._joint1)
		self._buildGraph(self._joint1, self._cond1)
		#self._print(self._cond1)


	# returns joint
	def _conditionalOn(self,joint):
		#print joint
		tot = sum(joint[k] for k in joint)
		for k in joint:
			joint[k] = joint[k] * tot
		#print joint
		return joint


	#multiplies mplier to every value in d
	def _mult(self, d, mplier):
		temp = []
		##### why doesn't this work???????
		###### why do i need temp?
		for item in d:
			#print item
			#item[2] = item[2] * mplier
			item = (item[0], item[1], item[2]*mplier)
			temp.append(item)
			#print item
			#print #####
		#print temp
		return temp
		#return list( [(item[0], item[1], item[2]*tot)] for every item in d )



	# normalize so that they all sum to one
	#def normalize(self,flist):
	def _normalize(self,d):
		#print sum(sum([d[k][key] for key in d[k]]) for k in d)
		tot = sum(item[2] for item in d)
		return self._mult(d, Decimal('1')/tot)


	#adds n to every value in dict d
	def _addN(self,d,n):
		return [(item[0], item[1], item[2] + n) for item in d]




	# build graph of conditional probs from joint list
	def _buildGraph(self,lst,grph):
		for item in lst:
			self._add(grph,item[0],item[1],item[2])
		for key in grph:
			grph[key] = self._conditionalOn(grph[key])
			#map(add,item)
			#print item[0]
        
        
        
        
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
			#print bits
			#print ####
			for i in range(1,len(bits),2):
			    item = [bits[0], bits[i], Decimal(bits[i+1]) ]
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



	## no longer used
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
			self._suggSymbList = sorted(self._bigrph[lastTyped].items(), key=itemgetter(1), reverse=True)
			#print "self._suggSymbList:", self._suggSymbList
			#print "####################"



	def _nxtProb(self, lastTyped, lastSuggSymb):
		#print "lastTyped: ", lastTyped
		#print "lastSuggSymb:", lastSuggSymb
		if lastSuggSymb == '':  #nuthin suggested yet
			self._setSuggSymbList(lastTyped)
		elif self._suggSymbList == []:  #reached end of list
				return ''
		nxtSuggSymb = self._suggSymbList[0][0]
		del self._suggSymbList[0]
		return nxtSuggSymb	 


	def _print(self,grph):
		for key in grph:
			#print key
			print key, " : ", grph[key]
			print "###############"