# simple circlespell 
#	- works with keyboard input 
#	- alphabetical letters
#	- HMM
#	- moving hilite
# last edit: 11/10
########################## TO USE #############################
# up arrow = select   ::  down arrow = rotate  :: use undo if you overshoot a circle
################CHANGES############
# functions organized
# alphabetized keyboard
# hilite moves 
# set_highlighted()
##########TODO##############
# tcp/ip socket
# scan text and calculate freq
# need to determine max_r2
# window resizable?
# window on top?
# addition of phrases: menu of topics, add to first circle, how to layout phrases?
# diving bell and butterfly
# change window name
# window focus: see line 309
# position root window in center of screen
# do colors aid in text scanning?
# is class._doc_ writable?
# put del b4 spc in training version, then switch
# last rotation = selection
######################BUGS#######################
# 
##############CURRENTLY WORKING ON##########
# 



from copy import deepcopy
from Tkinter import *
from math import *
from socket import *
from tkFont import *
from GlobalVariables import *
from Bigraph import *
import time



##################################-------------drawing fxns---------------##########

def draw_circle(x, y, r, width, tag):
	global gv
	gv._canvas.create_oval(x-r, y-r, x+r, y+r, width=width, tags=tag)



def draw_interface(x, y, r1, max_r2):
	#print "in draw interface()"	
	#print "gv._circleList @beginning of draw_interface():",gv._circleList
	
	global gv
	
	num_circles = len(gv._circleList)
	##print "num_circles in draw_interface =",num_circles
	angle       = ((2 * pi) / num_circles)

	if num_circles > 1:
		r2          = min(r1 * sin(angle/2), max_r2)
	else:
		r2			= r1
	
	##print "in draw_interface gv._circleList:",gv._circleList
	
	# draw each circle
	for i, circle in enumerate(gv._circleList):
		##print "in for loop"
		##print "circle%i" %i, " contains:",circle
		
		#name each circle
		tag = "circ%s" %i
		
		if i == gv._highlighted:
			width    = 3
		else:
			width    = 1
			
		if num_circles > 1:
			x_offset =  r1 * sin( angle * i)
			y_offset = -r1 * cos( angle * i)
		else:
			x_offset = 0
			y_offset = 0

		draw_circle(x+x_offset, y+y_offset, r2, width, tag)
		
		##print "1st interface drawn:", tag, "width=",gv._canvas.itemcget(tag,"width")
		##print "circle:",circle," width:",width
		
		#if circle == 'DEL': #print "true!"
			
		if circle == 'DEL' or circle == 'SPC':
			gv._canvas.create_text(x+x_offset, y+y_offset, text=circle, font="Courier 16 bold")
		else:
			num_objs = len(circle)
		
			##print "num_objs:",num_objs
		
			small_angle = ((2 * pi) / num_objs)

			#draw stuff in circle
			for j, letter in enumerate(circle):
				if num_objs > 1:		#space objects around circle
					letter_x_offset = 0.75 *  r2 * sin( small_angle * j)
					letter_y_offset = 0.75 * -r2 * cos( small_angle * j)
				else:	#center object
					letter_x_offset = 0
					letter_y_offset = 0

				gv._canvas.create_text(x+x_offset+letter_x_offset, y+y_offset+letter_y_offset, text=letter.upper(), font="Courier 16 bold")
						
	##print "gv._circleList @end of draw_interface():",gv._circleList
	gv._canvas.update()		#process all events in event queue



#########################-------------functions dealing with state-------######

#set state vars to new vals
def reset():
	if gv._circleList == 'DEL':
		gv._charNum -= 1
	elif gv._circleList == 'SPC':
		gv._lastTyped = ''
		gv._charNum = 0
	else:
		gv._lastTyped = gv._circleList	
		gv._charNum += 1

	setCurrProbs()
	gv._circleList = []



