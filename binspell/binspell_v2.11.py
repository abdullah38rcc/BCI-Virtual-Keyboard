# binspell - works with keyboard input
# no huffman used to layout
# delete immediately available
# up arrow = left   ::  down arrow = right
#
# last edit: 8/13
################CHANGES############
# no huff tree used
# no redudancy - basically binary search
##########TODO##############
#-----------Sri suggest------------
# use without huffman 
# prove huffman's optimality in this case
# compare itr w/o error of circlespell/hexospell/binspell
# display tree or change size of letter according to probs
#-----------------------------------
# break update() into more helper functions
# tcp/ip socket
# scan text and calculate freq
# window resizable?
# window on top?
# addition of phrases: menu of topics, 
# diving bell and butterfly
# change window name
# window focus: 
# position root window in center of screen
# do colors aid in text scanning?
# is class._doc_ writable?
# put del b4 spc in training version, then switch
# draw_interface: allow for multiple boxes
# delete state object after pop
######################BUGS#######################
# order in boxes after default layout, incorrect
##############CURRENTLY WORKING ON##########
# singleSymbInBx not rlly workin out...try placing spc and del seperate frrom alphabet after output



from copy import deepcopy
from Tkinter import *
from math import *
from socket import *
from tkFont import *
import random, time, heapq
from GlobalVariables import *
from Bigraph import *
from Stack import *
from State import *



######################################---------------------- gui -----------#############

def updateCanvas(hilite,norm):
	gv._canvas.itemconfigure(hilite,width=3)
	gv._canvas.itemconfigure(norm,width=1)
	#gv._canvas.update()		#process all events in event queue
	gv._canvas.delete('text')
	#set_layout(gv._box1)
	draw_interface(gv._canHt,gv._canWdth)
	gv._canvas.update()		#process all events in event queue



def draw_interface(canHt, canWd):
	#print "in draw interface()"	
	#print "gv._boxList @beginning of draw_interface():",gv._boxList

	global gv
	cntrx = 0.5 * canWd
	cntry = 0.5 * canHt
	pad = canWd / 30
	height = canHt /2 - pad
	width = 0.25 * canWd - pad
	brdr = 1

	cntrx_b1 = 0.25 * canWd
	cntry_b1 = 0.5 * canHt
	tag1 = 'box1'

	cntrx_b2 = canWd * 3/4
	cntry_b2 = 0.5 * canHt
	tag2 = 'box2'

	#test centers
	#gv._canvas.create_text(cntrx, cntry, text='x')
	#gv._canvas.create_text(cntrx_b2, cntry_b2, text='x')

	draw_square(cntrx_b1, cntry_b1, height, width, brdr, tag1)
	draw_square(cntrx_b2, cntry_b2, height, width, brdr, tag2)

	#print "drawing box1"
	draw_text(cntrx_b1, cntry_b1, height, width, gv._box1)
	#print "drawing box2"
	draw_text(cntrx_b2, cntry_b2, height, width, gv._box2)

	gv._canvas.update()		#process all events in event queue
	#time.sleep(1)



def draw_square(x, y, h, w, brdr, tag):
	global gv
	gv._canvas.create_rectangle(x-w, y-h, x+w, y+h, width=brdr, tags=tag)



