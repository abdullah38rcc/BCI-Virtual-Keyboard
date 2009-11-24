# Bigraph class
# bug: left not choosing correctly

from operator import itemgetter


class Bigraph:
	
	def __init__(self):
		self._bigrph = {}
		self._suggSymbList = []
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
		
		self._buildGraph(self._bigrphLst)
		
		
		
	def _add(self,lett1,lett2,weight):
	    #print weight
	    #item = {weight:lett1,lett2}
	    if lett1 not in self._bigrph:
	        self._bigrph[lett1] = {lett2:weight}
	    elif lett2 not in self._bigrph[lett1]:
	        tmp = self._bigrph[lett1]
	        tmp[lett2] = weight
	        self._bigrph[lett1] = tmp
	    #print lett1, ':', self._bigrph[lett1]

	def _adjacent(self,lett1, lett2):
	    return lett2 in self._bigrph[lett1]

	def _get_weight(self,lett1,lett2):
	    if self._adjacent(lett1,lett2):
	        tmp = self._bigrph[lett1]
	        return tmp[lett2]
	    else: return 0

	def _buildGraph(self,lst):
	    for item in lst:
	        self._add(item[0],item[1],item[2])
	        #map(add,item)
	        #print item[0]


	def _nxtProb(self, lastTyped, suggSymb):
		#print "lastTyped: ", lastTyped
		#print "suggSymb:", suggSymb
		ordLst = sorted(self._bigrph[lastTyped].items(), key=itemgetter(1), reverse=True)
		flag = False
		for symb, freq in ordLst:
			#print symb 
			#print freq
			if suggSymb == '':  #nuthin suggested yet
				return symb
			if flag:
				#print symb
				return symb
			if suggSymb in symb:
				#print "suggSymb:", suggSymb
				#print "sym:", symb
				flag = True		#set flag cuz its the next in the ordered list
		return ''  #came to last item in list - now use huffman


if False:
	def _print():
		global bigrph
		for key in bigrph:
			#print key
			print key, " : ", bigrph[key]
			print "###############"