def update(decision):
			global gv
			#global gv._circleList
			#print "in update()"
			##print "gv._circleList = ",gv._circleList

			gv._ttlNumSteps = gv._ttlNumSteps + 1		#for calculating itr

			update_circs(decision,x,y,r1,max_r2)
			##print "after update_circs call: gv._highlighted=",gv._highlighted



def update_circs(decision,x,y,r1,max_r2):
				global gv

				select = 1
				rotate = 0
				go_back = ['BACK']

				if decision == select:
					if gv._circleList[gv._highlighted] == go_back:
						gv._circleList=[]
						gv._circleList = pop()
					else:
						push(gv._circleList)
						gv._circleList = gv._circleList[gv._highlighted]
					if gv._circleList == 'DEL' or gv._circleList == 'SPC':
						num_circles = 1
					else:
						num_circles = len(gv._circleList)

					gv._canvas.delete('all')

					if num_circles == 1:   #single option left, must be user's choice
						output(gv._circleList)
						reset()
						gv._canvas.delete('all') #clear gv._canvas
						infoTransferRate()

					set_layout()	#arrange items in circles determine next default highlighing
					#gv._canvas.update()
					draw_interface(x,y,r1,max_r2)
				else:	#decision = rotate
					item = "circ%s" %gv._highlighted
					gv._canvas.itemconfigure(item,width=1)
					gv._highlighted = (gv._highlighted + 1) % len(gv._circleList)
					item = "circ%s" %gv._highlighted
					gv._canvas.itemconfigure(item,width=3)

				gv._canvas.update()		#process all events in event queue



#check for position in word and set probs accordingly
def setCurrProbs():
	global gv, bg
	#print "in setCurrProbs"
	if gv._lastTyped in bg._conditional1.keys():
		if gv._charNum > 1:		#more than one symbol typed b4 a space
			#print "more than one symbol typed"
			gv._currProbs = bg._conditional2[gv._lastTyped]
		elif gv._charNum > 0:	#single symbol typed b4 a space
			#print "single symbol typed:", gv._lastTyped
			gv._currProbs = bg._conditional1[gv._lastTyped]
	else:					#none typed yet b4 a space
		#print "nuthin typed yet"
		gv._currProbs = bg._prior



###########################################-----------------layout--------------##########################

#determine keyboard layout
def set_layout():
			#print "in set_layout()"
			global gv, bg
			#gv._highlighted = 0
			#num_circles = 5
			num_circles = 0
			#morseCode = [['SPC'],['DEL','e'],['i','t'],['s','a','n'],['h','u','r','d','m'],['w','g','v','l','f','b','k'],['o','p','j','x','c','z'],['y','q']]
			#spread out version of morse code
			#morseCode2 = [['SPC'],['DEL','e'],['i','t','s'],['a','n','h','u'],['r','d','m','w'],['g','v','l','f'],['b','k','o','p','j'],['x','c','z','y','q']]
						
			num_items = len(gv._circleList)		#number objects to be distributed among circles
			undo = ['BACK']

			#default screen
			if num_items == 0:
				setCircs()
			#elif gv._circleList[-1] != undo:
			elif num_items <= 4:
				#print "in setLayout: num_items:", num_items
				gv._circleList.append(undo)		#add "undo" circle to the set
				#print "stack after appending undo in set_layout= ",stack
			##print "stack @ end set_layout = ",stack			
			set_highlighted()	#determine highlighted circle



#arrange symbols in circles
def setCircs():
	global gv
	tmpLst = gv._sortByValue(gv._currProbs)
	tmpLst.sort()
	#print "tmpLst: ", tmpLst

	numSymbs = 2		#number of symbols in a circle to start with
	maxNumSymbs = 4		#max number of symbols in a circle
	circSymbs = ['DEL']	#start with circle2
	for item in tmpLst:
		#print item
		if len(circSymbs) >= numSymbs:
			numSymbs += 1
			if numSymbs > maxNumSymbs:
				numSymbs = maxNumSymbs
			gv._circleList.append(circSymbs)
			circSymbs = []
		circSymbs.append(item[0])
	gv._circleList.append(circSymbs)
	gv._circleList.insert(0,['SPC'])
	#print "gv._circleList:", gv._circleList
	#print "-" * 10



