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
		#self._bifname = "wordBgrams.txt"
		self._bifname = "testwords.txt"
		self._cleanBgrmFile = "cleanWordBgrams.txt"
		self._alphabet = []
		self._singleLettWrds = ['a','i']	#acceptable single letter words
		self._unigrams = {}
		self._bigrams = {}
		self._start()
		



	def _start(self):
		self._alphabet = map(chr,range(97,123))
		self._buildUniDict()
		self._buildBiDict()
		self._writeCleanBgmFile()
		#for key in self._tgraph:
			#self._normalize(self._tgraph[key])
		#self._print(self._bigrams)




	#reads in bigramfile and sends rows of data to be cleaned and added unigram dict
	def _buildBiDict(self):
		tgrams = csv.reader(open(self._bifname),delimiter=' ')
		for row in tgrams:
			#print row
			self._cleanAddBi(row)
		#self._print(self._tgraph)




	#strip off extra stuff read in from file, and seperate into word1,word2,count and add to bigram dict
	#args: list containing one row read in from file
	def _cleanAddBi(self,row):
		#print row
		word1 = row[0].strip(' ')
		word2 = row[1].strip(' ')
		val = row[2].strip(' ')
		wrds = [word1,word2]

		for w in wrds:
			if w[0].isdigit():
				return
			while w[0] not in self._alphabet:
				#print "old word:",word
				w = w.strip(w[0])
				#print "new word:", word
				#print #

			while w[-1] not in self._alphabet:
				#print "old word:",word
				w = w.strip(w[-1])
				#print "new word:", word
				#print #
			if len(w)==1 and w not in self._singleLettWrds:
				#print word
				return

		temp = {wrds[1]:float(val)}
		if wrds[0] in self._bigrams.keys():
			#print "in if"
			self._bigrams[wrds[0]].update(temp)
		else:
			#print "in else"
			self._bigrams[wrds[0]] = temp





	#reads in unigramfile and sends rows of data to be cleaned and added unigram dict
	def _buildUniDict(self):
		tgrams = csv.reader(open(self._unifname),delimiter=' ')
		for row in tgrams:
			#print row
			self._cleanAddUni(row)
		#self._print(self._tgraph)

			


	#strip off extra stuff read in from file, and seperate into word,count and add to unigram dict
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




	#write bigram dictionary to a file for easier future reading
	#writing -- word1,word2-1,val,word2-2,val,etc
	def _writeCleanBgmFile(self):
		fd = open(self._cleanBgrmFile,'w')
		kys = self._bigrams.keys()
		for k in kys:
			string = k + ','
			fd.write(string)
			for key in self._bigrams[k]:
				string = key + ',' + str(self._bigrams[k][key]) + ','
				fd.write(string)
			fd.write('\n')
		fd.close



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




	def _print(self,grph):
		for key in grph:
			#print key
			print key, " : ", grph[key]
			print "-" * 10
