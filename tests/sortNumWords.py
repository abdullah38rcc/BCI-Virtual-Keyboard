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
	for line in fd:
		
		