def set_highlighted():
	global gv
	tmpLst = gv._sortByValue(gv._currProbs)
	#print "in set_highlighted"
	#print "highest prob: ", tmpLst[0][0]
	#print gv._circleList
	for item in tmpLst:
		for symbSet in gv._circleList:
			#print symbSet
			if item[0] in symbSet:
				print "in set_highlighted"
				print "highest prob: ", item[0]
				gv._highlighted = gv._circleList.index(symbSet)
				return



################------------------stack fxns---------########

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



#####################################--------I/O------------########################

def output(item):
	#global gv._canvas, gv._txtBox
	#print #
	#print "in output():"
	#print item
	#print item[0]
	#print "-" * 10
	#print 'DEL' == item[0]
	#print #
		
	if item[0] == 'SPC':
		gv._txtBox.insert(INSERT," ")
	elif item == 'DEL' or item[0] == 'DEL':
		gv._txtBox.delete("%s-1c" % INSERT,INSERT)
	else:
		gv._txtBox.insert(INSERT,item[0])
	
	##print "2rd cursor pos:", gv._txtBox.index(INSERT)



#print out itr
def infoTransferRate():
	global gv
	#print "number of characters typed:", gv._charNum
	print "total number of steps taken: ", gv._ttlNumSteps
	print "information transfer rate: %.5f" %(float(gv._charNum) / (gv._ttlNumSteps * gv._trialLen)) + " chars/sec"
	print #



def getKeyIn():
	#print "in getKeyIn()"
	##print event.keysym
	#decision = gv._highlighted
	
	#global gv._canvas
	
	##print "in getKeyIn, gv._highlighted=",gv._highlighted
	
	def keyCtrl(event):
		##print "in keyCtrl()"
		#return "break"
		
		#global gv._circleList, gv._highlighted, gv._txtBox
		
		decision = 2
		
		##print "key pressed:",event.keysym
		
		if event.keysym == 'Up':
			##print "key up"
			decision = 1	#select
		if event.keysym == 'Down':
			##print "key down"
			decision = 0	#rotate
			
		##print "before update call"
		
		if decision < 2:
			update(decision)
					
		##print "after upddte call"
		##print "in keyCtrl gv._highlighted=", gv._highlighted
		
		return "break"
	
	##print "before bind call"
	
	gv._canvas.bind_all('<Key>',keyCtrl)
	
	#canv.bind_all('<Key-u>',keyCtrl)

	##print "end of getKeyIn"	
	



#####################################-------------test---------#################

def test_interface():
	time.sleep(2)	#just to see initial interface
	##print "in test_interface()"
	numtries = 10
	for i in range(1,numtries):
		##print "user input #",i
		##print "in test_interface: gv._highlighted=",gv._highlighted
		update(1)
		time.sleep(2)




##########################-------------------main-------------###########

root = Tk()
gv = GlobalVariables()
bg = Bigraph()

s = 50
x = 200
y = 200
r1 = 110 #radius of center circle
max_r2 = 80

#gv._circleList = []
stack = []

gv._canvas = Canvas(root,height=400,width=400,bg='yellow')
gv._canvas.grid(row=2,column=1)
#gv._canvas.focus_set()

gv._txtBox = Text(root,width=50,height=1,padx=5,pady=5,insertofftime=250,takefocus=1)
gv._txtBox.grid(row=1,column=1)
gv._txtBox.focus()
#gv._txtBox.insert(INSERT,"hello")

#print "hilite", gv._highlighted
#print "num steps:", gv._ttlNumSteps
gv._currProbs = bg._prior
set_layout()
draw_interface(x,y,r1,max_r2)

#testing
#test_interface(gv._highlighted,gv._circleList,gv._txtBox)

#grab keyboard input
getKeyIn()

root.mainloop()
