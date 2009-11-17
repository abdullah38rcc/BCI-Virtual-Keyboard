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
		#self._f1name = "tgramsNoSpc.txt"
		#self._f2name = "trgramsWithSpc.txt"
		self._fname = "trigrams.txt"
		self._alphabet = []			#for building tgraph
		self._tgraph = {}
		self._start()
		



	def _start(self):
		#self._buildTgraph(self._f1name)
		self._initTgraph()
		#self._addf1Data(self._f1name)
		#self._addf2Data(self._f2name)
		self._addData(self._fname)
		
		for key in self._tgraph:
			self._normalize(self._tgraph[key])
		#self._print(self._tgraph)
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
	def _addData(self,flname):
		tgrams = csv.reader(open(flname),delimiter=',')
		for row in tgrams:
			#print row
			#row = self._cleanRow(row)
			self._cleanAndAdd(row)
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



	#reads in file, cleans up data and adds data to tree
	#args: filename
	def _addf2Data(self,flname):
		tgrams = csv.reader(open(flname),delimiter='-')
		for row in tgrams:
			#print row
			row = self._cleanRow2(row)
			self._addToTree(row)
		#self._print(self._tgraph)
			


	#adds row of data to tree
	#args: list containing properly formatted data [trigram,valS]
	def _addToTree(self, row):
		#print "row:", row
		#print "-" * 10

		if '[' in row[0][0] or '[' in row[0][1]:
			bgrm = row[0][0:6]
			lett = row[0][6:len(row[0])]
		elif ']' in row[0][-1]:
			x = row[0].find('[')
			bgrm = row[0][0:x]
			lett = row[0][x:len(row[0])]	
		else:
			bgrm = row[0][0:2]
			lett = row[0][-1]

		#print "bigram:", bgrm
		#print "lett:",lett
		#print #		

		val = float(row[1]) + 1				# +1 avoids zero vals
		#print "bgrm:", bgrm
		if bgrm in self._tgraph.keys() and lett in self._alphabet:
			self._tgraph[bgrm][lett] = val
		else:
			print "not in tree bgram: ", bgrm
			print "lett:",lett
			print #




	#strip off extra stuff read in from file
	#args: list containing one row read in
	#returns: ['trigram','freq']
	def _cleanAndAdd(self,row):
		#print "row:", row
		#print #
		bgram = row[0][0:2]
		lett = row[0][-1]
		#print "orig bgram:",bgram
		#replace whitespace with [SPC]
		x = bgram.find(' ')
		while x >= 0:
			#print 'x', x >= 0
			y = list(bgram)
			y[x] = '[SPC]'
			bgram = ''.join(y)
			x = bgram.find(' ')

		x = lett.find(' ')
		if x == 0:
			lett = '[SPC]'
		#print "new bgram", bgram
		#print "lett:",lett


		row[1] = row[1].strip(' ')			#strip all xtra white-space off row[1]
		val = float(row[1])			
		#print "val:", val
		#print #
		self._tgraph[bgram][lett] = val






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
		mplier = float(1) / float(tot)
		return self._mult(d, mplier)



	def _print(self,grph):
		for key in grph:
			#print key
			print key, " : ", grph[key]
			print "-" * 10
