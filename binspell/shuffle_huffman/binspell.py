# binspell
# trigram model
# keyboard input
# delete immediately available
# up arrow = left   ::  down arrow = right
#
# last edit: 11/19
# comments - column 81
################ CHANGES ############
# works with Word class (contains word unigrams and bigrams)
########## TODO ##############
# tcp/ip socket
# window resizable?
# window on top?
# addition of phrases: menu of topics,
# diving bell and butterfly
# change window name
# window focus:
# position root window in center of screen
# do colors aid in text scanning?
# put del b4 spc in training version, then switch
# draw_interface: allow for multiple boxes
###################### BUGS #######################
# 
############## CURRENTLY WORKING ON ##########
# 



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
from Trigraph import *
from Words import *



######################################---------------------- gui -----------#############

def updateCanvas(hilite,norm):
	"""
	This function updates the canvas object reflecting changes due to user interaction
	Args: tag name of user selected box, tag name of non-selected box
	"""
	gv._canvas.itemconfigure(hilite,fill='orange',width=3)
	gv._canvas.itemconfigure(norm,fill='white')
	gv._canvas.update()															#process all events in event queue
	time.sleep(0.05)
	gv._canvas.itemconfigure(hilite,width=1)
	gv._canvas.delete('text')
	draw_interface(gv._canHt,gv._canWdth)
	gv._canvas.update()		



def draw_interface(canHt, canWd):
	"""
	This function draws the objects on the canvas
	Args: canvas height, canvas width
	"""
	global gv
	cntrx = 0.5 * canWd
	cntry = 0.5 * canHt
	pad = canWd / 50
	height = canHt /2 - pad
	width = 0.25 * canWd - pad
	brdr = 1

	cntrx_b1 = 0.25 * canWd
	cntry_b1 = 0.5 * canHt
	tag1 = 'box1'

	cntrx_b2 = canWd * 3/4
	cntry_b2 = 0.5 * canHt
	tag2 = 'box2'

	draw_square(cntrx_b1, cntry_b1, height, width, brdr, tag1)					#draw boxes
	draw_square(cntrx_b2, cntry_b2, height, width, brdr, tag2)

	draw_text(cntrx_b1, cntry_b1, height, width, gv._box1)						#draw symbols in boxes
	draw_text(cntrx_b2, cntry_b2, height, width, gv._box2)

	gv._canvas.update()															#process all events in event queue



def draw_square(x, y, h, w, brdr, tag):
	"""
	This function draws a square onto the canvas object
	Args: center x position, center y position, height, width, border width, tag name
	"""
	global gv
	gv._canvas.create_rectangle(x-w, y-h, x+w, y+h, width=brdr, tags=tag)



def draw_text(cntrx, cntry, h, w, symbolList):
	"""
	This function draws the symbols within the box objects
	Args: center x postion of box, center y postion of box, height of box, width of box, list of symbols
	"""
	global gv, bg

	maxFntSz = 60																#largest font size
	minFntSz = 15																#smallest font size
	color = 'black'
	x = cntrx - w
	y = cntry - h

	padx = w/7																	#left and right margins
	pady = h/5																	#top and bottome margins
	tab = 40																	#space between symbols
	pos = 'w'																	#left justified
	xtraSymbSpace = 0															#for whole words or large symbols

	if len(symbolList) == 1:													#one symbol left in box
		if len(str(symbolList[0])) > 1:  										#SPC or DEL, etc
			color = 'red'
			fontSz = 40
			font = 'Courier %i bold' %fontSz
			xtraSymbSpace = len(str(symbolList[0])) * fontSz/2
			pos = 'c'
		else:
			font = 'Courier %i bold' %maxFntSz
			color = 'red'
		gv._canvas.create_text(cntrx, cntry, text=symbolList[0].upper(), font=font, tag='text', fill=color, anchor=pos)
	else:
		for item in symbolList:
			color = 'black'														#reset
			tab = 40
			xtraSymbSpace = 0

			if len(str(item)) > 1:												#if '[DEL]' or '[SPC]' is in item
				color = 'cyan'
				fontSz = 40
				font = 'Courier %i bold' %fontSz
				xtraSymbSpace = len(str(item)) * fontSz
				pos = 'w'
			else:
				fontSz = getRelFntSz(item, maxFntSz, minFntSz)
				font = 'Courier %i bold' %fontSz

			if fontSz <= 20:													#less space for small symbols
				tab = 25
				color = 'blue'

			if fontSz > 45:														#more space for large symbols
				xtraSymbSpace = round(fontSz / 3)

			if item in gv._hiProb:												#most probable letter is red
				color = 'red'

			if x + padx + xtraSymbSpace > cntrx + w - padx:   					#goin past the edge of the box
				x = cntrx - w   												#reset x to right edge
				y = y + pady + fontSz   										#new line
				gv._canvas.create_text(x+padx, y+pady, text='\n', font=font)

			gv._canvas.create_text(x+padx, y+pady, text=item.upper(), font=font, tag='text', fill=color, anchor=pos)
			x = x + tab + xtraSymbSpace