def draw_text(cntrx, cntry, h, w, symbolList):
	global gv, bg

	#print symbolList
	#print ###########
	maxFntSz = 60			#largest font size
	minFntSz = 15			#smallest font size
	color = 'black'
	x = cntrx - w
	y = cntry - h

	padx = w/7			#left and right margins
	pady = h/5			#top and bottome margins
	tab = 40			#space between symbols
	pos = 'w'			#left justified
	xtraSymbSpace = 0	#for whole words or large symbols

	#print #
	#print gv._hiProb
	#print #

	if len(symbolList) == 1:			#one symbol left in box
		#print symbolList
		#print "len(str(item)):", len(str(symbolList[0]))
		#print #
		if len(str(symbolList[0])) > 1:  #SPC or DEL, etc
			color = 'cyan'
			fontSz = 40
			font = 'Courier %i bold' %fontSz
			xtraSymbSpace = len(str(symbolList[0])) * fontSz/2
			pos = 'c'
		else:
			font = 'Courier %i bold' %maxFntSz
			#color = 'red'
		gv._canvas.create_text(cntrx, cntry, text=symbolList[0].upper(), font=font, tag='text', fill=color, anchor=pos)
	else:
		for item in symbolList:
			color = 'black'		#reset
			tab = 40
			xtraSymbSpace = 0

			if len(str(item)) > 1:	#if '[DEL]' or '[SPC]' in item
				color = 'cyan'
				fontSz = 40
				font = 'Courier %i bold' %fontSz
				xtraSymbSpace = len(str(item)) * fontSz/2
				pos = 'w'
			else:
				fontSz = getRelFntSz(item, maxFntSz, minFntSz)
				font = 'Courier %i bold' %fontSz
				#print item + ": %i" %fontSz

			if fontSz <= 20:		#less space for small symbols
				tab = 25
				#print "in draw text: fontSz <= 20: ", item

			if fontSz > 45:		#more space for large symbols
				xtraSymbSpace = round(fontSz / 3)
				#print "in draw text: fontSz > 45: ", item

			if item in gv._hiProb:		#most probable letter is red
				color = 'red'
				#print "in draw text: item:", item
				#print "in draw text: hiProb:", gv._hiProb
			#print item + ":" + color

			if x + padx + xtraSymbSpace > cntrx + w - padx:   #goin past the edge
				x = cntrx - w   #reset x to rt edge
				y = y + pady + fontSz   #\n
				gv._canvas.create_text(x+padx, y+pady, text='\n', font=font)

			gv._canvas.create_text(x+padx, y+pady, text=item.upper(), font=font, tag='text', fill=color, anchor=pos)
			x = x + tab + xtraSymbSpace



###################################################---------------state fxns---------########

#def saveState(usrChoice):
def saveState():
	global gv, bg, stack
	#stateObj = State(gv._box1, gv._box2, gv._currProbs, gv._hiProb, usrChoice)
	#print "in save state"
	#print "gv._lastTyped: ", gv._lastTyped
	#print "box1"
	stateObj = State(gv._lastTyped, gv._currCondTree)
	stack._push(stateObj)
	



def getPrevState():
	global gv, stack
	stateObj = stack._pop()
	#gv._box1 = stateObj._box1
	#gv._box2 = stateObj._box2
	gv._lastTyped = stateObj._lasttyped
	gv._currCondTree = stateObj._conditionals
	#gv._currProbs = stateObj._currprobs
	#gv._hiProb = stateObj._hiprob
	#gv._suggested = stateObj._suggested
	#gv._huffSuggest = stateObj._huff
	#bg._topList = stateObj._bgraph
	#return stateObj._usrchoice
	return stateObj._conditionals



def return2PrevState():
	global gv, bg
	gv._box1 = []
	gv._box2 = []
	#prevDecision = getPrevState()
	#print "in return2PrevState"
	gv._currProbs = getPrevState()
	if False:
		if gv._lastTyped != ' ':
			#print "gv._lastTyped: ", gv._lastTyped
			gv._box1 = list((key) for key in gv._currProbs)
			gv._box1.sort()
			gv._box2.insert(0,'[DEL]')
		else:
			set_layout([],gv._currProbs)
	set_layout([],gv._currProbs)
	#gv._currProbs = conds[gv._lastTyped]
	#hilite = "box%i" %prevDecision

	hiProb = getLrgstLeaf(gv._currProbs)
	gv._hiProb = hiProb[0]					####### HACK ########

	hilite = "box1"
	norm = "box2"
	if False:
		if prevDecision > 1:
			norm = "box1"
		else:
			norm = "box2"

	updateCanvas(hilite,norm)	#process all events in event queue



#reset global constants
def resetConsts(typed):
	global gv, bg

	gv._lastTyped = typed
	gv._charNum = gv._charNum + 1
	#print "typed: ",gv._lastTyped

	#check for position in word being typed
	if gv._lastTyped == '[SPC]':
		#print "space ttyped"
		gv._currCondTree = bg._prior
	elif gv._charNum > 2:
		gv._currCondTree = bg._conditional2[gv._lastTyped]
	else:	#begginning of word
		gv._currCondTree = bg._conditional1[gv._lastTyped]
	#print "in update: gv._currProbs: ", gv._currProbs
	#print ##
	gv._ttlNumSteps = gv._ttlNumSteps + gv._numSteps
	gv._ttlNumErr = gv._ttlNumErr + gv._numErrors
	gv._numSteps = 0
	gv._numErrors = 0
	gv._typed = ['',0]
	gv._hiProb = ['',0]
	gv._numTimesLargest = 0
	return gv._currCondTree



