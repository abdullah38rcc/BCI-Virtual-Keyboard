#marginal and conditional prob tables of letter-trigrams 
#stored in and accessed from sqlLite
#last edited: 11/2/09


from pysqlite2 import dbapi2 as sqlite
import csv
import string
from decimal import Decimal
#from NGramDB import *
from Trigraph import *
from Bigraph import *
from Words import *

def cleanRow(row):
	row[0] = row[0][0:-1]	#strip just the last xtra white-space off row[0]
	
	row[1] = row[1].strip(' ')	#strip all xtra white-space off row[1]
	row[1] = string.split(row[1],' ')
	row[1] = row[1][0]	#for tgramnospc
	#row = row[0:-1]			#strip end of row to get ['trigram','value']
	return row


def buildTgrams(flname,crsr):
	#print "in buildTgrams"
	tgrams = csv.reader(open(flname),delimiter='-')
	count = 0
	for row in tgrams:
		if count < 5:
			#print row
			row = cleanRow(row)
			crsr.execute('INSERT INTO triMargProbs VALUES (?,?)',(row[0],row[1]))
			#print row
			#print #
		count += 1


# read in frequency values from a text file into a list
def readBgrmFile(flName,crsr):
	#fd = open('bgTst.txt', 'r')
	fd = open(flName, 'r')
	#print fd
	#print fd.readline()
	lst = []
	for line in fd:
		#print line
		bits = string.split(line, ',')
		#print Decimal(bits[2].strip(' ')) + 1
		del(bits[-1])
		#print "bits:", bits
		#print ####
		for i in range(1,len(bits),2):
		    item = [(bits[0], bits[i]), Decimal(bits[i+1]) ]
		    crsr.execute('INSERT INTO biMargProbs VALUES (?,?)',(bits[0]+bits[i],bits[i+1]))
		    #print item
		    #lst.append(item)
	#print lst
	return lst

if False:
	#fname = "trgramsWithSpc.txt"
	fname = "tgramsNoSpc.txt"

	connection = sqlite.connect('test.db')		#if file doesn't exist, it'll be opened

	#create a temporary database that exists in memory:
	#memoryConnection = sqlite.connect(':memory:')

	cursor = connection.cursor()
	cursor.execute('DROP TABLE triMargProbs')
	cursor.execute('DROP TABLE biMargProbs')
	#cursor.execute('DROP TABLE prior')
	cursor.execute('CREATE TABLE triMargProbs (tgram CHAR(3) PRIMARY KEY, count INT)')
	cursor.execute('CREATE TABLE biMargProbs (bgram CHAR(2) PRIMARY KEY, count INT)')
	#cursor.execute('CREATE TABLE prior (letter CHAR(1) PRIMARY KEY, count INT)')

	#cursor.execute('ALTER TABLE triMargProbs DROP COLUMN prob')
	#cursor.execute('ALTER TABLE triMargProbs ADD count INT')
	buildTgrams(fname,cursor)
	readBgrmFile("bgramFreq1.txt",cursor)








if False:
	#create initial db tables
	def _createTables(self):
		self._cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")	#get names of existing tables from master table
		tables = self._cursor.fetchall()	#get result array
		for i in range (0,len(tables)):
			query = 'DROP TABLE ' + tables[i][0] 
			self._cursor.execute(query)
		self._cursor.execute('CREATE TABLE triRaw (tgram CHAR(3) PRIMARY KEY, count FLOAT)')
		self._cursor.execute('CREATE TABLE biRaw1 (bgram CHAR(2) PRIMARY KEY, count FLOAT)')
		self._cursor.execute('CREATE TABLE biRaw2 (bgram CHAR(2) PRIMARY KEY, count FLOAT)')
		self._cursor.execute('CREATE TABLE prior (letter CHAR(1) PRIMARY KEY, prob FLOAT)')
		self._cursor.execute('CREATE TABLE biCond1 (bgram CHAR(2) PRIMARY KEY, prob FLOAT)')
		self._cursor.execute('CREATE TABLE biCond2 (bgram CHAR(2) PRIMARY KEY, prob FLOAT)')
		self._cursor.execute('CREATE TABLE triCond (tgram CHAR(3) PRIMARY KEY, prob FLOAT)')
		self._cursor.execute('CREATE TABLE lettMarg (letter CHAR(1) PRIMARY KEY, prob FLOAT)')

		#from literature: >15 chars word length not very probable
		self._cursor.execute('CREATE TABLE wrdBgram (word1 VARCHAR(15), word2 VARCHAR(15), count FLOAT, PRIMARY KEY(word1,word2))')
		self._cursor.execute("CREATE TABLE wordPrior(word VARCHAR(15) PRIMARY KEY, prob FLOAT)")	
		self._cursor.execute("CREATE TABLE wordCond(word1 VARCHAR(15), word2 VARCHAR(15), prob FLOAT, PRIMARY KEY(word1,word2))")











#connection.commit()
if False:
	lett = 'a'
	alphabet = map(chr,range(97,123))
	for lett in alphabet:
		lett = lett + '%'
		cursor.execute("SELECT SUM(count) FROM biMargProbs WHERE bgram LIKE ?||? ",lett)	# || = sqlite string concatenator
		for row in cursor:
			print '-' * 10
			print "letter:", lett
			print "count:", row[0]
			#print "count:", row[1]
			print '-' * 10
#cursor.execute("SELECT SUM(count) FROM biMargProbs WHERE bgram LIKE 'ag'")
#cursor.execute("SELECT SUM(count) FROM biMargProbs WHERE bgram LIKE 'a%'")	# % --> sqlite wildcard


#ng = NGramDB()


#cursor.close()
#connection.close()


#bg = Bigraph()
#tg = Trigraph()
wd = Words()
#wd._closestWords("thi")
