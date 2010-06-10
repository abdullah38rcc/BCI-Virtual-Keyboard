#! usr/bin/python

from heapq import *
from TstClass import *
from GlobalVariables import *
from stoplight import *

#why doesn't this work?
#import TstClass

if False:
	def test_for():
		print "in test_for"
		d = {'one':1, 'two':2}
		if False:
			for i in range(1, 5):
				print i
			else:
				print 'The for loop is over'
			for element in [1, 2, 3]:
			    print element
			for element in (1, 2, 3):
			    print element
			for char in "123":
			    print char
			for line in open("myfile.txt"):
			    print line
	
			for key in {'one':1, 'two':2}:
			    print key
	
		for value in d.values():
			print key 
		
		#for k,v in d.iteritems()  #only in python 2.6
			#print k,v
		
def test_heap():
	heap = []
	data = [(1, 'J'), (4, 'N'), (3, 'H'), (2, 'O')]
	for item in data:
	     heappush(heap, item)
	
	while heap:
	     print heappop(heap)[1]
	

def swap_dictionary(original_dict):
	return dict([(v, k) for (k, v) in original_dict.iteritems()])
	

#test_for()

if False:
	#test_heap()
	d = {"server":"mpilgrim", "database":"master"}

	tst = TstClass(4,'a')
	tst.x = 5
	tst.newVar = tst.lst
	tst.newVar = ['h','e','l','p']
	alphabet = map(chr,range(97,123))
	print 'tst.lst:',tst.lst
	print 'tst.newVar:',tst.newVar
	print 'tst.y:',tst.y
	print 'tst.callFxn:',tst.callFxn()	


#gv = GlobalVariables()
#print gv._canvas
	

#test stoplight class
timing = [5,2,1]
tstSL = Stoplight(timing)