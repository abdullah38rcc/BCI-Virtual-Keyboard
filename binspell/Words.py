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
from difflib import *
import cPickle as pickle
from operator import itemgetter

class Words:
	def __init__(self):
		self._unifname = "written-lexicon.txt"			#file containing word unigrams and their freqs
		self._bifname = "wordBgrams.txt"			#file containing word bigrams and their freqs
		#self._bifname = "testwords.txt"				#test file
		self._bdictFile = "bgramPickle.txt"			#file containg pickled bigram dict
		self._udictFile = "ugramPickle.txt"			#file containg pickled unigram dict
		self._alphabet = []
		self._singleLettWrds = ['a','i']			#acceptable single letter words
		self._unigrams = {}
		self._bigrams = {}

		self._start()
		



	def _start(self):
		self._alphabet = map(chr,range(97,123))
		#self._buildUniDict()
		#self._buildBiDict()
		self._unpickleUni()
		self._unpickleBi()
		#self._print(self._bigrams)



	#read pickle string into unigram dict
	def _unpickleUni(self):
		fd = open(self._udictFile,'r')
		self._unigrams = pickle.load(fd)
		#self._print(self._unigrams)



	#read pickle string into bigram dict
	def _unpickleBi(self):
		fd = open(self._bdictFile,'r')
		self._bigrams = pickle.load(fd)
		#self._print(self._bigrams)



	#returns dict of top 3 words predicted
	#args: ngram string of letters, last full word typed
	def _closestWords(self,ngram,lastwrd):
		#get_close_matches(word, possibilities[, n][, cutoff])
		#n= max num to return (default-3), cutoff=num b/t 0-1, if not at least this num, ignore (default-.6)
		print "in closest words"
		matches = {}
		top3 = []

		if lastwrd != '' and lastwrd in self._bigrams.keys():
			temp = self._bigrams[lastwrd]
			for word in temp:
				if word.startswith(ngram):
					matches[word] = temp[word]

		if len(matches.keys()) < 3:
			for word in self._unigrams:
				if word.startswith(ngram):
					matches[word] = self._unigrams[word]
		self._normalize(matches)
		
		srtMatch = self._sortByValue(matches)
		#for i,(word,prob) in enumerate(srtMatch):
			#print "%d: %s   with prob %3.3f" % (i, word, prob)
			#if i > 8: break
		top3 = dict(srtMatch[0:3])
		return top3
		#self._print(top3)
			


	#args: unsorted dictionary
	#returns list of dict items sorted from greatest to least
	def _sortByValue(self, unsrtdDict):
		#print "dict:", unsrtdDict
		#print ###
		items = unsrtdDict.items()
		#print "items:", items
		items.sort(key = itemgetter(1), reverse=True)
		return items




	#reads in bigramfile and sends rows of data to be cleaned and added unigram dict
	def _buildBiDict(self):
		tgrams = csv.reader(open(self._bifname),delimiter=' ')
		for row in tgrams:
			#print row
			self._cleanAddBi(row)
		for key in self._bigrams:
			self._normalize(self._bigrams[key])
		fd = open(self._bdictFile,'w')
		pickle.dump(self._bigrams,fd)
		#self._print(self._bigrams)




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
		ugrams = csv.reader(open(self._unifname),delimiter=' ')
		for row in ugrams:
			#print row
			self._cleanAddUni(row)
		self._normalize(self._unigrams)
		fd = open(self._udictFile,'w')
		pickle.dump(self._unigrams,fd)
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

		#check for repeats	
		if word in self._unigrams.keys():
			self._unigrams[word] += float(val)
		else:
			self._unigrams[word] = float(val)
		
		#print "word:",word
		#print "val:", self._unigrams[word]
		#print "-"*10





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
		#print "in normalize: d:"
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
