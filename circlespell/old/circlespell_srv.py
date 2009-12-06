# simple circlespell implementation w/ testing code
# last edit: 4/20
##########TODO##############
#bug?: after last update call, none of the circles are highlighted - see test_interface, numtries = 6
#need to determine max_r2
#window on top
##############CURRENTLY WORKING ON##########
#redrawing screen after text output
#make interface main focus



from Tkinter import *
from math import *
from socket import *
import time

def draw_circle(canvas, x, y, r, width, tag):
	return canvas.create_oval(x-r, y-r, x+r, y+r, width=width, tags=tag)



def draw_interface(canvas, x, y, r1, max_r2, highlighted, circle_list, txtBox):
	print "in draw interface()"	
	num_circles = len(circle_list)
	#print "num_circles in draw_interface =",num_circles
	angle       = ((2 * pi) / num_circles)

	if num_circles > 1:
		r2          = min(r1 * sin(angle/2), max_r2)
	else:
		r2			= r1
	
	# draw big circle
	# draw_circle(canvas, x, y, r1)
	#print "highlighted=",highlighted
	
	# draw each circle
	for i, circle in enumerate(circle_list):
		#print "in for loop"
		
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

		draw_circle(canvas, x+x_offset, y+y_offset, r2, width, tag)
		#print "1st interface drawn:", tag, "width=",canvas.itemcget(tag,"width")
		
		#print "circle:",circle," width:",width
			
		num_letters = len(circle)
		small_angle = ((2 * pi) / num_letters)

		#draw stuff in circle
		for j, letter in enumerate(circle):
			if num_letters > 1:		#space objects around circle
				letter_x_offset = 0.75 *  r2 * sin( small_angle * j)
				letter_y_offset = 0.75 * -r2 * cos( small_angle * j)
			else:	#center object
				letter_x_offset = 0
				letter_y_offset = 0

			canvas.create_text(x+x_offset+letter_x_offset, y+y_offset+letter_y_offset, text=letter)
						
	canvas.update()		#process all events in event queue
			
def update(decision,highlighted,circle_list,txtBox):
			print "in update()"
			circle_list,highlighted = update_circs(decision,win,x,y,r1,max_r2,highlighted,circle_list,txtBox)
			print "after update_circs call: highlighted=",highlighted
			return circle_list,highlighted
			

def update_circs(decision,canvas,x,y,r1,max_r2,highlighted,circle_list,txtBox):
				print "in update_circs()"
				select = 1
				rotate = 0
				
				#print "decision =",decision
				print "begin update_circs: highlighted:",highlighted
				
				if decision == select:
					print "decision == select"
					circle_list = circle_list[highlighted]
					num_circles = len(circle_list)
					
					#clear screen
					canvas.delete('all')
					
					if num_circles == 1:   #single option left, must be user's choice
						#print "num_circles == 1"
						txtBox = output(circle_list,txtBox)
						print circle_list						
					else:
						#print "circle_list b4 get_layou() call:",circle_list
						#arrange items in circles and determine next default highlighing
						circle_list,highlighted = get_layout(circle_list,highlighted)
						
					draw_interface(canvas,x,y,r1,max_r2,highlighted,circle_list,txtBox)
					
				else:	#decision = rotate
					print "decision = rotate"
					item = "circ%s" %highlighted
					canvas.itemconfigure(item,width=1)
					print item,": width=",canvas.itemcget(item,"width")
					highlighted = highlighted + 1
					item = "circ%s" %highlighted
					canvas.itemconfigure(item,width=3)
					print item,": width=",canvas.itemcget(item,"width")
				
				canvas.update()		#process all events in event queue
				#txtBox.update()
				print "end of update_circs: highlighted =",highlighted
				return circle_list,highlighted
					

def output(item,txtBox):
	print "in output_canvas"
	#item = "%s" %item		#formatting
	txtBox.insert(INSERT,item[0])
	return txtBox
	#if txt widget
	#	add text
	#else
		
	

def get_layout(circle_items,highlighted):
			print "in get_layout()"
			#default screen
			#later change according to text in output
			num_items = len(circle_items)		#number objects to be distributed among circles
			if num_items == 0:
				circle_items = map(chr,range(97,123))
				num_items = len(circle_items)
				#print "circle_items in get_layout", circle_items
			
			#use huffman to determine
			#highlighted = huffman
			num_circles = 5
			max_circle_len = int(ceil(num_items / num_circles))				#max number items in each new  circle
			#print "max_circle_len in get_layout", max_circle_len
			#print "num_items after if in get_layout",num_items
			#print "circle_items in get_layout after if", circle_items
			new_circles = []
			index = 0
			
			#distribute objects in circles
			while len(new_circles) < num_circles:
				if len(new_circles) == (num_circles - 1):	#we're in last circle
					new_circles.append(circle_items[index:num_items])
				else:
					new_circles.append(circle_items[index:index+max_circle_len])
					index = index + max_circle_len				
				#print "circle_items[index:index+max_circle_len]",circle_items[index:index+max_circle_len]
				#print "new_circles before if",new_circles
				#print "index =",index
				#print "index+max_circle_len",index+max_circle_len
				#print "j =",j

				
			return new_circles, highlighted
			
			
			
def test_interface(highlighted,circle_list,txtBox):
	time.sleep(2)	#just to see initial interface
	print "in test_interface()"
	numtries = 3
	for i in range(1,numtries):
		print "user input #",i
		print "in test_interface: highlighted=",highlighted
		circle_list,highlighted = update(1,highlighted,circle_list,txtBox)
		time.sleep(2)
		

def getKeyIn(event):
	print "in getKeyIn()"
	#print event.keysym
	if event.keysym == 'Up':
		print "key up"
		decision = 1	#select
	if event.keysym == 'Down':
		print "key down"
		decision = 0	#rotate
	
			


root = Tk()
s = 50
x = 200
y = 200
r1 = 110
max_r2 = 80

# Set the socket parameters
host = "localhost"
port = 21567
buf = 1024
addr = (host,port)

win = Canvas(root,height=400,width=400,bg='yellow')
win.grid(row=2,column=1)

txt_box = Text(root,width=50,height=1,padx=5,pady=5)
txt_box.grid(row=1,column=1)
#txt_box.insert(INSERT,"hello")

highlighted = 0		#default highlited circle
circle_list = []
circle_list, highlighted = get_layout(circle_list,highlighted)

#print "b4 binding"

# Create socket and bind to address
#UDPSock = socket(AF_INET,SOCK_DGRAM)
#UDPSock.bind(addr)


draw_interface(win,x,y,r1,max_r2, highlighted, circle_list,txt_box)
#draw_interface(win, 200,200, 110, 80, 0, [["F"], ["G"], ["H"]])
#win.create_text(200,200, text="M")


#testing
#test_interface(highlighted,circle_list,txt_box)

#grab keyboard input
root.bind_all('<KeyPress>',getKeyIn)	


#print "in sock server key:"

# Receive messages
#while 1:
#	data,addr = UDPSock.recvfrom(buf)
 #	print data
#	update(data)
#	if data == '0':
#		break

# Close socket
#UDPSock.close()

root.mainloop()