###################################################---------------state fxns---------########

def saveState():
	"""
	This function creates a State object, assigns State member variables the values of selected variables representing the state of the keyboard, 
	and pushes the State object onto the stack
	"""
	global gv, bg, stack
	stateObj = State(gv._ngram, gv._currCondTable, gv._transitionProbs, gv._emissionProbs, gv._lastWordTyped, gv._prefix, gv._posInWrd, gv._top3words)
	stack._push(stateObj)



def return2PrevState():
	"""
	This function pops the last State object off the stack, and assigns current keyboard state variables the values 
	of the State member variables
	"""
	global gv, bg

	gv._box1 = []
	gv._box2 = []
	flag = 0																	#indicates whether or not gv._numTyped needs to be further modified

	if gv._prefix == '' and gv._posInWrd == 0:									#whole word needs to be erased
		gv._numTyped = gv._numTyped - len(gv._lastWordTyped) - 1				# -1 for [spc] automatically added after selection of a whole word
		flag = 1
	else:
		gv._numTyped -= 1

	stateObj = stack._pop()
	gv._ngram = stateObj._ngram													#return keyboard to previous state
	gv._currCondTable = stateObj._currCondTree
	gv._transitionProbs = stateObj._currTrnsProbs
	gv._emissionProbs = deepcopy(gv._transitionProbs)
	gv._lastWordTyped = stateObj._lastWord
	gv._prefix = stateObj._prefix
	gv._posInWrd = stateObj._posinwrd
	gv._top3words = stateObj._top3

	if flag == 1:
		gv._numTyped += len(gv._prefix)
		for lett in gv._prefix:													#replace letters user already typed out and don't want to delete
			output(lett)

	if gv._top3words != {}:
		updateDist(gv._top3words,gv._emissionProbs[gv._ngram])
	
	set_layout(gv._emissionProbs[gv._ngram].keys(),gv._emissionProbs[gv._ngram])

	hiProb = getLrgstLeaf(gv._emissionProbs[gv._ngram])
	gv._hiProb = hiProb[0]														####### HACK ########

	hilite = "box1"
	norm = "box2"

	updateCanvas(hilite,norm)													#process all events in event queue



def resetConsts(typed):
	"""
	This function resets all global constants depending on what symbol was last chosen by the user
	Args: last user symbol selected
	"""
	global gv, bg

	if len(typed) > 1 and '[' not in typed[0]:									#check for selection of a full word, but not [spc] or [del]
		gv._lastWordTyped = typed
		gv._posInWrd = 0
		gv._obsOut.append('[SPC]')												#automatically insert [spc] after a full word
		gv._ngram = typed[-1] + '[SPC]'											#reset bigram to last letter of last word typed + spc
		gv._numTyped += (len(typed) - len(gv._prefix) + 1)
		gv._currCondTable = tg._tgraph
		gv._prefix = ''
	else:			
		gv._numTyped += 1
		if typed == '[SPC]':													#a word was spelled out by user
			gv._lastWordTyped = gv._prefix
			gv._prefix = ''
			gv._posInWrd = 0
		else:
			gv._posInWrd += 1
			gv._prefix += typed

		if gv._numTyped < 2:													#only one letter typed thus far
			gv._currCondTable = bg._conditional1
			gv._ngram = typed
		else:																	#use trigram conditional probabilities
			gv._ngram = getBgram()
			gv._currCondTable = tg._tgraph

	gv._transitionProbs = gv._currCondTable
	gv._emissionProbs = deepcopy(gv._transitionProbs)

	gv._top3words = wd._closestWords(gv._prefix,gv._lastWordTyped)				#guess words based on what's been typed
	if gv._top3words != {}:
		updateDist(gv._top3words,gv._emissionProbs[gv._ngram])

	gv._ttlNumSteps = gv._ttlNumSteps + gv._numSteps
	gv._ttlNumErr = gv._ttlNumErr + gv._numErrors
	gv._numSteps = 0
	gv._numErrors = 0
	gv._typed = ['',0]

	hiProb = getLrgstLeaf(gv._emissionProbs[gv._ngram])
	gv._hiProb = hiProb[0]														####### HACK ########
	gv._numTimesLargest = 0