def split(chosen,Nchosen):
	global gv
	#output a character and/or reset state if final symbol
	if len(chosen) == 1:
		output(chosen[0])
		if '[DEL]' in chosen[0]:
			#print "deleting"
			gv._charNum = gv._charNum - 1
			return2PrevState()
			return
		else:									#output into text box
			#print "outputting a letter"
			saveState()
			#condList = list((gv._currProbs[key],key) for key in gv._currProbs)
			#printProbs(condList)
			gv._currProbs = resetConsts(chosen[0])
			infoTransferRate()
			chosen = []
	else:
		if gv._charNum > 0:					#sumthin already typed so check for delete
			gv._box2.remove('[DEL]')		#remove delete
		if chosen != []:
			gv._currProbs = updateProbs(chosen,Nchosen,gv._currProbs)
			gv._currProbs = bg._normalize(gv._currProbs)

	hiProb = getLrgstLeaf(gv._currProbs)
	gv._hiProb = hiProb[0]					####### HACK ########
	#print "in update: hiProb:", gv._hiProb
	set_layout(chosen,gv._currProbs)



def shuffle(chosen,Nchosen):
	global gv

	if gv._charNum > 0:					#sumthin already typed so check for delete
		gv._box2.remove('[DEL]')		#remove delete

	gv._currProbs = updateProbs(chosen,Nchosen,gv._currProbs)
	gv._currProbs = bg._normalize(gv._currProbs)
	#compareProbs()				#difference between largest and smallest prob
	hiProb = getLrgstLeaf(gv._currProbs)
	hiProb = hiProb[0]					####### HACK ########
	gv._hiProb = hiProb
	#print "in shuffle: hiProb: ", hiProb
	#if singleSymbInBx(chosen):
		#print "eureka!"
	#if hiProb[1] > gv._threshold or singleSymbInBx(chosen) and hiProb[0] in chosen:			#output a symbol
	if hiProb[1] > gv._threshold:
		#condList = list((gv._currProbs[key],key) for key in gv._currProbs)
		#printProbs(condList)
		output(hiProb[0])
		if '[DEL]' in chosen[0]:
			#print "deleting"
			gv._charNum = gv._charNum - 1
			return2PrevState()
			return
		else:
			gv._currProbs = resetConsts(hiProb[0])
			saveState()
			infoTransferRate()

	set_layout(chosen,gv._currProbs)



#update state
def update(decision):
	global gv, bg

	left = 1
	right = 2
	gv._numSteps = gv._numSteps + 1

	if decision == left:
		hilite = "box%i" %left
		norm = "box%i" %right
		chosen = gv._box1
		Nchosen = gv._box2
	else:	
		hilite = "box%i" %right
		norm = "box%i" %left
		chosen = gv._box2
		Nchosen = gv._box1

	#split(chosen,Nchosen)	#split symbols like binary search
	shuffle(chosen,Nchosen)	#shuffle symbols

	updateCanvas(hilite,norm)



####################################################--------- helper fxns----------#########

def singleSymbInBx(symb):
	#print "gv._box2:", gv._box2
	#print "len(gv._box1):", len(gv._box1)
	if len(gv._box1) == 1:
		print "in singleSymbInBx: symb: ", symb
		print "in singleSymbInBx: box1: ", gv._box1
		print "symb in box1: ", symb == gv._box1
		return (symb == gv._box1) 
	elif len(gv._box2)==1:
		return (symb == gv._box2) 
	else:
		return False



#args: symbol, maxFontSize, minFontSize
#returns: font size for symbol determined by it's order in orderd prob list
def getRelFntSz(symb,max, min):
	global gv
	sortdProbs = gv._sortByValue(gv._currProbs)		#sort current probs in order greatest to least
	for item in sortdProbs:
		if symb in item:
			return max
		max = max - 2
		if max < min:
			return min
	#return round(gv._currProbs[symb] * max)



#################################################------------ I/O ---------------##############

