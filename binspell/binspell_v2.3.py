# binspell - works with keyboard input - morse code language model
# up arrow = left   ::  down arrow = right
#
# last edit: 6/21
################CHANGES############
# classes work
# changed get_layout to set_layout
# works with up and down keys
# brackets around spc and del
# SPC works
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
# add check for empty selected box
# huffTop3
######################BUGS#######################
# order in boxes after default layout, incorrect
# cursor moving incorrectly
##############CURRENTLY WORKING ON##########




from copy import deepcopy
from Tkinter import *
from math import *
from socket import *
from tkFont import *
import random, time, heapq
from GlobalVariables_v2 import *
from Bigraph import *




def draw_square(x, y, h, w, brdr, tag):
	global gv
	gv._canvas.create_rectangle(x-w, y-h, x+w, y+h, width=brdr, tags=tag)
	
	


def draw_text(cntrx, cntry, h, w, symbolList):
	global gv, bgrph

	#print symbolList
	#print ###########

	fontSz = 30
	font = 'Courier %i bold' %fontSz
	x = cntrx - w
	y = cntry - h

	padx = w/7
	pady = h/10
	tab = 30

	if len(symbolList) == 2:
		gv._canvas.create_text(cntrx, cntry, text=symbolList[1].upper(), font=font, tag='text')
	else:
		if bgrph._suggSymbList != []:
			for item in bgrph._suggSymbList:
				#print "in bgrph._suggSymbList, item:", item
				if x+padx > cntrx+w-padx:   #goin past the edge
					x = cntrx - w   #reset x to rt edge
					y = y + pady + fontSz   #\n
					gv._canvas.create_text(x+padx, y+pady, text='\n', font=font)
				gv._canvas.create_text(x+padx, y+pady, text=item[0].upper(), font=font, tag='text',fill='red')
				x = x + tab
				#print "len(item[0]):", len(item[0])
				if len(str(item[0])) > 1:
					x = x + fontSz * len(item[0])

		#print "symbolList", symbolList
		#print ###########

		if '[DEL]' not in symbolList[1] and '[SPC]' not in symbolList[1]:
			setNxtProbHuff(symbolList)

		for item in symbolList:
			#print item[1]
			#print "len(str(item[1])):", len(item[1])		
			if item not in bgrph._suggSymbList:  #no redundant chars
				if len(str(item[1])) > 1:  #SPC or DEL, etc
					color = 'green'
					fontSz = 20
					font = 'Courier %i bold' %fontSz
					xtraSymbSpace = len(str(item[1])) * fontSz/2
					pos = 'w'
				else:
					fontSz = 30
					font = 'Courier %i bold' %fontSz
					color = 'black'	
					pos = 'center'
					xtraSymbSpace = 0

				if gv._huffSuggest in item:
					color = 'blue'
					
				if x + padx + xtraSymbSpace > cntrx + w - padx:   #goin past the edge
					x = cntrx - w   #reset x to rt edge
					y = y + pady + fontSz   #\n
					gv._canvas.create_text(x+padx, y+pady, text='\n', font=font)
					
				gv._canvas.create_text(x+padx, y+pady, text=item[1].upper(), font=font, tag='text', fill=color, anchor=pos)
				x = x + tab + xtraSymbSpace
		
		#decreasing font size
		#fontSz = fontSz - 2
		#font = 'Courier %i bold' %fontSz
		
		


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
	draw_text(cntrx_b1, cntry_b1, height, width, gv._box1Freqs)
	#print "drawing box2"
	draw_text(cntrx_b2, cntry_b2, height, width, gv._box2Freqs)

	gv._canvas.update()		#process all events in event queue
	#time.sleep(1)
	
	
	
def update(decision):
	#print "in update_circs()"
	global gv, bgrph
	#print "stack = ", stack
	
	left = 1
	right = 2

	
	if decision == left:
		gv._highlighted = left
		hilite = "box%i" %left
		norm = "box%i" %right
		if len(gv._box1Freqs) == 2:
			#print gv._box1Freqs
			output(gv._box1Freqs[1])
			gv._box1Freqs = []
			gv._box2Freqs = []
			bgrph._setSuggSymbList(gv._lastTyped)
		set_layout(gv._box1Freqs)			
		#print "gv._box1Freqs:", gv._box1Freqs
		#print "gv._box2Freqs:", gv._box2Freqs
	else:	
		gv._highlighted = right
		hilite = "box%i" %right
		norm = "box%i" %left
		set_layout(gv._box2Freqs)			
	
	#print "hilite:", hilite	
	#print "norm", norm
	
	gv._canvas.itemconfigure(hilite,width=3)
	gv._canvas.itemconfigure(norm,width=1)
	#gv._canvas.update()		#process all events in event queue			
	gv._canvas.delete('text')	
	#set_layout(gv._box1Freqs)
	draw_interface(gv._canHt,gv._canWdth)								
	gv._canvas.update()		#process all events in event queue				


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
	
	
def makeHuffTree(symbolTupleList):
	#print len(symbolTupleList)
	#print "##########"
	
	trees = list(symbolTupleList)
	heapq.heapify(trees)
	while len(trees) > 1:
		childR, childL = heapq.heappop(trees), heapq.heappop(trees)
		#print "childL:",childL
		#print "childR",childR
		#print "##########"
		parent = (childL[0] + childR[0], childL, childR)
		#print "parent:", parent
		#print "##########"
		heapq.heappush(trees, parent)

	return trees[0]
	
	