def shuffle(chosen,Nchosen):
	"""
	This function determines whether or not symbol should be typed out.  If so, it calls methods which 
	modify the state of the keyboard according to the symbol being output.  It also calls a method which 
	re-orders the displayed keyboard symbols.
	Args: set of symbols chosen by user, set of symbols not chosen by user
	"""
	global gv

	gv._emissionProbs[gv._ngram] = updateEmiss(gv._emissionProbs[gv._ngram], chosen)
	hiProb = getLrgstLeaf(gv._emissionProbs[gv._ngram])
	hiProb = hiProb[0]															####### HACK ########
	gv._hiProb = hiProb

	if hiProb[1] > gv._threshold:												#output a symbol
		output(hiProb[0])
		gv._obsOut.append(hiProb[0])
		if '[DEL]' in hiProb[0]:
			gv._numDels += 1
			return2PrevState()
			infoTransferRate()
			return
		else:
			saveState()
			resetConsts(hiProb[0])
			infoTransferRate()

	set_layout(chosen,gv._emissionProbs[gv._ngram])



def update(decision):
	"""
	This function sets variables used to update the state of the keyboard, based on the user's input.
	It then calls the method which re-orders and re-allocates the symbols between boxes, and calls the 
	canvas to update the displayed keyboard with the new symbol order.
	Args: User's left or right box selection
	"""
	global gv, bg

	left = 1
	right = 2
	gv._numSteps = gv._numSteps + 1												#keep track of number of user decisions

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

	shuffle(chosen,Nchosen)														#re-order symbols
	updateCanvas(hilite,norm)													#update keyboard displayed



####################################################--------- helper fxns----------#########

def updateDist(wrdProbs,eProbs):
	"""
	This function updates the emission probability tables for the symbols, to include the probabilities
	of the most likely words.
	Args: dict of most likely words:probs, dict of emission probs of letters
	"""
	wtot = sum(wrdProbs[key] for key in wrdProbs)								#sum of probs in top words dict
	ltot = sum(eProbs[key] for key in eProbs)									#sum of probs in emission probs dict

	if '[DEL]' in eProbs.keys():
		reWeightDel(eProbs,len(wrdProbs),wtot+ltot)								#assign [del] avg of all probs
		ltot = sum(eProbs[key] for key in eProbs)								#new sum

	mplier = float(wtot)/float(ltot)
	for key in eProbs:															#normalize
		eProbs[key] *= mplier
	
	eProbs.update(wrdProbs)														#update emission probabilities



#assign [del] average of emiss probs and word probs
#subtract n smallest values to make [del] weigh more, where n=number of previous deletes
#args: emission probs,number of words,sum(emissionprobs + wordprobs)
def reWeightDel(eprobs,numwrds,tot):
	ordrEprobs = gv._sortByValue(eprobs)
	sm = 0
	num =  3
	for i in range(0,num):
		sm += ordrEprobs[i][1]
	eprobs['[DEL]'] = sm / num		#assign [del] average of top 3 values
	#print "in reweight: eprobs[del]:", eprobs['[DEL]']

	
	
#returns: string containing last 2 letters output
def getBgram():
	global gv
	temp = gv._obsOut[-2:]
	#print "in getBgram: temp:", temp
	return temp[0]+temp[1]


def consonant(symb):
	alphabet = set(map(chr,range(97,123)))
	v_set = set(['a','e','i','o','u','y'])
	c_set = alphabet - v_set
	#print "consonants: ", c_set
	return (symb in c_set)



def wrongGrammar(symb):
	global gv
	if symb == '[SPC]' and gv._ngram == '[SPC]':
		return True
	#if gv._posInWrd > 0 and gv._posInWrd < 4:
		#if consonant(gv._ngram) and consonant(symb):
			#return True
	return False



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
	sortdProbs = gv._sortByValue(gv._emissionProbs[gv._ngram])		#sort current probs in order greatest to least
	for item in sortdProbs:
		if symb in item:						#most probable, so max font size
			return max
		max = max - 2
		if max < min:
			return min



