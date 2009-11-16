#trigraph class
# last edit: 11/12
################CHANGES############
# 
##########TODO##############
# 
######################BUGS#######################
# 
##############CURRENTLY WORKING ON##########
# 

from operator import itemgetter
import string
from decimal import Decimal
import csv

class Trigraph:
	def __init__(self):
		self._f1name = "tgramsNoSpc.txt"
		self._f2name = "trgramsWithSpc.txt"
		self._tgraph = {}
		self._start()
		



	def _start(self):
		#self._buildTgraph(self._f1name)
		self._initTgraph()
		self._addf1Data(self._f1name)
		self._addf2Data(self._f2name)
		
		for key in self._tgraph:
			self._normalize(self._tgraph[key])
		#self._print(self._tgraph)
		#print self._tgraph.keys()



	#generate all possible trigrams and assign frequncy of 1 to each
	def _initTgraph(self):
		alphabet = map(chr,range(97,123))
		alphabet.append('[SPC]')
		alphabet.append('[DEL]')
		for symb1 in alphabet:
			for symb2 in alphabet:
				temp = {}
				for symb3 in alphabet:
					temp[symb3] = 1
				self._tgraph[symb1+symb2] = temp
		#self._print(self._tgraph)



	#adds datat from file 1 to tree
	#args: filename
	def _addf1Data(self,flname):
		tgrams = csv.reader(open(flname),delimiter='-')
		for row in tgrams:
			#print row
			row = self._cleanRow1(row)
			self._addToTree(row)
		#self._print(self._tgraph)



	#adds data from file 2 to tree
	#args: filename
	def _addf2Data(self,flname):
		tgrams = csv.reader(open(flname),delimiter='-')
		for row in tgrams:
			#print row
			row = self._cleanRow2(row)
			self._addToTree(row)
		#self._print(self._tgraph)
			


	def _addToTree(self, row):
		bgrm = row[0][0:2]
		lett = row[0][2]
		val = Decimal(row[1]) + 1				# +1 avoids zero vals
		#print "bgrm:", bgrm
		if bgrm in self._tgraph.keys():
			self._tgraph[bgrm][lett] = val



	#for trigrams no space
	#strip off extra stuff read in from file
	#args: list containing one row read in
	#returns: ['trigram','freq']
	def _cleanRow1(self,row):
		#print "row:", row
		#print #
		row[0] = row[0][0:-1]				#strip just the last xtra white-space off row[0]
		row[0] = row[0].lower()
		row[1] = row[1].strip(' ')			#strip all xtra white-space off row[1]
		row[1] = string.split(row[1],' ')
		row[1] = row[1][0]					#for tgramnospc
		#row = row[0:-1]					#strip end of row to get ['trigram','value']
		#print "row:", row
		#print #
		return row



	#for trigrams with space
	#strip off extra stuff read in from file
	#args: list containing one row read in
	#returns: ['trigram','freq']
	def _cleanRow2(self,row):
		#print "row:", row
		#print #
		row[0] = row[0][0:-1]				#strip just the last xtra white-space off row[0]
		row[0] = row[0].lower()

		#replace whitespace with [SPC]
		x = row[0].find(' ')
		if x>=0:
			y = list(row[0])
			y[x] = '[SPC]'
			row[0] = ''.join(y)

		#for cases with single letter surrounded by whitespace
		x = row[0].find(' ')
		if x>=0:
			y = list(row[0])
			y[x] = '[SPC]'
			row[0] = ''.join(y)


		row[1] = row[1].strip(' ')			#strip all xtra white-space off row[1]
		row[1] = string.split(row[1],' ')
		row[1] = row[1][0]				
		row = row[0:-1]					#strip end of row to get ['trigram','value']
		#print "row:", row
		#print #
		return row



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



	# returns normalized prob graph
	# args: dict{lett: val}
	def _normalize(self,d):
		#print "in normalize: d:", d
		#print #
		#print sum(sum([d[k][key] for key in d[k]]) for k in d)
		tot = sum(d[key] for key in d)
		#print "in normalize: tot:", tot
		#print "1/tot", 1/tot
		mplier = Decimal(1) / Decimal(tot)
		return self._mult(d, mplier)



	def _print(self,grph):
		for key in grph:
			#print key
			print key, " : ", grph[key]
			print "-" * 10
