# global variables class

# GlobalVariables class
# last edit: 7/28
################CHANGES############
# changed variables
# added self._huffTree
##########TODO##############
#
######################BUGS#######################
#
##############CURRENTLY WORKING ON##########
#


from operator import itemgetter
from decimal import Decimal

class GlobalVariables:
	def __init__(self):
		self._highlighted = 0
		self._box1 = []				#symbol contents of left box
		self._box2 = []				#symbol contents of right box
		self._canvas = 0
		self._txtBox = 0
		self._canHt = 0				#canvas height
		self._canWdth = 0			#canvas width

		self._numSteps = 0			#number of choices made to select a letter
		self._numErrors = 0			#number of classifier errors during selection of a letter
		self._ttlNumSteps = 0		#total number of choices made
		self._ttlNumErr = 0			#total number of classifier errors
		self._numDels = 0			#number of times delete was used

		self._posInWrd = 0			#number of characters typed b4 a space
		self._numTyped = 0			#number of characters typed in total (including [del] and [spc])
		self._numTimesLargest = 0	#number of times largest chosen consecutively
		self._obsOut = []			#list of symbols typed thus far
		self._numB4Shuffle	= 0		#for shuffle_alternate()
		#self._currSymbList = []

		self._delta = {}			#viterbi: [key]{symb,prob}: prob of path ending at time [key] in state 'symb'
		self._psi = {}				#viterbi: argmax_i
		self._qStar = ''			#viterbi: most probable path

		self._huffTree = []			#huffman tree of conditional probs
		self._hiProb = ['',0]			#[most probable symbol, prob]
		self._currProbs = {}			#{symbols:current probilities}
		self._currCondTable = {}		#current bigram conditional tree being referenced (for saving state purpose)

		self._transitionProbs = {}
		self._emissionProbs = {}

		self._classAcc = float(0.8)		#classifier accuracy
		self._threshold = float(0.80)		#threshold
		self._diffThreshold = float(0.3)	#difference threshold
		self._trialLen = 3			#trial length
		self._startTime = 0			#for testing itr for simulation
		#self._nxtProb = 0

		self._suggested = ''
		self._huffSuggest = ''
		self._lastTyped = '[SPC]'		#assume start with a space
		self._ngram = '[SPC]'			#last letter ngram typed, assume start with a space, used for indexing into letter cond tables
		self._lastWordTyped = ''
		self._prefix = ''
		self._top3words = {}			#top 3 words returned from word class based on what's been typed

		self._symbolFreqList = [
			(0.124167  , 'e'),
		   (0.0969225 , 't'),
		   (0.0820011 , 'a'),
		   (0.0768052 , 'i'),
		   (0.0764055 , 'n'),
		   (0.0714095 , 'o'),
		   (0.0706768 , 's'),
		   (0.0668132 , 'r'),
		   (0.0448308 , 'l'),
		   (0.0363709 , 'd'),
		   (0.0350386 , 'h'),
		   (0.0344391 , 'c'),
		   (0.028777  , 'u'),
		   (0.0281775 , 'm'),
		   (0.0235145 , 'f'),
		   (0.0203171 , 'p'),
		   (0.0189182 , 'y'),
		   (0.0181188 , 'g'),
		   (0.0135225 , 'w'),
		   (0.0124567 , 'v'),
		   (0.0106581 , 'b'),
		   (0.00393019, 'k'),
		   (0.00219824, 'x'),
		   (0.0019984 , 'j'),
		   (0.0009325 , 'q'),
		   (0.000599  , 'z')
		]
		#self._symbolFreqDict = dict(self._symbolFreqList)
		#self._srtdSynbFreqLst = self.sortByValue(self._symbolFreqDict)
		#self._swappdSymbFreqDict = self.swap_dictionary(self._symbolFreqDict)

		#self.printDict(self._swappdSymbFreqDict)



	#returns dict{key:value} as dict{value:key}
	def _swap_dictionary(self, original_dict):
		tmp = [(v, k) for (k, v) in original_dict.iteritems()]
		#print dict(tmp)['a']
		#return dict([(v, k) for (k, v) in original_dict.iteritems()])
		return dict(tmp)




	#args: unsorted dictionary
	#returns list of dict items sorted from greatest to least : [(key,val),(key,val),etc]
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



	#for testing
	if False:
		self._symbolFreqList = [
			(8  , 'e'),
			(6 , 't'),
			(5 , 'a'),
			(2 , 'i'),
		]
		self._symbolFreqList = [
		(0.144167, 'SPC'),
		(0.134167, 'DEL'),
			(0.124167  , 'e'),
		   (0.0969225 , 't'),
		   (0.0820011 , 'a'),
		   (0.0768052 , 'i'),
		   (0.0764055 , 'n'),
		   (0.0714095 , 'o'),
		   (0.0706768 , 's'),
		   (0.0668132 , 'r'),
		   (0.0448308 , 'l'),
		   (0.0363709 , 'd'),
		   (0.0350386 , 'h'),
		   (0.0344391 , 'c'),
		   (0.028777  , 'u'),
		   (0.0281775 , 'm'),
		   (0.0235145 , 'f'),
		   (0.0203171 , 'p'),
		   (0.0189182 , 'y'),
		   (0.0181188 , 'g'),
		   (0.0135225 , 'w'),
		   (0.0124567 , 'v'),
		   (0.0106581 , 'b'),
		   (0.00393019, 'k'),
		   (0.00219824, 'x'),
		   (0.0019984 , 'j'),
		   (0.0009325 , 'q'),
		   (0.000599  , 'z')
		]