#################################################------------ I/O ---------------##############

#print out itr
def infoTransferRate():
	print #
	print "number of characters typed:", gv._numTyped
	print "number of classifier errors:", gv._ttlNumErr
	print "number of times delete used: ", gv._numDels
	print "total number of steps taken: ", gv._ttlNumSteps
	print "simulation information transfer rate: %.5f" %(float(gv._numTyped) * float(60) / float(time.time() - gv._startTime))
	print "projected BCI-controlled information transfer rate: %.5f" %(float(gv._numTyped) * float(60) / float(gv._ttlNumSteps * gv._trialLen)) + " chars/min"
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

	#print "in output(): pos in word: ", gv._posInWrd
	#print item
	#if False:
	if item == "[SPC]":
		gv._txtBox.insert(INSERT," ")
	elif item == "[DEL]":
		if gv._prefix == '' and gv._lastWordTyped != '':		#deleting a word
			l = len(gv._lastWordTyped)				
			gv._txtBox.delete("%s-%ic" % (INSERT,l),INSERT)
		gv._txtBox.delete("%s-1c" % INSERT,INSERT)			#delete single character or also delete [spc] (referring to above if)
	elif '[BACK]' in item:							#for bin search version
		return
	elif len(item) > 1:
		#print "outputing:", item
		gv._txtBox.delete("%s-%ic" % (INSERT,gv._posInWrd),INSERT)	#delete prefix
		gv._txtBox.insert(INSERT,item)					#replace prefix with whole word
		gv._txtBox.insert(INSERT," ")					#insert [spc] after word

	else:
		gv._txtBox.insert(INSERT,item)
	#gv._ngram = item
	##print "2rd cursor pos:", gv._txtBox.index(INSERT)



#####################################################--------- viterbi -------###############

#args: list of observed output symbols
def viterbi(obs):
	global bg, gv, stack
	#print "in viterbi: observed:", obs
	#print "len(obs):", len(obs)
	#print #
	state_obj = stack._pop()
	transProbs = state_obj._currTrnsProbs
	emissProbs = state_obj._currEmissProbs

	if len(obs) == 1:
		gv._psi[len(obs)], gv._delta[len(obs)] = init(obs[0],emissProbs)
		#print "in viterbi: gv._delta[len(obs)]:", gv._delta[len(obs)]
		stack._push(state_obj)
		return gv._delta[len(obs)]
	else:
		for symb in obs:
			mxDltaAij, gv._psi[len(obs)] = calcMax(viterbi(obs[0:-1]),transProbs,obs)
			gv._delta[len(obs)] = multEmission(mxDltaAij,emissProbs,obs[-1])

	stack._push(state_obj)

	if len(obs) == len(gv._obsOut):
  		T = len(obs)
		qstar = {}
		pstar,qstar[T] = terminate(gv._delta,gv._psi,T)
		gv._qStar = backTrack(gv._psi,qstar,T)
		gv._qStar[T] = qstar[T]
		print "most probable path:", getPath(gv._qStar,T)
		#print "path: ", gv._qStar
		#print "qstar[T]: ", qstar[T]
	else:
		return gv._delta[len(obs)]



def getPath(qstar,time):
	t = 1
	p = ''
	while t <= time:
		p += qstar[t]
		t +=1
	return p



def terminate(dlta,psy,time):
	#print "in terminate: 
	maxProb = max(dlta[time].values())
	rev_dlta = gv._swap_dictionary(dlta[time])
	argMx = rev_dlta[maxProb]
	return maxProb, argMx



def backTrack(psy,qstar,T):
	while T > 0:
		print "T:", T
		print "qstar[T]:", qstar[T]
		print "psy[qstar[T]]: ", psy
		print #
		qstar[T-1] = psy[qstar[T]]
		T -= 1
	return qstar



# intermediate viterbi calculation
# multiply emission probs by max(delta * aij)
def multEmission(mx_DltaAij,emiss,obsrvd):
	dlta = {}		#delta

	for key in mx_DltaAij:
		#print "mx_DltaAij: ", mx_DltaAij
		#print #
		#print "key:", key
		#print "in multemission: emiss[key]:", emiss[key]
		#print "mx_DltaAij[key]:", mx_DltaAij[key]
		#print #
		dlta[key] = mx_DltaAij[key] * emiss[key][obsrvd]
	return dlta



