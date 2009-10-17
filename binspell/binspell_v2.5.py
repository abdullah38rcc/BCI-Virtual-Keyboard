# binspell - works with keyboard input - shuffle symbols
# up arrow = left   ::  down arrow = right
#
# last edit: 7/28
################CHANGES############
# deleted defaultLayout()
# getLeaves()
# rewrote setLayout()
##########TODO##############
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
# getting new version of Bigraph to work correctly with binspell




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



######################----------------------drawing fxns-----------#############

def draw_square(x, y, h, w, brdr, tag):
	global gv
	gv._canvas.create_rectangle(x-w, y-h, x+w, y+h, width=brdr, tags=tag)



def draw_text(cntrx, cntry, h, w, symbolList):
	global gv, bg

	#print symbolList
	#print ###########

	fontSz = 30
	font = 'Courier %i bold' %fontSz
	x = cntrx - w
	y = cntry - h

	padx = w/7
	pady = h/5
	tab = 30
	pos = 'w'
	xtraSymbSpace = 0	#for whole words

	if len(symbolList) == 1:
		gv._canvas.create_text(cntrx, cntry, text=symbolList[0].upper(), font=font, tag='text')
	else:
		for item in symbolList:
			#print item[1]
			#print "len(str(item[1])):", len(item[1])	
			if item in bg._topList:
				#print "item: ", item
				#print #########
				color = 'red'
				fontSz = 30
			else:
				fontSz = 20
				color = 'black'	
			if x + padx + xtraSymbSpace > cntrx + w - padx:   #goin past the edge
				x = cntrx - w   #reset x to rt edge
				y = y + pady + fontSz   #\n
				gv._canvas.create_text(x+padx, y+pady, text='\n', font=font)

			gv._canvas.create_text(x+padx, y+pady, text=item.upper(), font=font, tag='text', fill=color, anchor=pos)
			x = x + tab + xtraSymbSpace



####################----------------fxns to do with keyboard state---------########

def saveState(hi,norm):
	global gv, bg, stack
	stateObj = State(gv._box1, gv._box2, gv._suggested, gv._huffSuggest, bg._topList, hi, norm)
	stack._push(stateObj)
	



def getPrevState():
	global gv, bg, stack
	stateObj = stack._pop()
	gv._box1 = stateObj._box1
	gv._box2 = stateObj._box2
	gv._suggested = stateObj._suggested
	gv._huffSuggest = stateObj._huff
	bg._topList = stateObj._bgraph
	return stateObj._highlighted, stateObj._normal



def return2PrevState():
	hilite, norm = getPrevState()
	gv._canvas.itemconfigure(hilite,width=3)
	gv._canvas.itemconfigure(norm,width=1)
	gv._canvas.delete('text')	
	draw_interface(gv._canHt,gv._canWdth)
	gv._canvas.update()		#process all events in event queue



#################-----------gui fxns-----------#############

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



