# simple circlespell - works with keyboard input - morse code language model
# up arrow = select   ::  down arrow = rotate
#
# last edit: 5/12
################CHANGES############
# added morse code letter arrangment to default gui
# hacks to make 'del' show up as one word
# undo circle -- 'BACK'
##########TODO##############
# tcp/ip socket
# scan text and calculate freq
# need to determine max_r2
# window resizable?
# window on top?
# rewrite into classes
# addition of phrases: menu of topics, add to first circle, how to layout phrases?
# diving bell and butterfly
# change window name
# window focus: see line 309
# position root window in center of screen
# do colors aid in text scanning?
######################BUGS#######################

##############CURRENTLY WORKING ON##########
# min_steps.py



from Tkinter import *
from math import *
from socket import *
from tkFont import *
import time

def draw_circle(x, y, r, width, tag):
	global canvas
	canvas.create_oval(x-r, y-r, x+r, y+r, width=width, tags=tag)



def draw_interface(x, y, r1, max_r2):
	#print "in draw interface()"	
	#print "circle_list @beginning of draw_interface():",circle_list
	
	global canvas, highlighted, circle_list, txtBox
	
	num_circles = len(circle_list)
	#print "num_circles in draw_interface =",num_circles
	angle       = ((2 * pi) / num_circles)

	if num_circles > 1:
		r2          = min(r1 * sin(angle/2), max_r2)
	else:
		r2			= r1
	
	#print "in draw_interface circle_list:",circle_list
	
	# draw each circle
	for i, circle in enumerate(circle_list):
		#print "in for loop"
		#print "circle%i" %i, " contains:",circle
		
		#name each circle
		tag = "circ%s" %i
		
		if i == highlighted:
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
		
		#print "1st interface drawn:", tag, "width=",canvas.itemcget(tag,"width")
		#print "circle:",circle," width:",width
		
		#if circle == 'DEL': print "true!"
			
		if circle == 'DEL' or circle == 'SPC':
			canvas.create_text(x+x_offset, y+y_offset, text=circle, font="Courier 16 bold")
		else:
			num_objs = len(circle)
		
			#print "num_objs:",num_objs
		
			small_angle = ((2 * pi) / num_objs)

			#draw stuff in circle
			for j, letter in enumerate(circle):
				if num_objs > 1:		#space objects around circle
					letter_x_offset = 0.75 *  r2 * sin( small_angle * j)
					letter_y_offset = 0.75 * -r2 * cos( small_angle * j)
				else:	#center object
					letter_x_offset = 0
					letter_y_offset = 0

				canvas.create_text(x+x_offset+letter_x_offset, y+y_offset+letter_y_offset, text=letter, font="Courier 16 bold")
						
	#print "circle_list @end of draw_interface():",circle_list
	canvas.update()		#process all events in event queue
	
	
	
def update(decision):
			#global circle_list
			print "in update()"
			#print "circle_list = ",circle_list
			update_circs(decision,x,y,r1,max_r2)
			#print "after update_circs call: highlighted=",highlighted
			return
			

def update_circs(decision,x,y,r1,max_r2):
				print "in update_circs()"
				global canvas, highlighted, circle_list, txtBox
				print "stack = ", stack
				
				select = 1
				rotate = 0
				undo = ['BACK']
				
				
				#print "decision =",decision
				#print "begin update_circs: highlighted:",highlighted
				
				if decision == select:
					print "decision == select"
					#print "in update_circs(): selected =", circle_list[highlighted]
					print "stack = ",stack
					
					if circle_list[highlighted] == undo:
						print "back selected"
						#print "circle_list b4 pop", circle_list
						print "stack = ",stack
						circle_list=[]
						circle_list = pop()
						#print "circle_list in update_circs after pop()",circle_list
						print "stack after pop()",stack
					else:
						print "back not selected"
						#print "in update_circs, circle_list b4 pushing", circle_list
						print "stack b4 push() = ",stack
						push(circle_list)
						circle_list = circle_list[highlighted]
						print "in update_circs, new circle_list after pushing", circle_list
						print "stack = ",stack
						#print "in update_circs(): selected =", circle_list
					
					if circle_list == 'DEL' or circle_list == 'SPC':
						num_circles = 1
					else:
						num_circles = len(circle_list)
					
					#clear screen
					canvas.delete('all')
					
					if num_circles == 1:   #single option left, must be user's choice
						#print "num_circles == 1"
						output(circle_list)
						circle_list = []
						canvas.delete('all') #clear canvas
					
					#print "circle_list before layout():", circle_list						
					#print "in update() circle_list b4 get_layou() call:",circle_list
					print "stack right b4 get_layout",stack
					get_layout()	#arrange items in circles and determine next default highlighing
					canvas.update()
					print "in update() circle_list after layout():", circle_list						
					print "stack after get_layout = ",stack	
					draw_interface(x,y,r1,max_r2)
					
				else:	#decision = rotate
					print "decision = rotate"
					print "stack = ",stack
					item = "circ%s" %highlighted
					canvas.itemconfigure(item,width=1)
					
					#print item,": width=",canvas.itemcget(item,"width")
					
					highlighted = (highlighted + 1) % len(circle_list)
					item = "circ%s" %highlighted
					canvas.itemconfigure(item,width=3)
					
					#print item,": width=",canvas.itemcget(item,"width")
					canvas.update()		#process all events in event queue
				
									

