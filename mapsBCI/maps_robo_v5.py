# simulation of robot that enters and travels around a room, looks left frequently, detects and avoid objects
# last edit: 5/21
##########TODO##############
# lambda expressions for case-swtich/dictionary
# maps algorithm
# argument to drawRoom() to specify num obastacles
# in drawObstacles() randomly place objects in room
#	             check for max obstacle size
# add camera
# y is the line of sight being drawn thru bot?
#   - hack: add padding
# change moveBot so dir's are in order of moving around room
# lookLeft: y does find_closest work better than find overlapping?
# use global class
###############CHANGES##########################
# getLOS: max_dist = 100 
# start_bot: robo travels left b4 it looks left
# erase canvas.create_line(los) as view changes
# drawRoom: roowidth returned : rwidth and rheight modified to acct for wallthick
# start_bot: roomwidth passed as arg
######################BUGS#######################
# moving up stops for bot
# getLOS: pad=16 creates wierd behaviour
##############CURRENTLY WORKING ON##########
# obstacle detection/avoidance
# 

from Tkinter import *
from math import *
import time

#how can i pass angle into instantiation
class RotMatrx:   #rotation matrix  (clockwise for left cuz y-axis increases downward)
	#def _init_(self,angle):
		#self.angle = angle
		#self.data = [[cos(radians(angle)), sin(radians(angle))],[-sin(radians(angle)),cos(radians(angle))]]
	#angle = 0
	#data = [[cos(radians(angle)), sin(radians(angle))],[-sin(radians(angle)),cos(radians(angle))]]
	#data = [[cos(angle), sin(angle)],[-sin(angle),cos(angle)]]
	data = [[0,1],[-1,0]]


class RtRotMatrx:
	data = [[0,-1],[1,0]]

class TransMatrx:  #translates matrices to coord system origin
	x_Amt = 0
	y_Amt = 0
	data = [[x_Amt,y_Amt],[x_Amt,y_Amt]]

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
	canvas.create_oval(x-r, y+r, x+r, y-r, fill='black',tag=tag)
	
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
	canvas.move(id,0,2)

def getCOM(points):  #returns center of line formed by obj bounding box corners
	#print "in getCOM"
	#print "points of bounding box",points
	#print "original pnts:",points
	center = [(points[0]+points[2])/2, (points[1]+points[3])/2]
	#print "center:",center
	return center

def translate(points,x_amt,y_amt,original):
	#print "in translate"	
	if original:   #if translating back to original position
		x_amt = - x_amt
		y_amt = - y_amt
	#print "x amt:",x_amt
	#print "y amt",y_amt
	transPnts = []
	transPnts.append(points[0] - x_amt)
	transPnts.append(points[1] - y_amt)
	transPnts.append(points[2] - x_amt)
	transPnts.append(points[3] - y_amt)
	#print "translated points:", transPnts
	return transPnts
	
	
def rotate(coords,cntrOfMass):
	#print "in rotate"
	#global canvas
	#transMtrx = TransMatrx()
	#x_amt = cntrOfMass[0]
	#y_amt = cntrOfMass[1]

	rotCoords = []
	rm = RotMatrx()
	#rm.angle = angle
	#print coords
	#print rm.angle
	#print rm.data[0]
	#print rm.data[1]
	#print rm.data
	transCoords = translate(coords,cntrOfMass[0],cntrOfMass[1],0)
	vec1 = transCoords[0:2]
	vec2 = transCoords[2:4]
	#print vec1
	#coord vector X rotation matrix
	rotCoords.append(sum(map(lambda x,y:x*y,vec1,rm.data[0])))
	rotCoords.append(sum(map(lambda x,y:x*y,vec1,rm.data[1])))
	rotCoords.append(sum(map(lambda x,y:x*y,vec2,rm.data[0])))
	rotCoords.append(sum(map(lambda x,y:x*y,vec2,rm.data[1])))
	#print "rotated coordinates:",rotCoords
	newCoords = translate(rotCoords,cntrOfMass[0],cntrOfMass[1],1)	
	#newCoords = translate(rotCoords,1)
	#print newCoords
	return newCoords