#print out itr
def infoTransferRate():
	print #
	print "number of characters typed:", gv._charNum
	print "total number of steps taken: ", gv._ttlNumSteps
	print "information transfer rate: %.5f" %(float(gv._charNum) / (gv._ttlNumSteps * gv._trialLen)) + " chars/sec"
	print #



#arg: list[probs,symbols]
#sorts list and visually compares probalilities
def printProbs(probs):
	pad = 3
	n = 75
	probs.sort()
	for item in probs:
		hashNum = int(round(item[0] * n))
		#print hashNum
		print item[1].ljust(pad) + '#' * hashNum + '.' * (n - hashNum) + "%f" %(item[0])
	print ## 



def output(item):
	global gv
	#global gv._canvas, gv._txtBox
	
	##print "in output():"
	#print item		
	#if False:
	if item == "[SPC]":
		gv._txtBox.insert(INSERT," ")
	elif item == "[DEL]":
		gv._txtBox.delete("%s-1c" % INSERT,INSERT)
	else:
		gv._txtBox.insert(INSERT,item)
	#gv._lastTyped = item	

	##print "2rd cursor pos:", gv._txtBox.index(INSERT)



#####################################################---------- hmm ---------################

# recalculate probabilities for shuffling
# args: selected box, box not selected, conditionals
# returns dict of probabilites multiplied by classifier accuracy
def updateProbs(selBx,notSelBx, condTree):
	global gv, bg
	#print "in update probs"
	selTree = getLeaves(selBx,condTree)	#selected subtree
	notSelTree = getLeaves(notSelBx,condTree)	#subtree not selected
	selTree = bg._mult(selTree, gv._classAcc)
	notSelTree = bg._mult(notSelTree, 1-gv._classAcc)
	selTree.update(notSelTree)
	return selTree



#check out what current probs are doing to find a better threshold
def compareProbs():
	global gv
	sortedProbs = gv._sortByValue(gv._currProbs)
	#print "largest prob: ", sortedProbs[0]
	#print "smallest prob: ",sortedProbs[-1] 
	print "difference b/t largest and smallest: ", sortedProbs[0][1] - sortedProbs[-1][1]
	#print "difference b/t largest and smallest: ", sortedProbs[0][1] - sortedProbs[-1][1]
	#print "2nd largest: ", sortedProbs[1]
	print "diff b/t largest and 2nd largest : ", sortedProbs[0][1] - sortedProbs[1][1]
	print "number of times largest leaf remained largest consecutively:", gv._numTimesLargest
	print ##
	#return Decimal(sortedProbs[0][1] - sortedProbs[1][1])
	return ((sortedProbs[0][1] - sortedProbs[-1][1]) > gv._diffThreshold)



######################################----------------- huffman tree methods -------------##############

# left child > right child
# args: list of symbols and their probs
def makeHuffTree(symbLst):
	#print len(symbLst)
	#print "##########"
	#print "huff tree"
	tree = symbLst
	#print tree.sort()
	heapq.heapify(tree)
	while len(tree) > 1:
		childR, childL = heapq.heappop(tree), heapq.heappop(tree)
		#print "childL:",childL
		#print "childR",childR
		#print childR < childL
		#print "##########"
		parent = (childL[0] + childR[0], childL, childR)
		#print "parent:", parent
		#print "##########"
		heapq.heappush(tree, parent)

	#print tree
	return tree[0]



# args: box of chars, tree
# returns conditional subtree associated with box of chars
def getLeaves(box,tree):
	#print tree
	#print #
	return dict( (item,tree[item]) for item in box)



# returns largest node in tree as [key,tree[key]]
def getLrgstLeaf(tree):
	maxProb = max(tree.values())
	#print "maxProb:", maxProb
	return list(([key,tree[key]]) for key in tree if tree[key] == maxProb)



###################################--------------------------------- layout -------------##############

