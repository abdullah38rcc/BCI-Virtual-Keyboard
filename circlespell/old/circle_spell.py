# simple circlespell - works with keyboard input
# up arrow = select   ::  down arrow = rotate
#
# last edit: 4/26
################CHANGES############
# addition of global variables
# canvas text more legible
# cleaned up code a bit
# made txtBox the window focus
# blinking cursor
##########TODO##############
# tcp/ip socket
# simple language model based on letter frequency
# need to determine max_r2
# window resizable?
# window on top?
# undo if wrong circle is selected
# addition of phrases: menu of topics, add to first circle, how to layout phrases?
# diving bell and butterfly
# change window name
######################BUGS#######################
# 
##############CURRENTLY WORKING ON##########
# window focus: see line 309
# trying to position root window in center of screen


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
			
		num_letters = len(circle)
		
		#print "num_letters:",num_letters
		
		small_angle = ((2 * pi) / num_letters)

		#draw stuff in circle
		for j, letter in enumerate(circle):
			if num_letters > 1:		#space objects around circle
				letter_x_offset = 0.75 *  r2 * sin( small_angle * j)
				letter_y_offset = 0.75 * -r2 * cos( small_angle * j)
			else:	#center object
				letter_x_offset = 0
				letter_y_offset = 0

			canvas.create_text(x+x_offset+letter_x_offset, y+y_offset+letter_y_offset, text=letter, font="Courier 16 bold")
						
	canvas.update()		#process all events in event queue
	
	
	
def update(decision):
			#print "in update()"
			update_circs(decision,x,y,r1,max_r2)
			#print "after update_circs call: highlighted=",highlighted
			return
			

def update_circs(decision,x,y,r1,max_r2):
				#print "in update_circs()"
				global canvas, highlighted, circle_list, txtBox
				
				select = 1
				rotate = 0
				
				#print "decision =",decision
				#print "begin update_circs: highlighted:",highlighted
				
				if decision == select:
					#print "decision == select"
					circle_list = circle_list[highlighted]
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
					
					get_layout()	#arrange items in circles and determine next default highlighing
					
					#print "in update() circle_list after layout():", circle_list						
						
					draw_interface(x,y,r1,max_r2)
					
				else:	#decision = rotate
					#print "decision = rotate"
					item = "circ%s" %highlighted
					canvas.itemconfigure(item,width=1)
					
					#print item,": width=",canvas.itemcget(item,"width")
					
					highlighted = (highlighted + 1) % len(circle_list)
					item = "circ%s" %highlighted
					canvas.itemconfigure(item,width=3)
					
					#print item,": width=",canvas.itemcget(item,"width")
				
				canvas.update()		#process all events in event queue
				
									

def output(item):
	global canvas, txtBox
	
	#print "in output():"
		
	if item[0] == "SPC":
		txtBox.insert(INSERT," ")
	elif item[0] == "DEL":
		txtBox.delete("%s-1c" % INSERT,INSERT)
	else:
		txtBox.insert(INSERT,item[0])
	
	#print "2rd cursor pos:", txtBox.index(INSERT)
			
	

def get_layout():
			#print "in get_layout()"

			global highlighted, circle_list
			
			#use huffman to determine
			#highlighted = huffman()			
			highlighted = 0
			num_circles = 5
			
			#default screen
			num_items = len(circle_list)		#number objects to be distributed among circles
			if num_items == 0:
				#circle_list = ['DEL','SPC']
				circle_list = map(chr,range(97,123))
				circle_list.insert(0,'DEL')
				circle_list.insert(0,'SPC')
				num_items = len(circle_list)
				
				#print "circle_list in get_layout", circle_list
			
			if num_items < num_circles:
				num_circles = num_items
				
			max_circle_len = int(ceil(num_items / num_circles))			#max number items in each new  circle
			
			#print "max_circle_len in get_layout", max_circle_len
			#print "num_items after if in get_layout",num_items
			#print "circle_list in get_layout after if", circle_list
			
			new_circles = []
			index = 0
			
			#distribute objects in circles
			while len(new_circles) < num_circles:
				if len(new_circles) == (num_circles - 1):	#we're in last circle
					new_circles.append(circle_list[index:num_items])
				else:
					new_circles.append(circle_list[index:index+max_circle_len])
					index = index + max_circle_len				
					
				#print "circle_list[index:index+max_circle_len]",circle_list[index:index+max_circle_len]
				#print "new_circles before if",new_circles
				#print "index =",index
				#print "index+max_circle_len",index+max_circle_len
				#print "j =",j
			
			circle_list = new_circles
					
			
			
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
	#print "in getKeyIn()"
	#print event.keysym
	#decision = highlighted
	
	global canvas
	
	#print "in getKeyIn, highlighted=",highlighted
	
	def keyCtrl(event):
		#print "in keyCtrl()"
		#return "break"
		
		global circle_list, highlighted, txtBox
		
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

canvas = Canvas(root,height=400,width=400,bg='yellow')
canvas.grid(row=2,column=1)
#canvas.focus_set()

txtBox = Text(root,width=50,height=1,padx=5,pady=5,insertofftime=250,takefocus=1)
txtBox.grid(row=1,column=1)
txtBox.focus()
#txtBox.insert(INSERT,"hello")

highlighted = 0		#default highlited circle
circle_list = []
get_layout()
draw_interface(x,y,r1,max_r2)

#testing
#test_interface(highlighted,circle_list,txtBox)

#grab keyboard input
getKeyIn()

root.mainloop()