def layoutHuff(huffTree, nxtProbSymb):
	global gv
	#print huffTree
	#print "#############"

	if len(huffTree) == 2:
		if nxtProbSymb in huffTree:
			gv._box1Freqs = huffTree
		else:
			#print huffTree
			gv._box2Freqs.insert(0,huffTree)
	else:
		layoutHuff(huffTree[1],nxtProbSymb)
		layoutHuff(huffTree[2],nxtProbSymb)
	
	
def defaultLayout():
	global gv
	
	symLst = list(gv._symbolFreqList)
	heapq.heapify(symLst)
	
	for i in range(1,len(symLst)/2+1):
		gv._box2Freqs.insert(0,heapq.heappop(symLst))
		
	while symLst:
		gv._box1Freqs.insert(0,heapq.heappop(symLst))
		if '[SPC]' in gv._box1Freqs[0] or '[DEL]' in gv._box1Freqs[0]:
			del gv._box1Freqs[0]		
		
		
		
def setNxtProbHuff(symbList):
	global gv, bgrph
	symbDict = dict(symbList)
	if gv._suggested != '':
		#print "gv._suggested:", gv._suggested
		#print "gv._swappdSymbFreqDict:", gv._swappdSymbFreqDict
		#print "gv._swappdSymbFreqDict['a']:", gv._swappdSymbFreqDict['a']
		val = gv._swappdSymbFreqDict[gv._suggested]
		#print val
		if val in symbDict:
			del symbDict[val]
	if bgrph._suggSymbList != '':
		for item in bgrph._suggSymbList:
			#print "item in bgrph._suggSymbList:", item
			if item[1] in symbDict:
				del symbDict[item[1]]
	
	nxtProb = max(symbDict.keys())
	gv._huffSuggest = symbDict[nxtProb]
	
	

def set_layout(symbList):
	#print "in set_layout()"
	#print symbList
	global gv, bgrph
	
	if gv._lastTyped == '':  #nuthin typed yet
		gv._box2Freqs = []
		gv._box1Freqs = []
		
		setNxtProbHuff(symbList)  #set gv._huffSuggest
		
		huffTree = makeHuffTree(symbList)
		layoutHuff(huffTree,gv._huffSuggest)
		#print huffTree
	else:  
		#print "old gv._suggested:", gv._suggested
		#print "gv._lastTyped:", gv._lastTyped
		gv._box2Freqs = []
		gv._suggested = bgrph._nxtProb(gv._lastTyped,gv._suggested)
	
		#print "new gv._suggested:", gv._suggested
		if symbList == []:
			#print "using whole list for box2"
			symbList = gv._symbolFreqList
	
		if gv._suggested == '':  #nuthin in bigraph list
			#print symbList
			tmpDict = dict(symbList)
			gv._suggested = dict(symbList)[max(tmpDict.keys())]
				
		huffTree = makeHuffTree(symbList)
		layoutHuff(huffTree,gv._suggested)
		#print len(gv._box2Freqs)
			
			
			
				
def push(item):
	#print "in push()"
	#global stack
	#global circle_list
	itemCpy = deepcopy(item)
	stack.append(itemCpy)
	##print "stack after append = ", stack

def pop():
	#print "in pop()"
	#global stack, circle_list
	
	if stack != []:
		s = stack.pop()
	#s = stack[len(stack)-1]
	##print s," has been popped"
		return s
	#return stack.pop()

		

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
			
		if False:
			#simulate misclassification
			bool = random.choice(errArr)
			if bool == 0:
				decision = abs(decision - 1)
		
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
	print nxtProb(gv.lastTyped)
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
	defaultLayout()
	draw_interface(canvHeight,canvWidth)

	#grab keyboard input
	getKeyIn()





root = Tk()
gv = GlobalVariables()
bgrph = Bigraph()

#print gv._canWdth

canvHeight = 300
canvWidth = 500
gv._canHt = canvHeight
gv._canWdth = canvWidth
txtBxWidth = canvWidth / 8
txtBxHeight = 1

#gv._boxList = []
stack = []

gv._canvas = Canvas(root,height=canvHeight,width=canvWidth,bg='yellow')
gv._canvas.grid(row=2,column=1)
#gv._canvas.focus_set()

gv._txtBox = Text(root,width=txtBxWidth,height=txtBxHeight,padx=5,pady=5,insertofftime=250,takefocus=1)
gv._txtBox.grid(row=1,column=1)
gv._txtBox.focus()
#gv._txtBox.insert(INSERT,"hello")

#print gv._highlighted
#print gv._currSymbList

start()
#testing
#test_interface()

root.mainloop()
