"""
script that takes a file containing a number of tags words (one per line) and sorts them by the number of times they 
occur in the file (descending order), but exclude words that only occur once. Ignore the case of the words, and 
filter out any puncutation characters. The output should be the word, followed by a space and the number of times 
it occurs in the file.
"""

import string
from operator import itemgetter

def readFile(flname):
	fd = open(flname, 'r')
	return fd

def getWords(flhandle):
	wrdsncnt = {}
	punct = string.punctuation
	for line in flhandle:
		tmp_lst = list(line)
		for indx, ch in enumerate(tmp_lst):
			if ch in punct:
				#print ch
				del(tmp_lst[indx])
		word = ''.join(tmp_lst)
		word = word.lower()
		wrdsncnt = addtoDict(word,wrdsncnt)
	return wrdsncnt

def addtoDict(wrd,dictn):
	if wrd in dictn.keys():
		dictn[wrd] +=1
	else:
		dictn[wrd] = 1
	return dictn

def printAns(wcdict):
	print wcdict
	for key,val in wcdict.items():
		if val > 1:
			print "%s %d" %(key, val)
		

file = 'testWrds.txt'
flhandler = readFile(file)
wordCntDict = getWords(flhandler)
printAns(wordCntDict)