def output(item):
	#global canvas, txtBox
	
	#print "in output():"
	#print item[0]
		
	if item[0] == "SPC":
		txtBox.insert(INSERT," ")
	elif item == "DEL":
		txtBox.delete("%s-1c" % INSERT,INSERT)
	else:
		txtBox.insert(INSERT,item[0])
	
	#print "2rd cursor pos:", txtBox.index(INSERT)
			
	

def get_layout():
			print "in get_layout()"

			global highlighted, circle_list
			#print "circle_list:",circle_list
			print "stack @ beginning get_layout",stack
			
			#use huffman to determine
			#highlighted = huffman()			
			highlighted = 0
			#num_circles = 5
			num_circles = 0
			morseCode = [['SPC'],['DEL','e'],['i','t'],['s','a','n'],['h','u','r','d','m'],['w','g','v','l','f','b','k'],['o','p','j','x','c','z'],['y','q']]
						
			num_items = len(circle_list)		#number objects to be distributed among circles
			undo = ['BACK']
			
			#default screen
			if num_items == 0:
				print "default screen"
				print "stack = ",stack
				#circle_list = ['DEL','SPC']
				#circle_list = map(chr,range(97,123))
				circle_list = morseCode
				#circle_list.insert(0,'DEL')
				#circle_list.insert(0,'SPC')
				#circle_list.insert(1,['DEL','SPC'])
				num_items = len(circle_list)
				
			elif circle_list[num_items-1] != undo:
				print "in get_layout: last circle:",circle_list[num_items-1]
				print "stack = ",stack
				#print circle_list[0]
				#print len(circle_list)
				circle_list.append(undo)		#add "undo" circle to the set
				print "stack after appending undo in get_layout= ",stack
			#print "stack @ end get_layout = ",stack			
			

	
def push(item):
	print "in push()"
	#global stack
	#global circle_list
	print "circle_list b4 append", circle_list
	print "stack b4 append", stack
	itemCpy = deepcopy(item)
	stack.append(itemCpy)
	print "stack after append = ", stack
	
def pop():
	print "in pop()"
	#global stack, circle_list
	print "circle_list b4 pop", circle_list
	if stack != []:
		s = stack.pop()
	#s = stack[len(stack)-1]
	print "circle_list after pop()", circle_list
	print s," has been popped"
	return s
	#return stack.pop()


def test_interface():
	time.sleep(2)	#just to see initial interface
	#print "in test_interface()"
	numtries = 10
	for i in range(1,numtries):
		#print "user input #",i
		#print "in test_interface: highlighted=",highlighted
		update(1)
		time.sleep(2)
		

def getKeyIn():
	print "in getKeyIn()"
	#print event.keysym
	#decision = highlighted
	
	#global canvas
	
	#print "in getKeyIn, highlighted=",highlighted
	
	def keyCtrl(event):
		#print "in keyCtrl()"
		#return "break"
		
		#global circle_list, highlighted, txtBox
		
		decision = 2
		
		#print "key pressed:",event.keysym
		
		if event.keysym == 'Up':
			#print "key up"
			decision = 1	#select
		if event.keysym == 'Down':
			#print "key down"
			decision = 0	#rotate
			
		#print "before update call"
		
		if decision < 2:
			update(decision)
					
		#print "after upddte call"
		#print "in keyCtrl highlighted=", highlighted
		
		return "break"
	
	#print "before bind call"
	
	canvas.bind_all('<Key>',keyCtrl)
	
	#canv.bind_all('<Key-u>',keyCtrl)

	#print "end of getKeyIn"	
	

root = Tk()
s = 50
x = 200
y = 200
r1 = 110 #radius of center circle
max_r2 = 80
highlighted = 0		#default highlited circle
circle_list = []
stack = []

canvas = Canvas(root,height=400,width=400,bg='yellow')
canvas.grid(row=2,column=1)
#canvas.focus_set()

txtBox = Text(root,width=50,height=1,padx=5,pady=5,insertofftime=250,takefocus=1)
txtBox.grid(row=1,column=1)
txtBox.focus()
#txtBox.insert(INSERT,"hello")

get_layout()
draw_interface(x,y,r1,max_r2)

#testing
#test_interface(highlighted,circle_list,txtBox)

#grab keyboard input
getKeyIn()

root.mainloop()