def rt_rotate(coords,cntrOfMass):
	#print "in rotate"
	#global canvas
	#transMtrx = TransMatrx()
	#x_amt = cntrOfMass[0]
	#y_amt = cntrOfMass[1]

	rotCoords = []
	rm = RtRotMatrx()
	#rm.angle = angle
	#print coords
	#print rm.angle
	#print rm.data[0]
	#print rm.data[1]
	#print rm.data
	transCoords = translate(coords,cntrOfMass[0],cntrOfMass[1],0)
	vec1 = transCoords[0:2]
	vec2 = transCoords[2:4]
	#print vec1
	#coord vector X rotation matrix
	rotCoords.append(sum(map(lambda x,y:x*y,vec1,rm.data[0])))
	rotCoords.append(sum(map(lambda x,y:x*y,vec1,rm.data[1])))
	rotCoords.append(sum(map(lambda x,y:x*y,vec2,rm.data[0])))
	rotCoords.append(sum(map(lambda x,y:x*y,vec2,rm.data[1])))
	#print "rotated coordinates:",rotCoords
	newCoords = translate(rotCoords,cntrOfMass[0],cntrOfMass[1],1)	
	#newCoords = translate(rotCoords,1)
	#print newCoords
	return newCoords



def getLOS(id): #returns line of sight
	global canvas
	rad = 10    #radius of robot
	maxDist = 100  #max distance robot can see
	pad = 20   #hack
	coords = canvas.coords(id)
	#print "robo located at",coords
	los = [coords[2]-rad,coords[3]-pad,coords[2]-rad,coords[3]-maxDist]
	#canvas.create_line(los,width=2,arrow=LAST,tag='los',fill='blue')
	#canvas.update()
	#print "first looking towards (blue):",los
	return los


def lookLeft(los,com):
	global canvas
	time.sleep(.3)
	canvas.delete('los')
	newLOS = rotate(los,com)
	#print "looking left (red):",newLOS
	#print "looking towards",newLOS

	objId = canvas.find_closest(los[2],los[3], halo=0)
	#objId = canvas.find_overlapping(los[0],los[1],los[2],los[3])
	print "looking left at:",canvas.itemcget(objId,'tag')
	canvas.create_line(newLOS,width=2,arrow=LAST,fill='red',tag='los')
	canvas.update()
	#print objId

def turnLeft(id,los,com):
	global canvas
	print "turning left"
	coords = canvas.coords(id)
	#print "before turn, located at",coords
	newCoords = rotate(coords,com)
	#print coords
	#print newCoords
	canvas.coords(id,newCoords[0],newCoords[1],newCoords[2],newCoords[3])
	#look(coords)
	canvas.delete('los')
	newLnOfSght = rotate(los,com)
	#print "now looking towards (orange)",newLnOfSght
	#canvas.create_line(newLnOfSght,width=2,fill='orange',arrow=LAST,tag='los')
	#print los
	#print newLnOfSght
	#canvas.update()
	return newLnOfSght


def turnRight(id,los,com):
	global canvas
	print "turning right"
	coords = canvas.coords(id)
	#print "before turn, located at",coords
	newCoords = rt_rotate(coords,com)
	#print coords
	#print newCoords
	canvas.coords(id,newCoords[0],newCoords[1],newCoords[2],newCoords[3])
	#look(coords)
	canvas.delete('los')
	newLnOfSght = rt_rotate(los,com)
	#print "now looking towards (orange)",newLnOfSght
	canvas.create_line(newLnOfSght,width=2,fill='orange',arrow=LAST,tag='los')
	#print los
	#print newLnOfSght
	canvas.update()
	return newLnOfSght

	