def set_layout(symbs,probs):
	#print "in set_layout()"
	#print "in set layout:", symbs
	#print #
	global gv
	gv._box1 = []
	gv._box2 = []

	#splitLayAlpha(symbs,probs)
	#splitLaySrtd(symbs,probs)
	#splitLayHuff(symbs,probs)
	#shuffleHuffLay(probs)
	shuffleRndmLay(probs)

	#print "box1: ", gv._box1
	gv._box1.sort()
	gv._box2.sort()

	#print "in setlayout: gv._box1:", gv._box1
	#print "in setlayout: gv._box2:", gv._box2

	if gv._charNum > 0:		#check for sumthin already typed 	
	#if len(symbs) < 3
		#print "charNum:", gv._charNum
		gv._box2.insert(-1,'[DEL]')
		#gv._box2.insert(-1,'[SPC]')



def shuffleHuffLay(probs):
	global gv
	#print "in shuffleHuffLay: probs:", probs
	#print #
	condList = list((probs[key],key) for key in probs)
	gv._huffTree = makeHuffTree(condList)
	lTree = gv._huffTree[1]
	#print "lTree:", lTree
	rTree = gv._huffTree[2]
	#print "rTree:", rTree
	#print #
	gv._box1 = layoutHuff(lTree,[])
	gv._box2 = layoutHuff(rTree,[])



# randomly lay out symbols
def shuffleRndmLay(probs):
	global gv
	#print "in shuffleRndmLay: probs: ", probs
	for key in probs:
		bool = random.randint(0,1)
		if bool == 0:
			gv._box1.insert(0,key)
		else:
			gv._box2.insert(0,key)



# args: half the huffman tree, box 1 or 2
# returns a list of symbols in the tree 
def layoutHuff(hTree,box):
	#print "in layoutHuff()"
	global gv
	#print "hTree:", hTree
	#print "len(hTree):", len(hTree)
	#print "left tree:", hTree[0]
	#print ######
	#print "right tree:", hTree[1]
	if len(hTree) == 2:
		#print hTree
		if hTree[1] not in box:
			box.append(hTree[1])
		#print "box:", box
		box.sort()
		return box
	else:
		layoutHuff(hTree[1],box)
		layoutHuff(hTree[2],box)
		box.sort()
		return box



# start with prior probs
def default():
	#print "in default()"
	global gv, bg
	#print "cond[' ']:", bg._conditional1[gv._lastTyped]
	gv._currProbs = bg._prior
	gv._currCondTree = bg._prior
	hiProb = getLrgstLeaf(gv._currProbs)
	gv._hiProb = hiProb[0]					####### HACK ########
	#print "in default, hiprob:", hiProb
	set_layout([],gv._currProbs)
	saveState()
	#print gv._currProbs
	#print "box1:", gv._box1
	#print ###
	#print "box2:", gv._box2
	draw_interface(gv._canHt, gv._canWdth)



#let huffman encoding determine arrangement
def splitLayHuff(symbs,probs):
	#print "in splitLayHuff: symbs: ", symbs
	if len(symbs) == 1:
		#print "length 1"
		gv._box1 = symbs
	else:
		if symbs != []:
			condList = list((gv._currProbs[key],key) for key in gv._currProbs if key in symbs)
		else:
			condList = list((gv._currProbs[key],key) for key in gv._currProbs)
		#printProbs(condList)
		if len(condList) > 1:
			gv._huffTree = makeHuffTree(condList)
			lTree = gv._huffTree[1]
			#print "lTree:", lTree
			rTree = gv._huffTree[2]
			#print "rTree:", rTree
			#print #
			gv._box1 = layoutHuff(lTree,[])
			gv._box2 = layoutHuff(rTree,[])



#arrange symbols: 1/2 box1 and 1/2 box2
#sorted according to probs
def splitLaySrtd(symbs,probs):
	if len(symbs) == 1:
		gv._box1 = symbs
	else:
		if symbs != []:
			probs = dict((key,probs[key]) for key in probs if key in symbs)

		srtdProbs = gv._sortByValue(probs)

		if symbs == []:
			if gv._charNum > 0:
				for item in srtdProbs:
					#print "in update: item: ", item
					gv._box1.insert(-1,item[0])
			else :								#default layout
				for i in range(0,len(srtdProbs)/2):
					gv._box1.insert(-1,srtdProbs[i][0])

				for i in range(len(srtdProbs)/2,len(srtdProbs)):
					gv._box2.insert(-1,srtdProbs[i][0])
		else:
			if len(symbs) > 1:
				for i in range(0,len(srtdProbs)/2):
					if srtdProbs[i][0] in symbs:
						gv._box1.insert(-1,srtdProbs[i][0])

				for i in range(len(srtdProbs)/2,len(srtdProbs)):
					if srtdProbs[i][0] in symbs:
						gv._box2.insert(-1,srtdProbs[i][0])
			else:
				gv._box1.insert(0,symbs[0])

	#######-----move--------###########
				gv._box1.sort()
				gv._box2.sort()