def update(decision):
	#print "in update_circs()"
	global gv, bg
	#print "stack = ", stack
	
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

	gv._currProbs = updateProbs(chosen,Nchosen,gv._currProbs)
	gv._currProbs = bg._normalize(gv._currProbs)
	#print "original conditional:", bg._conditional1[gv._lastTyped]
	#print #
	#print "gv._currProbs:", gv._currProbs
	#print #
	hiProb = getLrgstLeaf(gv._currProbs)
	hiProb = hiProb[0]					####### HACK ########

	#check for redundancy
	if hiProb[0] == gv._hiProb[0]:
		gv._numTimesLargest = gv._numTimesLargest + 1
	else:
		#print "hiProb[0]:", hiProb[0]
		#print 
		gv._hiProb = hiProb
		gv._numTimesLargest = 1

	print "largest leaf:", hiProb
	print "number of times largest consecutively:", gv._numTimesLargest
	print "number of steps to choose:", gv._numSteps
	print #

	#if hiProb[1] > gv._threshold or gv._numTimesLargest > 2:				#output a symbol
	if hiProb[1] > gv._threshold:							#output a symbol
		gv._lastTyped = hiProb[0]
		gv._charNum = gv._charNum + 1

		#check for position in word being typed
		if gv._charNum > 2:
			gv._currProbs = bg._conditional2[gv._lastTyped]
		else:	#begginning of word
			gv._currProbs = bg._conditional1[gv._lastTyped]
		#print "in update: gv._currProbs: ", gv._currProbs
		#print ##
		gv._ttlNumSteps = gv._ttlNumSteps + gv._numSteps
		gv._ttlNumErr = gv._ttlNumErr + gv._numErrors
		gv._numSteps = 0
		gv._numErrors = 0
		gv._hiProb = ['',0]
		gv._numTimesLargest = 0
		output(hiProb[0])
		print "total number of errors so far: ", gv._ttlNumErr
		print "total number of steps so far: ", gv._ttlNumSteps
		print ##
		#print "gv._threshold:", gv._threshold
		#print "hiProb:", hiProb

	condList = list((gv._currProbs[key],key) for key in gv._currProbs)
	#condList = gv._sortByValue(gv._currProbs)
	#print "condList: ",condList
	#print ##

	gv._huffTree = makeHuffTree(condList)
	lTree = gv._huffTree[1]
	#print "lTree:", lTree
	rTree = gv._huffTree[2]
	#print "rTree:", rTree
	gv._box1 = layoutHuff(lTree,[])
	gv._box2 = layoutHuff(rTree,[])

	#print "hilite:", hilite
	#print "norm", norm
	
	gv._canvas.itemconfigure(hilite,width=3)
	gv._canvas.itemconfigure(norm,width=1)
	#gv._canvas.update()		#process all events in event queue
	gv._canvas.delete('text')
	#set_layout(gv._box1)
	draw_interface(gv._canHt,gv._canWdth)
	gv._canvas.update()		#process all events in event queue



#####################---------gui helper fxns----------#########

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
		gv._txtBox.insert(INSERT,item.lower())
	gv._lastTyped = item	

	##print "2rd cursor pos:", gv._txtBox.index(INSERT)



# recalculate probabilities for shuffling
# args: selected box, box not selected, conditionals
# returns dict of probabilites multiplied by classifier accuracy
def updateProbs(selBx,notSelBx, condTree):
	global gv, bg
	selTree = getLeaves(selBx,condTree)	#selected subtree
	notSelTree = getLeaves(notSelBx,condTree)	#subtree not selected
	selTree = bg._mult(selTree, gv._classAcc)
	notSelTree = bg._mult(notSelTree, 1-gv._classAcc)
	selTree.update(notSelTree)
	return selTree



###########---------- huffman tree methods -------------##############

# left child > right child
def makeHuffTree(symbLst):
	#print len(symbLst)
	#print "##########"
	
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
	return dict( (item,tree[item]) for item in box)



# returns largest node in tree as [key,tree[key]]
def getLrgstLeaf(tree):
	maxProb = max(tree.values())
	print "maxProb:", maxProb
	return list(([key,tree[key]]) for key in tree if tree[key] == maxProb)



###########---------- methods to do with layout -------------##############

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
	startProbs = list((gv._currProbs[key],key) for key in gv._currProbs)
	#print "in default: startProbs:"
	#print startProbs
	#print ##
	gv._huffTree = makeHuffTree(startProbs)
	lTree = gv._huffTree[1]
	#print "lTree:", lTree
	rTree = gv._huffTree[2]
	#print "rTree:", rTree
	gv._box1 = layoutHuff(lTree,[])
	gv._box2 = layoutHuff(rTree,[])
	#print "box1:", gv._box1
	#print ###
	#print "box2:", gv._box2
	draw_interface(gv._canHt, gv._canWdth)



###############--------no longer used---------################

def set_layout(decision):
		#print "in set_layout()"
		#print symbList
		global gv, bg
		lTree = getLeaves(gv._huffTree[1], [])
		rTree = getLeaves(gv._huffTree[2], [])
		#print "ltree:", lTree
		updateProbs(decision,lTree,rTree)
		huffTree = makeHuffTree(lTree.append(rTree))
		layoutHuff(huffTree[0],huffTree[1])
		#print len(gv._box2)



##########---------------------start/test------------###########

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
		bool = random.choice(errArr)
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
	#print bg.bigrphLst
	
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



################------------------python main---------------########

root = Tk()
gv = GlobalVariables()
bg = Bigraph()
#bg._print(bg._bigrph1)
#bg._print(bg._bigrph2)
stack = Stack()

canvHeight = 300
canvWidth = 500
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
