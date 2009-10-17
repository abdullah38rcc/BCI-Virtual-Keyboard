#!/usr/bin/env python

from Tkinter import *
import tkMessageBox
import sys

def show_alert() :
    root.bell()
    tkMessageBox.showinfo("Ready!", "DING DING DING!")
    sys.exit()

def start_timer() :
    # Next line should be * 60000, but use 1000 to speed debugging:
    root.after(scale.get() * 1000, show_alert)


root = Tk()

minutes = Label(root, text="Minutes:")
minutes.grid(row=0,column=0)

scale = Scale(root, from_=1, to=45, orient=HORIZONTAL, length=300)
scale.grid(row=0, column=1)

button = Button(root, text="start timing", command=start_timer)
button.grid(row=1, column=1, pady=5, sticky=E)

root.mainloop()
