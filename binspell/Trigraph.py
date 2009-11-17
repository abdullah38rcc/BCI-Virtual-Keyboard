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
		self._delsEqlAvg()
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
			self._cleanAndAdd(row)
		#self._print(self._tgraph)

			


	#strip off extra stuff read in from file, and seperate into bigram, single letter, value, which is added to tgraph{}
	#args: list containing one row read in from file
	def _cleanAndAdd(self,row):
		bgram = row[0][0:2]
		lett = row[0][-1]

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
		self._tgraph[bgram][lett] = val




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
