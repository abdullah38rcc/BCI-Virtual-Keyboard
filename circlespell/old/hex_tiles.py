#create background hexagons
#last edit 4/14

from Tkinter import *
from math import *
#from array import *

def calc_h(s):
    h = sin(radians(60)) * s
    return (h)

def calc_r(s):
    r = cos(radians(60)) * s
    return(r)

def lin_len(x1,y1,x2,y2):
    l = sqrt( (x2-x1)**2 + (y2-y1)**2 )
    return l


def create_hex(s,win):
	
	h = abs( calc_h(s) )
	r = abs( calc_r(s) )
	h2 = abs(s*cos(30) )
	r2 = abs( s*sin(30) )
	a = 2 * h       #width of surrounding rect

	#print "test"
	#print "r=",r 
	#print "h=",h
	
	coords = []
	
	#bottom line
	blx = 175  #bottom left x coord
	coords.append(blx)	
	bly = 150  #bottom left y coord
	coords.append(bly)	
	brx = blx + s   #bottom rt xcoord
	coords.append(brx)	
	bry = bly  #bottom rt ycoord
	coords.append(bry)
	#botLn = win.create_line(blx,bly,brx,bry)
	botLn = win.create_line(coords)
	#print "coords=",coords
	coords = []

	#top line
	tplx = blx  #top lft xcoord
	coords.append(tplx)	
	tply = bly - a  #top lft ycoord
	coords.append(tply)	
	tprx = brx  #top rt xcoord
	coords.append(tprx)	
	tpry = bry - a  #top rt ycoord
	coords.append(tpry)	
	topLn = win.create_line(coords)
	#print "tpry=",tpry
	coords = []

	#top left diag line
	tdlx1 = tplx
	coords.append(tdlx1)	
	tdly1 = tply
	coords.append(tdly1)	
	tdlx2 = tplx - r
	coords.append(tdlx2)	
	tdly2 = tply + h 
	coords.append(tdly2)	
	tdLn = win.create_line(coords)
	#print "tdly2=",tdly2
	coords = []

	#bottom left diag line
	bldx1 = tdlx2
	coords.append(bldx1)	
	bldy1 = tdly2
	coords.append(bldy1)	
	bldx2 = blx
	coords.append(bldx2)	
	bldy2 = bly
	coords.append(bldy2)	
	bldLn = win.create_line(coords)
	coords = []

	#top right diag line
	trdx1 = tprx
	coords.append(trdx1)	
	trdy1 = tpry
	coords.append(trdy1)	
	trdx2 = trdx1 + r
	coords.append(trdx2)	
	trdy2 = trdy1 + h
	coords.append(trdy2)	
	trdLn = win.create_line(coords)
	coords = []
	
	#bottom right diag line
	brdx1 = trdx2
	coords.append(brdx1)	
	brdy1 = trdy2
	coords.append(brdy1)	
	brdx2 = brdx1 - r
	coords.append(brdx2)	
	brdy2 = brdy1 + h
	coords.append(brdy2)	
	brdLn = win.create_line(coords)
	
	#hex = win.create_polygon(coords)
