# binspell - works with keyboard input - morse code language model
# left arrow = left   ::  right arrow = right
#
# last edit: 6/11
################CHANGES############
# 
# 
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
######################BUGS#######################
# import GlobalVariables doesn't work
# order in boxes after default layout, incorrect
##############CURRENTLY WORKING ON##########




from copy import deepcopy
from Tkinter import *
from math import *
from socket import *
from tkFont import *
import random, time, heapq
#import GlobalVariables



class GlobalVariables:
		_highlighted = 0
		_box1Freqs = []
		_box2Freqs = []
		_canvas = 0
		_txtBox = 0
		_currSymbList = []
		_nxtProb = 0
		_canHt = 0
		_canWdth = 0
		_lastTyped = ''
		_symbolFreq = [
			(0.124167  , 'e'),   
		   (0.0969225 , 't'),   
		   (0.0820011 , 'a'),   
		   (0.0768052 , 'i'),   
		   (0.0764055 , 'n'),   
		   (0.0714095 , 'o'),   
		   (0.0706768 , 's'),   
		   (0.0668132 , 'r'),   
		   (0.0448308 , 'l'),   
		   (0.0363709 , 'd'),   
		   (0.0350386 , 'h'),   
		   (0.0344391 , 'c'),   
		   (0.028777  , 'u'),   
		   (0.0281775 , 'm'),   
		   (0.0235145 , 'f'),   
		   (0.0203171 , 'p'),   
		   (0.0189182 , 'y'),   
		   (0.0181188 , 'g'),   
		   (0.0135225 , 'w'),   
		   (0.0124567 , 'v'),   
		   (0.0106581 , 'b'),   
		   (0.00393019, 'k'),   
		   (0.00219824, 'x'),   
		   (0.0019984 , 'j'),   
		   (0.0009325 , 'q'),   
		   (0.000599  , 'z')   
		]
		
		if False:
			_symbolFreq = [
				(8  , 'e'),   
				(6 , 't'),   
				(5 , 'a'),   
				(2 , 'i'),   
			]
		
			


def draw_square(x, y, h, w, brdr, tag):
	global gv
	gv._canvas.create_rectangle(x-w, y-h, x+w, y+h, width=brdr, tags=tag)
	
	

def draw_text(cntrx, cntry, h, w, symbolList):
	global gv
	
	print symbolList
	
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
		for item in symbolList:
			#print item
			if x+padx > cntrx+w-padx:
				x = cntrx - w
				y = y + pady + fontSz
				gv._canvas.create_text(x+padx, y+pady, text='\n', font=font)
			gv._canvas.create_text(x+padx, y+pady, text=item[1].upper(), font=font, tag='text')
			x = x + tab
		
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
	
	draw_text(cntrx_b1, cntry_b1, height, width, gv._box1Freqs)
	draw_text(cntrx_b2, cntry_b2, height, width, gv._box2Freqs)

	gv._canvas.update()		#process all events in event queue
	#time.sleep(1)
	
	
	
def update(decision):
	#print "in update_circs()"
	global gv
	#print "stack = ", stack
	
	left = 1
	right = 2

	
	if decision == left:
		gv._highlighted = left
		hilite = "box%i" %left
		norm = "box%i" %right
		if len(gv._box1Freqs) == 2:
			output(gv._box1Freqs[1])
			gv._box1Freqs = []
			gv._box2Freqs = []	
		get_layout(gv._box1Freqs)			
	else:	
		gv._highlighted = right
		hilite = "box%i" %right
		norm = "box%i" %left
		get_layout(gv._box2Freqs)			
	
	#print hilite	
	
	gv._canvas.itemconfigure(hilite,width=3)
	gv._canvas.itemconfigure(norm,width=1)
	gv._canvas.update()		#process all events in event queue			
	gv._canvas.delete('text')	
	draw_interface(gv._canHt,gv._canWdth)								
	gv._canvas.update()		#process all events in event queue				


def output(item):
	global gv
	#global gv._canvas, gv._txtBox
	
	##print "in output():"
	##print item[0]
	gv._txtBox.insert(INSERT,item)
	gv._lastTyped = item	
		
	if False:
		if item[0] == "SPC":
			gv._txtBox.insert(INSERT," ")
		elif item == "DEL":
			gv._txtBox.delete("%s-1c" % INSERT,INSERT)
		else:
			gv._txtBox.insert(INSERT,item[0])
	
	##print "2rd cursor pos:", gv._txtBox.index(INSERT)
	
	
def makeHuffTree(symbolTupleList):
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
	
	
def layout(huffTree):
	global gv

	if len(huffTree) == 2 and huffTree[0] == gv._nxtProb:
		gv._box1Freqs = huffTree
		#print huffTree[1]
		#steps[huffTree[1]] = prefix
		#print steps
	elif len(huffTree) == 2:
		gv._box2Freqs.insert(0,huffTree)
	else:
		layout(huffTree[1])
		layout(huffTree[2])
	
	
def defaultLayout():
	global gv
	
	symLst = list(gv._symbolFreq)
	heapq.heapify(symLst)
	
	for i in range(1,len(symLst)/2+1):
		gv._box2Freqs.insert(0,heapq.heappop(symLst))
		
	while symLst:
		gv._box1Freqs.insert(0,heapq.heappop(symLst))
	
	

def get_layout(symbList):
			#print "in get_layout()"
			global gv
			
			if symbList == []:
				if gv._lastTyped == '':
					defaultLayout()
				else:
					print 'bigrph'
			else:
				gv._box1Freqs = []
				gv._box2Freqs = []
				gv._nxtProb = max(dict(symbList).keys())
				huffTree = makeHuffTree(symbList)
				layout(huffTree)
				#print huffTree	
			#print gv._box1Freqs
			
				
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
		
		if event.keysym == 'Left':
			##print "key up"
			decision = 1	#select left
		if event.keysym == 'Right':
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
	x = 200
	y = 200
	r = 100
	tag = 'box1'
	width = 3
	
	draw_square(x,y,r,width,tag)
	#time.sleep(2)	#just to see initial interface
	##print "in test_interface()"
	numtries = 10
	if False:
		for i in range(1,numtries):
		##print "user input #",i
		##print "in test_interface: gv._highlighted=",gv._highlighted
			update(1)
			time.sleep(2)	




root = Tk()
gv = GlobalVariables
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

get_layout(gv._currSymbList)
draw_interface(canvHeight,canvWidth)

#testing
#test_interface()

#grab keyboard input
getKeyIn()

root.mainloop()