#intermediate viterbi calculation
#returns max(delta * aij)
#args: delta, transition  probs, observed(just for testing)
def calcMax(delta,aij,obs):
	#print "in calcMax: observed:",obs
	#print #
	mxDltaxAij = {}			# max(delta * aij)
	argmax_i = {}				#argmax(i) of max(delta * aij)

	alphabet = map(chr,range(97,123))

	for lett in alphabet:
		mxDltaxAij[lett] = 0
		#print "in calcMax: delta:", delta
		#print #
		for key in delta:
			#print "key: ", key
			#print "delta[key]:", delta[key]
			#print #
			temp = aij[key][lett] * delta[key]
			if temp > mxDltaxAij[lett]:
				mxDltaxAij[lett] = temp
				argmax_i[lett] = key

	return mxDltaxAij, argmax_i



#initialize gamma and delta for 1st observation
#args: 1st typed symbol
def init(obs,emiss):
	global bg
	#temp = 0
	delta_0 = {}
	gamma_0 = {}
	for key in bg._prior:
		#print "[key]:", [key]
		#print "in init: emis[key]:", bg._emissionProbs[key]
		#print #
		delta_0[key] = bg._prior[key] * emiss[key][obs]
		gamma_0[key] = 0
	return gamma_0, delta_0



#####################################################---------- hmm ---------################

def updateEmiss(eProbs,chos):
	print "in updateemiss: old eprobs:", gv._sortByValue(eProbs)
	print #
	for key in eProbs:
		if key in chos:
			eProbs[key] *= float(0.85)
		else:
			eProbs[key] *= float(0.15)
	eProbs = bg._normalize(eProbs)
	print "in updateemiss: new eprobs:", gv._sortByValue(eProbs)
	print "-"*10
	return eProbs
	#return bg._normalize(eProbs)


#check out what current probs are doing to find a better threshold
def compareProbs():
	global gv
	sortedProbs = gv._sortByValue(gv._emissionProbs[gv._ngram])
	#print "largest prob: ", sortedProbs[0]
	#print "smallest prob: ",sortedProbs[-1]
	print "difference b/t largest and smallest: ", sortedProbs[0][1] - sortedProbs[-1][1]
	#print "difference b/t largest and smallest: ", sortedProbs[0][1] - sortedProbs[-1][1]
	#print "2nd largest: ", sortedProbs[1]
	print "diff b/t largest and 2nd largest : ", sortedProbs[0][1] - sortedProbs[1][1]
	print "number of times largest leaf remained largest consecutively:", gv._numTimesLargest
	print ##
	#return float(sortedProbs[0][1] - sortedProbs[1][1])
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

#args: chosen symbols, trans probs given last typed
def set_layout(symbs,probs):
	#print "in set_layout()"
	#print "probs: ", probs
	#print "in set layout:", symbs
	#print "probs: ", probs
	#print #
	global gv
	gv._box1 = []
	gv._box2 = []

	#splitLayAlpha(symbs,probs)
	#splitLaySrtd(symbs,probs)
	#splitLayHuff(symbs,probs)
	shuffleHuffLay(probs)
	#shuffleRndmLay(probs)

	#print "box1: ", gv._box1
	gv._box1.sort()
	gv._box2.sort()

	#print "in setlayout: gv._box1:", gv._box1
	#print "in setlayout: gv._box2:", gv._box2

	if False:
		if gv._numTyped > 0:		#check for sumthin already typed
		#if len(symbs) < 3
			#print "charNum:", gv._numTyped
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



def default():
	"""
	This function initializes all probability tables and reads in, arranges, and displays all symbols.
	"""
	global gv, bg
	gv._currCondTable = bg._conditional1										#table of prior probabilities
	gv._transitionProbs = gv._currCondTable										#table of transition probs
	gv._emissionProbs = deepcopy(gv._transitionProbs)							#table of emission probs
	gv._top3words = wd._closestWords(gv._prefix,gv._lastWordTyped)				#guess words based on what's been typed
	updateDist(gv._top3words,gv._emissionProbs[gv._ngram])						#add words to emission probs
	hiProb = getLrgstLeaf(gv._emissionProbs[gv._ngram])							#most probable symbol
	gv._hiProb = hiProb[0]														####### HACK ########
	set_layout([],gv._emissionProbs[gv._ngram])									#arrange the symbols (letters and words)
	saveState()																	#in case of a later 'delete'
	draw_interface(gv._canHt, gv._canWdth)										#display



