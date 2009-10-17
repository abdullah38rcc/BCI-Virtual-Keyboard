#!/usr/bin/python

from Tkinter import *

def Insert():
	name = text.get()
	list.insert(2, name)
	text.delete(0,END)	

root = Tk()
root.geometry('200x210+350+70')

text = Entry(root, bg = 'white')
button = Button(root, text = "press me", command = Insert)

list = Listbox(root, bg = 'blue', fg = 'yellow')


text.pack(anchor = W)
button.pack(padx = 4, pady = 4, anchor= E)

list.pack()


root.mainloop()
	