#arrange symbols: 1/2 box1 and 1/2 box2
#sorted alphabetically
def splitLayAlpha(symbs,probs):
	global gv
	if len(symbs) == 1:
		gv._box1 = symbs
	else:
		if symbs == []:
			if gv._charNum > 0:
				for key in probs:
					#print "in update: item: ", item
					gv._box1.insert(-1,key)
			else :								#default layout
				print "default layout"
				alphabet = map(chr,range(97,123))
				print len(alphabet)/2
				for i in range(0,len(alphabet)/2):
					gv._box1.insert(-1,alphabet[i])
				for i in range(len(alphabet)/2,len(alphabet)):
					gv._box2.insert(-1,alphabet[i])

		else:
			if len(symbs) > 1:
				for i in range(0,len(symbs)/2):
					gv._box1.insert(-1,symbs[i])
				for i in range(len(symbs)/2,len(symbs)):
					gv._box2.insert(-1,symbs[i])
			else:
				gv._box1.insert(0,symbs[0])

	#######-----move--------###########
				gv._box1.sort()
				gv._box2.sort()



#################################--------------------------start/test------------###########

#get user input, send to keyboard
def getKeyIn():
	#print "in getKeyIn()"
	##print event.keysym
	##print "in getKeyIn, gv._highlighted=",gv._highlighted
	
	def keyCtrl(event):
		##print "in keyCtrl()"
		
		#simulate 80% classifier accuracy
		errArr = [1,0,1,1,1,0,1,1,1,1]

		decision = 3
		
		##print "key pressed:",event.keysym
		
		if event.keysym == 'Up':
			##print "key up"
			decision = 1	#select left
		if event.keysym == 'Down':
			##print "key down"
			decision = 2	#select right

		#simulate misclassification
		#bool = random.choice(errArr)
		bool = 1
		if bool == 0:
			if decision == 1:
				decision = 2
			else:
				decision = 1
			gv._numErrors = gv._numErrors + 1
			print "oops! classifier error!"
			print "number of errors:", gv._numErrors
			print ####
		
		if decision < 3:
			update(decision)
					
		##print "after upddte call"
		##print "in keyCtrl gv._highlighted=", gv._highlighted
		
		return "break"
	
	##print "before bind call"
	
	gv._canvas.bind_all('<Key>',keyCtrl)
	##print "end of getKeyIn"	



def test_interface():
	global gv, bg
	
	x = 200
	y = 200
	r = 100
	tag = 'box1'
	width = 3
	
	gv.lastTyped = 'h'
	#bg = Bigraph
	
	buildGraph(gv._bigrphLst)
	#print nxtProb(gv.lastTyped)
	print bg.bigrphLst
	
	#draw_square(x,y,r,width,tag)
	#time.sleep(2)	#just to see initial interface
	##print "in test_interface()"
	numtries = 10
	if False:
		for i in range(1,numtries):
		##print "user input #",i
		##print "in test_interface: gv._highlighted=",gv._highlighted
			update(1)
			time.sleep(2)



def start():
	default()		#display entire alphabet
	#grab keyboard input
	getKeyIn()



##################################-------------------main---------------########

root = Tk()
gv = GlobalVariables()
bg = Bigraph()
#bg._print(bg._bigrph1)
#bg._print(bg._bigrph2)
stack = Stack()

canvHeight = 400
canvWidth = 800
gv._canHt = canvHeight
gv._canWdth = canvWidth
txtBxWidth = canvWidth / 8
txtBxHeight = 1

gv._canvas = Canvas(root,height=canvHeight,width=canvWidth,bg='yellow')
gv._canvas.grid(row=2,column=1)

gv._txtBox = Text(root,width=txtBxWidth,height=txtBxHeight,padx=5,pady=5,insertofftime=250,takefocus=1)
gv._txtBox.grid(row=1,column=1)
gv._txtBox.focus()

start()
#testing
#test_interface()

root.mainloop()
