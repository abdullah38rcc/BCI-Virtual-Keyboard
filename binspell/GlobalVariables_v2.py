# global variables class
# added space and delete

from operator import itemgetter

class GlobalVariables_v2:
	def __init__(self):
		#self._highlighted = 0
		self._box1Freqs = []
		self._box2Freqs = []
		self._canvas = 0
		self._txtBox = 0
		self._currSymbList = []
		self._nxtProb = 0
		self._suggested = ''
		self._huffSuggest = ''
		self._canHt = 0
		self._canWdth = 0
		self._lastTyped = ''
		self._symbolFreqList = [
			(0.144167, '[SPC]'),
			(0.134167, '[DEL]'),
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
		self._symbolFreqDict = dict(self._symbolFreqList)
		self._srtdSynbFreqLst = self.sortByValue(self._symbolFreqDict)
		self._swappdSymbFreqDict = self.swap_dictionary(self._symbolFreqDict)
		self._stateStack = []
		
		#self.printDict(self._swappdSymbFreqDict)
		
	def swap_dictionary(self, original_dict):
		tmp = [(v, k) for (k, v) in original_dict.iteritems()]
		#print dict(tmp)['a']
		#return dict([(v, k) for (k, v) in original_dict.iteritems()])
		return dict(tmp)
	

	def sortByValue(self, unsrtdDict):
		items = unsrtdDict.items()
		return items.sort(key = itemgetter(1), reverse=True)
		
	
	def printDict(self,dictn):
		if dictn != {}:
			for key in dictn:
				print key,': ', dictn[key]
			#print dictn['a']

	if False:
		self._symbolFreqList = [
			(8  , 'e'),   
			(6 , 't'),   
			(5 , 'a'),   
			(2 , 'i'),   
		]
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
