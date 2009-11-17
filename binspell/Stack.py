class Stack:
	def __init__(self):
		self._stackList = []
	
	def _push(self,item):
		#itemCpy = deepcopy(item)
		self._stackList.append(item)
		##print "stack after append = ", stack

	def _pop(self):
		#print "in pop()"

		if self._stackList != []:
			s = self._stackList.pop()
		##print s," has been popped"
			return s
		#return self._stackList.pop()
	