# global variable class
from operator import itemgetter
from decimal import Decimal



class GlobalVariables:
	def __init__(self):
		self._highlighted = 0
		self._circleList = []
		self._canvas = 0
		self._txtBox = 0
		self._canHt = 0				#canvas height
		self._canWdth = 0			#canvas width

		self._numSteps = 0			#number of choices made to select a letter
		self._numErrors = 0			#number of classifier errors during selection of a letter
		self._ttlNumSteps = 0		#total number of choices made
		self._ttlNumErr = 0			#total number of classifier errors

		self._charNum = 0			#number of characters typed b4 a space
		self._numTimesLargest = 0	#number of times largest chosen consecutively
		#self._currSymbList = []

		self._huffTree = []						#huffman tree of conditional probs
		self._hiProb = ['',0]					#[most probable symbol, prob]
		self._currProbs = {}					#{symbols:current probilities}
		self._currCondTree = {}					#current bigram conditional tree being referenced (for saving state purpose)

		self._classAcc = Decimal('0.8')			#classifier accuracy
		self._threshold = Decimal('0.9')		#threshold 
		self._diffThreshold = Decimal('0.3')	#difference threshold
		self._trialLen = 3						#trial length
		#self._nxtProb = 0

		self._suggested = ''
		self._huffSuggest = ''
		self._lastTyped = ' '				#assume start with a space



	#returns dict{key:value} as dict{value:key}
	def _swap_dictionary(self, original_dict):
		tmp = [(v, k) for (k, v) in original_dict.iteritems()]
		#print dict(tmp)['a']
		#return dict([(v, k) for (k, v) in original_dict.iteritems()])
		return dict(tmp)



	#args: unsorted dictionary
	#returns dictionary as list:[(lett1,prob1),...], sorted from greatest to least
	def _sortByValue(self, unsrtdDict):
		#print "dict:", unsrtdDict
		#print ###
		items = unsrtdDict.items()
		#print "items:", items
		items.sort(key = itemgetter(1), reverse=True)
		return items



	#print formatted contents of dict
	def _printDict(self,dictn):
		if dictn != {}:
			for key in dictn:
				print key,': ', dictn[key]
			#print dictn['a']