def startBot(id,rHeight,rWidth):
	#print "in startBot()"
	#get key event to start robot
	global canvas
	dir = "up"
	#moveBot(id,dir)
	
	moveBot = {"left":left,   #defs defined above
		"right":right,
		"up":up,
		"down":down}
		
	ypos = canvas.coords(id)[3]	#3rd one is y position
	#print "ypos =" , ypos
	
	#for i in range(1,10):
	while ypos > rHeight-20:  #going thru entrance
		#print "in while loop"
		moveBot[dir](id)        #refer to dictionary above
		ypos = canvas.coords(id)[3]	
		#canvas.move(id,0,-1)
		canvas.update()
		#print "in for loop"
		time.sleep(.2)
	
	#id = 'rect'
	#id = 'bot1'	
	lnOfSght = getLOS(id)
	coords = canvas.coords(id)
	cntrOfMass = getCOM(coords)
	newLOS = turnLeft(id,lnOfSght,cntrOfMass)

	dir = 'left'
	#xpos = newLOS[2]
	#print "1/2 room width:",rWidth/2
	#print "1/2 room height:",rHeight/2

	stop = ()
	while stop == ():  #move towards left
		#print "in while loop"
		moveBot[dir](id)        #refer to dictionary above
		#tmp = tmp -1
		newLOS[0] = newLOS[0] - 2
		newLOS[2] = newLOS[2] - 2
		cntrOfMass[0] = cntrOfMass[0] - 2
		lookLeft(newLOS,cntrOfMass)
		feeler = [newLOS[2]+70,newLOS[3],newLOS[0]-1,newLOS[1]]
		#print "feelers overlapping :", canvas.find_overlapping(feeler)  #why doesn't this work?
		stop = canvas.find_overlapping(feeler[0],feeler[1],feeler[2],feeler[3])  #stop when it comes within certain dist of obstacle
		#print stop
		#stop = stop[0]
		if stop != ():
			print "stopped for:", canvas.itemcget(int(stop[0]),'tag')
		#canvas.move(id,0,-1)
		canvas.update()
		#print "xpos:",xpos
		time.sleep(.2)
	#print "feeler (yellow)"
	#canvas.create_line(feeler,fill='yellow',tag='feeler')
	#canvas.create_line(newLOS,fill='yellow',tag='los')
	#lookLeft(newLOS,cntrOfMass)
	
	dir = 'up'
	newLOS = turnRight(id,newLOS,cntrOfMass)
	stop = ()
	while stop == ():  #move up
		#print "in while loop"
		moveBot[dir](id)        #refer to dictionary above
		#tmp = tmp -1
		newLOS[1] = newLOS[1] - 2
		newLOS[3] = newLOS[3] - 2
		cntrOfMass[1] = cntrOfMass[1] - 2
		lookLeft(newLOS,cntrOfMass)
		feeler = [newLOS[2],newLOS[3]+70,newLOS[0],newLOS[1]-5]
		#print "feeler:",feeler
		#print "feelers overlapping :", canvas.find_overlapping(feeler)  #why doesn't this work?
		stop = canvas.find_overlapping(feeler[0],feeler[1],feeler[2],feeler[3])  #stop when it comes within certain dist of obstacle
		#print stop
		#stop = stop[0]
		if stop != ():
			print "stopped for:", canvas.itemcget(int(stop[0]),'tag')
		#canvas.move(id,0,-1)
		canvas.update()
		#print "xpos:",xpos
		time.sleep(.2)	

	dir = 'right'
	newLOS = turnRight(id,newLOS,cntrOfMass)
	stop = ()
	while stop == ():  #move right
		#print "in while loop"
		moveBot[dir](id)        #refer to dictionary above
		#tmp = tmp -1
		newLOS[0] = newLOS[0] + 2
		newLOS[2] = newLOS[2] + 2
		cntrOfMass[0] = cntrOfMass[0] + 2
		lookLeft(newLOS,cntrOfMass)
		feeler = [newLOS[2]-70,newLOS[3],newLOS[0]+1,newLOS[1]]
		#print "feeler:",feeler
		#print "feelers overlapping :", canvas.find_overlapping(feeler)  #why doesn't this work?
		stop = canvas.find_overlapping(feeler[0],feeler[1],feeler[2],feeler[3])  #stop when it comes within certain dist of obstacle
		#print stop
		#stop = stop[0]
		if stop != ():
			print "stopped for:", canvas.itemcget(int(stop[0]),'tag')
		#canvas.move(id,0,-1)
		canvas.update()
		#print "xpos:",xpos
		time.sleep(.2)	
	canvas.create_line(feeler,fill='yellow',tag='feeler')	
	canvas.update()
	
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
	canvas.create_line(walls,width=wallThick,tag='walls')
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
	rwidth = rwidth - 2 * wthick    #take wall thickness into acct
	rheight = rheight - wthick
	canvas.update()
	return dcenter, dwidth, rheight, rwidth
	




def testRotate():
	points = [0,0,4,0]
	#points = [1,1,5,1]
	#points = [3,1,7,10] #how bounding box coords specified (uppr lft, bott rt)	
	com = getCOM(points)
	angle = 90
	newPnts = rt_rotate(points,com)
	#newPnts = rotate(points,com)	
	print "orig points:",points
	print "rotated points:",newPnts


	
	

root = Tk()
numRobots = 1

canvas = Canvas(root,height=400,width=400,bg='green')
canvas.grid(row=1,column=1)
#getKeyIn()
doorcenter, doorwidth, roomheight, roomwidth = drawRoom()
tag = makeRobots(numRobots,doorcenter, doorwidth, roomheight)
startBot(tag,roomheight,roomwidth)
#testRotate()
root.mainloop()
