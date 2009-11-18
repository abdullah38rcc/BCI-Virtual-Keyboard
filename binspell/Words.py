# words class
# last edit: 11/117
################CHANGES############
# 
##########TODO##############
# 
######################BUGS#######################
#
##############CURRENTLY WORKING ON##########
#


import string
import csv

class Words:
	def __init__(self):
		self._unifname = "written-lexicon.txt"
		self._alphabet = []
		self._singleLettWrds = ['a','i']	#acceptable single letter words
		self._unigrams = {}
		self._bigrams = {}
		self._start()
		



	def _start(self):
		self._alphabet = map(chr,range(97,123))
		self._buildUniDict()
		#for key in self._tgraph:
			#self._normalize(self._tgraph[key])
		self._print(self._unigrams)
		#print self._tgraph.keys()



	#generate all possible trigrams and assign frequncy of 1 to each
	def _initTgraph(self):
		self._alphabet = map(chr,range(97,123))
		self._alphabet.append('[SPC]')
		self._alphabet.append('[DEL]')
		for symb1 in self._alphabet:
			for symb2 in self._alphabet:
				temp = {}
				for symb3 in self._alphabet:
					temp[symb3] = 1
				self._tgraph[symb1+symb2] = temp
		#self._print(self._tgraph)



	#reads in file, cleans up data and adds data to tree
	#args: filename
	def _buildUniDict(self):
		tgrams = csv.reader(open(self._unifname),delimiter=' ')
		for row in tgrams:
			#print row
			self._cleanAddUni(row)
		#self._print(self._tgraph)

			


	#strip off extra stuff read in from file, and seperate into word, count and add to unigram dict
	#args: list containing one row read in from file
	def _cleanAddUni(self,row):
		word = row[0]
		val = row[1].strip(' ')
		if word[0].isdigit():
			return
		while word[0] not in self._alphabet:
			#print "old word:",word
			word = word.strip(word[0])
			#print "new word:", word
			#print #

		while word[-1] not in self._alphabet:
			#print "old word:",word
			word = word.strip(word[-1])
			#print "new word:", word
			#print #
		if len(word)==1 and word not in self._singleLettWrds:
			#print word
			return
		
		self._unigrams[word] = float(val)




	#multiplies mplier to every value in dict
	#args: dictionary{letter,val}
	#returns: dictionary{letter,val*mplier}
	def _mult(self, d, mplier):
		for key in d:
			d[key] = d[key] * mplier
		return d



	# returns normalized prob graph
	# args: dict{lett: val}
	def _normalize(self,d):
		#print "in normalize: d:", d
		#print #
		#print sum(sum([d[k][key] for key in d[k]]) for k in d)
		tot = sum(d[key] for key in d)
		#print "in normalize: tot:", tot
		#print "1/tot", 1/tot
		mplier = float(1) / float(tot)
		return self._mult(d, mplier)



	# assign each '[del]' average of all values in the dict its in
	def _delsEqlAvg(self):
		for key in self._tgraph:
			if '[DEL]' not in key and '[DEL]' in self._tgraph[key].keys():
				#print key
				vals = self._tgraph[key].values()
				self._tgraph[key]['[DEL]'] = sum(vals,0.0) / len(vals)
				#print self._tgraph[key]['DEL']
				



	def _print(self,grph):
		for key in grph:
			#print key
			print key, " : ", grph[key]
			print "-" * 10