#let huffman encoding determine arrangement
def splitLayHuff(symbs,probs):
	#print "in splitLayHuff"
	print "in splitLayHuff: symbs: ", symbs
	if len(symbs) == 1:
		#print "length 1"
		gv._box1 = symbs
	else:
		if symbs != []:
			condList = list((gv._emissionProbs[gv._ngram][key],key) for key in gv._emissionProbs[gv._ngram] if key in symbs)
		else:
			condList = list((gv._emissionProbs[gv._ngram][key],key) for key in gv._emissionProbs[gv._ngram])
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

	if gv._numSteps > 0:
		#gv._box1.insert(-1,'[BACK]')
		gv._box2.insert(-1,'[BACK]')
	if gv._numTyped > 0 and '[DEL]' not in gv._box1 and '[DEL]' not in gv._box2:
		gv._box2.insert(-1,'[DEL]')
		#print "in splitlayhuff: in if: [del] in box1:", ('[DEL]' in gv._box1)
		#print "box2:", gv._box2
		#print #



#arrange symbols: 1/2 box1 and 1/2 box2
#sorted according to probs
def splitLaySrtd(symbs,probs):
	if len(symbs) == 1:
		gv._box1 = symbs
	else:
		if symbs != []:
			probs = dict((key,probs[key]) for key in probs if key in symbs)

		srtdProbs = gv._sortByValue(probs)
		print "in splitlaysorted: sorted probs:", srtdProbs
		print "symbs:",symbs
		print "probs: ",probs
		print #

		if symbs == []:
			if gv._numTyped > 0:
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
	if gv._numSteps > 0:
		#gv._box1.insert(-1,'[BACK]')
		gv._box2.insert(-1,'[BACK]')



#arrange symbols: 1/2 box1 and 1/2 box2
#sorted alphabetically
def splitLayAlpha(symbs,probs):
	global gv
	if len(symbs) == 1:
		gv._box1 = symbs
	else:
		if symbs == []:
			if gv._numTyped > 0:
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
	if gv._numSteps > 0:
		#gv._box1.insert(-1,'[BACK]')
		gv._box2.insert(-1,'[BACK]')



#################################--------------------------start------------###########

def getKeyIn():
	"""
	This function creates a binding between a keypress event and the nested keyCtrl() method
	"""
	def keyCtrl(event):
		"""
		This function is an handler for keypress events.  It also simulates misclassifications
		and calls the update() method to update the keyboard interface accordingly
		Args: keypress event
 		"""
		if gv._startTime == 0:
			gv._startTime = time.time()

		decision = 3

		if event.keysym == 'Up':
			decision = 1														#select left box
		if event.keysym == 'Down':
			decision = 2														#select right box

		#simulate misclassification
		err_var = random.random()												#returns number b/t 0-1
		err_var = 1																#100% accuracy -- comment out for misclassfication
		if err_var <= float(1 - gv._classAcc): 									#error case: test if err_var is <= classifier accuracy
			if decision == 1:													#flip user input to simulate error
				decision = 2
			else:																
				decision = 1
			gv._ttlNumErr = gv._ttlNumErr + 1
			print "oops! classifier error number ", gv._ttlNumErr
			print #

		if decision < 3:
			update(decision)

		return "break"

	gv._canvas.bind_all('<Key>',keyCtrl)										#bind keypress to method



def start():
	"""
	This function calls the method for drawing the default interface, then calls the method which
	processes keyboard inputs
	"""
	default()																	#display entire alphabet
	getKeyIn()																	#grab keyboard input



##################################-------------------main---------------################################

root = Tk()																		#new window
root.config(width=300,height=500)
gv = GlobalVariables()															#never a good idea but considering time constraint...
bg = Bigraph()
tg = Trigraph()
wd = Words()
stack = Stack()

canvHeight = 600
canvWidth = 1200
gv._canHt = canvHeight
gv._canWdth = canvWidth
txtBxWidth = canvWidth / 26
txtBxHeight = 1

gv._canvas = Canvas(root,height=canvHeight,width=canvWidth,bg='yellow')
gv._canvas.create_window(100,100)
gv._canvas.grid(row=2,column=1)

gv._txtBox = Text(root,width=txtBxWidth,height=txtBxHeight,padx=5,pady=5,insertofftime=250,takefocus=1, font='Courier 32 bold')
gv._txtBox.grid(row=1,column=1)
gv._txtBox.focus()

start()
root.mainloop()