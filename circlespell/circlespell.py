
# last edit: 4/14

from Tkinter import *
from math import *

def draw_circle(canvas, x, y, r, width=1):
	return canvas.create_oval(x-r, y-r, x+r, y+r, width=width)


#####need to determine max_r2
def draw_interface(canvas, x, y, r1, max_r2, highlighted, circle_list):
		
	num_circles = len(circle_list)
	#print "num_circles in draw_interface =",num_circles
	angle       = ((2 * pi) / num_circles)

	if num_circles > 1:
		r2          = min(r1 * sin(angle/2), max_r2)
	else:
		r2			= r1
	
	# draw big circle
	# draw_circle(canvas, x, y, r1)
	
	# draw each circle
	for i, circle in enumerate(circle_list):
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

		draw_circle(canvas, x+x_offset, y+y_offset, r2, width)
			
		num_letters = len(circle)
		small_angle = ((2 * pi) / num_letters)

		#draw stuff in circle
		for j, letter in enumerate(circle):
			if num_letters > 1:
				letter_x_offset = 0.75 *  r2 * sin( small_angle * j)
				letter_y_offset = 0.75 * -r2 * cos( small_angle * j)
			else:
				letter_x_offset = 0
				letter_y_offset = 0

			canvas.create_text(x+x_offset+letter_x_offset, y+y_offset+letter_y_offset, text=letter)
			
			
def update(decision):
			update_circs(decision,canvas,x,y,r1,max_r2,highlighted,circle_list)
			

def update_circs(decision,canvas,x,y,r1,max_r2,highlighted,circle_list):
				select = 1
				rotate = 0
				
				if decision == select:
					circle_list = circle_list[highlighted]
					num_circles = len(circle_list)
					
					if num_circles == 1:
						#output(circle_list)
						#print circle_list
						num = num_circles
					else:
						#arrange items in circles and determine next default highlighing
						circle_list,highlighted = get_layout(circle_list,highlighted)
						draw_interface(canvas,x,y,r1,max_r2,highlighted,circle_list)
						

def get_layout(circle_items,highlighted):
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
			


root = Tk()
s = 50
x = 200
y = 200
r1 = 110
max_r2 = 80

win = Canvas(root,height=400,width=400,bg='yellow')
win.grid()

highlighted = 0		#default highlited circle
circle_list = []
circle_list, highlighted = get_layout(circle_list,highlighted)


draw_interface(win,x,y,r1,max_r2, highlighted, circle_list)
#draw_interface(win, 200,200, 110, 80, 0, [["F"], ["G"], ["H"]])
#win.create_text(200,200, text="M")

root.mainloop()
