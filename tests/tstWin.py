import sys
from sys import *
#sys.path.append('/netopt/chimera/lib/python2.2/lib-dynload/')

from Tkinter import *
from SimpleDialog import SimpleDialog

# initialize GUI toolkit

#create pop-up window
root = Tk()

#w = Label(root,text="Next Letter")
#w.pack()  #size window to fit txt and display


# pop up a dialog window with some text
SimpleDialog(root,
             text="Hi there\nHere is some text",
             default=0,
             title="Demo Dialog").go()
