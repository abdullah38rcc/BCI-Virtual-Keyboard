from Tkinter import *
import time
#from sys import stdout,exit

print "b4 root"
root=Tk()
print "after root"

if False:
	#geometry(width x height + xpos + ypos))
	root.geometry('200x210+550+150')

	canv = Canvas(width=300,height=300,bg='black')
	# 0,0 = upper left corner
	#creat_oval(from_x,from_y,to_x,to_y)
	canv.pack(expand=YES,fill=BOTH)
	circ = canv.create_oval(50,50,150,150,fill='green',width=5)

	for ind in range(1,1):	
		#canv.after(20)
		time.sleep(3)
		canv.itemconfig(circ,fill='red')
		#canv.pack(expand=YES,fill=BOTH)
		#canv.after(3)
		time.sleep(3)
		canv.itemconfig(circ,fill='green')
		#stdout.write('changed oval')
mainloop()

