from Tkinter import *
from sys import stdout, exit


root=Tk()
#geometry(width x height + xpos + ypos))
root.geometry('200x210+550+150')

class helloButton:
	def __init__(self,root):
		#wid = Label(root,bg='black')
		#wid.config(height=10,width=50)
		#butn = Button(wid,bg='red',padx=15,pady=15,relief=RAISED)
		#wid = Button(text='asdgj',command=(lambda: stdout.write('exiting\n') or self.quit()))
		#butn.pack(expand=NO)
		#wid.pack(expand=YES,fill=BOTH)

		canv = Canvas(width=300,height=300,bg='black')
		# 0,0 = upper left corner
		#creat_oval(from_x,from_y,to_x,to_y)
		canv.create_oval(50,50,150,150,fill='green',width=5)
		canv.pack(expand=YES,fill=BOTH)
		canv.after(3)
		canv.create_oval(50,50,150,150,fill='red',width=5)
		canv.pack(expand=YES,fill=BOTH)
	def quit(self):
		exit()

helloButton(root)
mainloop()


