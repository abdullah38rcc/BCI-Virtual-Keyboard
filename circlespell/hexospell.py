# simple keyboard controlled hexospell implementation w/o language model
# last edit: 4/14

from Tkinter import *
from math import *
from hex_tiles import *

root = Tk()
s=50

win = Canvas(root,height=400,width=400,bg='yellow')
win.grid()

#circle w/ r=50
circ_id = win.create_oval(150,150,250,250,width=1,tags='circ')
#arrow_id = win.create_line(200,200,225,225,width=2,tags='arrow')

create_hex(s,win)

#hexagon w/ s=50
#hex1_id = win.create_polygon(175,150,225,150,225+r,150-h,175-r,150-h,175,150-(2*h),225,150-(2*h),width=2,tags='hex1')
#id = win.create_line(225,150,225+r,150-h)  #bottm,rt,diag
#id3 = win.create_line(175,150,175+s,150)   #bottm
#id4 = win.create_line(175,150,175-r,150-h)   #bottm,lft,diag
#id2 = win.create_line(175-r,150-h,175,150-h-h2)   #lft,upper,diag
#id5 = win.create_line(225+r,150-h,225,150-h-h2)   #upper,rt,diag
#id6 = win.create_line(175,150-h-h2,225,150-h-h2)  #top
#id6 = win.create_line(175,150-a,175+s,150-a)  #correct top


#coords = win.bbox(id)
#print coords
#print 225+h,", ",150-r
#len = lin_len(175,150,175,150-h-h2)
#len = lin_len(tdlx1, tdly1, tdlx2, tdly2)
#print "len=",len
#print "a=",a


#line1 = win.create_line(150,150,250,250)
#arc_id = win.create_arc(175,150,250,250)

root.mainloop()
