#Touched 
class State:
	#def __init__(self,box1,box2,suggested,huff,bgrph,hilite,norm):
	#def __init__(self,box1,box2,currprobs,hiprob,usrchoice):
	def __init__(self,lasttyped,conditionals):
	#def __init__(self,ngrm,conditionals,trans,emiss,lastWrd,prefx,pos,top3):
		#self._box1 = list(box1)
		#self._box2 = list(box2)
		self._lasttyped = lasttyped
		self._conditionals = conditionals
		#self._currEmissProbs = emiss
		#self._currTrnsProbs = trans
		#self._currCondTree = conditionals
		#self._lastWord = lastWrd
		#self._ngram = ngrm
		#self._prefix = prefx
		#self._posinwrd = pos
		#self._top3 = top3
		#self._currprobs = currprobs
		#self._hiprob = hiprob
		#self._usrchoice = usrchoice
		#self._suggested = suggested
		#self._huff = huff
		#self._bgraph = list(bgrph)
		#self._highlighted = hilite
		#self._normal = norm
		
		#self._printContents()
		
	
	def _printContents(self):
		print "self._box1: ", self._box1
 		print "self._box2: ", self._box2
		print "self._suggested: ", self._suggested
		print "self._huff: ", self._huff
		print "self._bgraph: ", self._bgraph
		print "self._highlighted: ", self._highlighted
		print "self._normal: ", self._normal
		print #########################
