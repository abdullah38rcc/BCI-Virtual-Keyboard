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
		self._fname = "tgramsNoSpc.txt"
		self._tgraph = {}
		self._buildTgraph(self._fname)



	#builds trigram tree
	#args: filename
	def _buildTgraph(self,flname):
		print "in buildTgrams"
		tgrams = csv.reader(open(flname),delimiter='-')
		for row in tgrams:
			#print row
			row = self._cleanRow(row)
			#print row
			#print "-" * 10
			self._addToTree(row)
		for key in self._tgraph:
			self._normalize(self._tgraph[key])
		self._print(self._tgraph)
			


	def _addToTree(self, row):
		bgrm = row[0][0:2]
		lett = row[0][2]
		val = Decimal(row[1]) + 1				# +1 avoids zero vals
		#print "bgrm:", bgrm
		if bgrm not in self._tgraph.keys():
			temp = {lett:val}		
			self._tgraph[bgrm] = temp	
		else:
			self._tgraph[bgrm][lett] = val



	#strip off extra stuff read in from file
	#args: list containing one row read in
	#returns: ['trigram','freq']
	def _cleanRow(self,row):
		row[0] = row[0][0:-1]				#strip just the last xtra white-space off row[0]

		row[1] = row[1].strip(' ')			#strip all xtra white-space off row[1]
		row[1] = string.split(row[1],' ')
		row[1] = row[1][0]					#for tgramnospc
		#row = row[0:-1]					#strip end of row to get ['trigram','value']
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
		#print "in normalize: d:", 
		#print sum(sum([d[k][key] for key in d[k]]) for k in d)
		tot = sum(d[key] for key in d)
		#print "in normalize: tot:", tot
		return self._mult(d, 1/tot)



	def _print(self,grph):
		for key in grph:
			#print key
			print key, " : ", grph[key]
			print "-" * 10