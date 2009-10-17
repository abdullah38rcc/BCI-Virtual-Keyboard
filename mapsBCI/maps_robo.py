# a robot simulation of robot that moves into a room and looks around, taking note of obstacles
# last edit: 5/24
##########TODO##############
# lambda expressions for case-swtich/dictionary
# maps algorithm
# argument to drawRoom() to specify num obastacles
# in drawObstacles() randomly place objects in room
#	             check for max obstacle size
# add camera
# rotate object
#    - see RotCanvas.pm
######################BUGS#######################
# robot dissapears
##############CURRENTLY WORKING ON##########
# obstacle detection/avoidance
# 

from Tkinter import *
from math import *
import time

#how can i pass angle into instantiation
class RotMatrx:   #rotation matrix  (counterclockwise)
	#def _init_(self,angle):
		#self.angle = angle
	angle = 0
	#data = [[cos(radians(angle)), -sin(radians(angle))],[sin(radians(angle)),cos(radians(angle))]]
	#data = [[cos(angle), -sin(angle)],[sin(angle),cos(angle)]]
	data = [[0,-1],[1,0]]

def getKeyIn():
	#print "in getKeyIn()"
	global canvas
		
	def keyCtrl(event):
		#print "in keyCtrl()"
		#print "key pressed:",event.keysym
		tag = 'bot1'
		
		if event.keysym == 'Up':
			print "key up"
			moveBot(tag,dir)
		if event.keysym == 'Down':
			print "key down"			
		return "break"
	
	#print "before bind call"
	
	canvas.bind_all('<Key>',keyCtrl)
		
	
#def moveBot(id,dir):
	#global canvas
	#while loop to keep moving
	#move = {"left":canvas.move(id,-1,0),
		#"right":canvas.move(id,1,0),
		#"up":canvas.move(id,0,-1),
		#"down":canvas.move(id,0,1)}
		
def makeRobots(numBots,dcenter, dwidth, rheight):
	x = dcenter
	y = rheight + 50
	r = 10
	tag = 'bot1'
	drawCircle(x,y,r,tag)
	return tag
	

def drawCircle(x, y, r, tag):
	global canvas
	canvas.create_oval(x-r, y-r, x+r, y+r, fill='black',tag=tag)
	
def left(id):
	global canvas
	canvas.move(id,-2,0)
	
def right(id):
	global canvas
	canvas.move(id,2,0)
	
def up(id):
	global canvas
	canvas.move(id,0,-2)
	
def down(id):
	global canvas
	canvas.move(id,0,-2)

def rotate(coords):
	#global canvas
	newCoords = []
	rm = RotMatrx()
	rm.angle = 90
	#print coords
	#print rm.angle
	#print rm.data[0]
	#print rm.data[1]
	print rm.data
	vec1 = coords[0:2]
	vec2 = coords[2:4]
	#print vec1
	newCoords.append(sum(map(lambda x,y:x*y,vec1,rm.data[0])))
	newCoords.append(sum(map(lambda x,y:x*y,vec1,rm.data[1])))
	newCoords.append(sum(map(lambda x,y:x*y,vec2,rm.data[0])))
	newCoords.append(sum(map(lambda x,y:x*y,vec2,rm.data[1])))
	#print newCoords
	return newCoords



def getLOS(id,rheight): #returns line of sight
	global canvas
	rad = 10    #radius of robot
	coords = canvas.coords(id)
	los = [coords[0]+rad,coords[1],coords[0]+rad,coords[1]+rheight]  #assume it sees across the room
	return los


def look(coords):
	r = 10

def turnLeft(id,los):
	print "looking left"
	coords = canvas.coords(id)
	newCoords = rotate(coords)
	print coords
	print newCoords
	canvas.coords(id,newCoords[0],newCoords[1],newCoords[2],newCoords[3])
	#look(coords)
	newLnOfSght = rotate(los)
	#print los
	#print newLnOfSght
	#canvas.update()
	return newLnOfSght
	
def startBot(id,rHeight):
	print "in startBot()"
	#get key event to start robot
	global canvas
	dir = "up"
	#moveBot(id,dir)
	
	moveBot = {"left":left,   #defs defined above
		"right":right,
		"up":up,
		"down":down}
		
	ypos = canvas.coords(id)[3]	#3rd one is y position
	print "ypos =" , ypos
	
	#for i in range(1,10):
	while ypos > rHeight:  #going thru entrance
		#print "in while loop"
		moveBot[dir](id)        #refer to dictionary above
		ypos = canvas.coords(id)[3]	
		#canvas.move(id,0,-1)
		canvas.update()
		#print "in for loop"
		time.sleep(.3)
	
	#id = 'rect'
	id = 'bot1'	
	lnOfSght = getLOS(id,rHeight)
	newLOS = turnLeft(id,lnOfSght)
	#canvas.update()
	
def stopBot():
	#get key event to stop robot
	print "in stopBot()"
	

def drawWalls():
	global canvas
	rmHeight = int( canvas.cget("height") ) - 100 #make room for robot to enter
	rmWidth = int( canvas.cget("width") )
	#print height
	doorWidth = 40
	doorCenter = rmWidth / 2
	doorBegin = doorCenter - doorWidth/2
	doorEnd = doorCenter + doorWidth/2
	wallThick = 5  #wall thickness
	walls = [doorBegin,rmHeight,wallThick,rmHeight,wallThick,wallThick,rmWidth,wallThick,rmWidth,rmHeight,doorEnd,rmHeight]
	canvas.create_line(walls,width=wallThick)
	return rmHeight,rmWidth,wallThick,doorCenter, doorWidth
	#canvas.update()
	
def drawObstacles(rmHeight, rmWidth, wallThick):
	global canvas
	numObst = 3
	
	#max height and width of each obstacle
	objHeightMax = rmHeight / numObst
	objWidthMax = rmWidth / numObst
	
	r = 30 #radius
	obst1Dim = [wallThick,wallThick,wallThick+r,wallThick+r]
	obst2Dim = [rmWidth-r,rmHeight-r,rmWidth-r*2,rmHeight-r*2]
	#write check for max size
	canvas.create_oval(obst1Dim,fill="yellow",tag='circ')
	canvas.create_rectangle(obst2Dim,fill="yellow",tag='rect')	
	#print obst2Dim
	#print rmHeight, rmWidth

	
	
def drawRoom():
	global canvas
	rheight, rwidth, wthick, dcenter, dwidth = drawWalls()
	drawObstacles(rheight, rwidth, wthick)
	canvas.update()
	return dcenter, dwidth, rheight
	
	
	

root = Tk()
numRobots = 1

canvas = Canvas(root,height=400,width=400,bg='green')
canvas.grid(row=1,column=1)
#getKeyIn()
doorcenter, doorwidth, roomheight = drawRoom()
tag = makeRobots(numRobots,doorcenter, doorwidth, roomheight)
startBot(tag,roomheight)
root.mainloop()
