# simulation of robot that enters and travels around a room, looks left frequently, detects and avoid objects
# last edit: 12/12
##########TODO##############
# speedometer
# grid
# lambda expressions for case-swtich/dictionary
# maps algorithm
# argument to drawRoom() to specify num obastacles
# in drawObstacles() randomly place objects in room
#	             check for max obstacle size
# change move so dir's are in order of moving around room
# lookLeft: y does find_closest work better than find overlapping?
###############CHANGES##########################
# startBot code = compact
# moveBot()
# rectangle1 larger and moved more into corner
######################BUGS#######################
# getLOS: pad=16 creates wierd behaviour
##############CURRENTLY WORKING ON##########
# 

from Tkinter import *
from math import *
from GlobalVariables import *
import time

#############################################----------- classes ------------------##############

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



##########################################------------------- draw gui ---------------###############

def makeRobots(numBots,dcenter, dwidth, rLength):
	x = dcenter
	y = rLength + 50
	r = 10
	tag = 'bot1'
	drawCircle(x,y,r,tag)
	return tag



def drawCircle(x, y, r, tag):
	global canvas
	canvas.create_oval(x-r, y+r, x+r, y-r, fill='black',tag=tag)



def drawWalls():
	global canvas
	rmLength = int( canvas.cget("height") ) - 100 #make room for robot to enter
	rmWidth = int( canvas.cget("width") )
	#print Length
	doorWidth = 40
	doorCenter = rmWidth / 2
	doorBegin = doorCenter - doorWidth/2
	doorEnd = doorCenter + doorWidth/2
	wallThick = 5  #wall thickness
	walls = [doorBegin,rmLength,wallThick,rmLength,wallThick,wallThick,rmWidth,wallThick,rmWidth,rmLength,doorEnd,rmLength]
	canvas.create_line(walls,width=wallThick,tag='walls')
	return rmLength,rmWidth,wallThick,doorCenter, doorWidth
	#canvas.update()
	
	
def drawGrid():
	global canvas
	x = 0
	y = 0
	xstep = 20
	ystep = 5
	rmLength = int( canvas.cget("height") )
	rmWidth = int( canvas.cget("width") )
	xend = x + rmWidth
	yend = y + rmLength

	for _x in range(x,xend+1,xstep):
		canvas.create_line(_x,y,_x,yend)


def drawObstacles(rmLength, rmWidth, wallThick):
	global canvas
	numObst = 3

	#max Length and width of each obstacle
	objLengthMax = rmLength / numObst
	objWidthMax = rmWidth / numObst

	r = 30 #radius
	obst1Dim = [wallThick,wallThick,wallThick+r,wallThick+r]
	obst2Dim = [rmWidth-r/2,rmLength-r/2,rmWidth-r*4,rmLength-r*2]
	#write check for max size
	canvas.create_oval(obst1Dim,fill="yellow",tag='circle1')
	canvas.create_rectangle(obst2Dim,fill="yellow",tag='rectangle1')	
	#print obst2Dim
	#print rmLength, rmWidth



def drawRoom():
	global canvas
	rLength, rwidth, wthick, dcenter, dwidth = drawWalls()
	drawObstacles(rLength, rwidth, wthick)
	rwidth = rwidth - 2 * wthick    #take wall thickness into acct
	rLength = rLength - wthick
	canvas.update()
	return dcenter, dwidth, rLength, rwidth



##################################################------------------- helper fxns --------------##########

def add(x,y):
	#print "x: ", x
	#print "y: ", y
	return x + y



def getCOM(points):  #returns center of line formed by obj bounding box corners
	#print "in getCOM"
	#print "points of bounding box",points
	#print "original pnts:",points
	center = [(points[0]+points[2])/2, (points[1]+points[3])/2]
	#print "center:",center
	return center



#################################################---------------- geometry ----------------############

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



#############################################################----------- camera -----------###############

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



def lookLeft(los,dir,com):
	global canvas
	time.sleep(.3)
	canvas.delete('los')
	newLOS = rotate(los,com)
	#print "looking left (red):",newLOS
	#print "looking towards",newLOS
	#print "in lookLeft: dir: ", dir

	#hack: alter los so that find_overlapping() doesn't return robo
	offsetDict = {}
	offsetDict["right"] = [0,-4,0,0]
	offsetDict["left"] = [0,4,0,0]
	offsetDict["down"] = [4,0,0,0]
	offsetDict["up"] = [-4,0,0,0]
	
	offset = offsetDict[dir]
	#objId = canvas.find_closest(los[2],los[3], halo=0)

	#find_overlapping(x1,y1,x2,y2) : upper left, lower right
	objId = canvas.find_overlapping(newLOS[0]+offset[0], newLOS[1]+offset[1], newLOS[2]+offset[2], newLOS[3]+offset[3])
	temp = [newLOS[0]+offset[0], newLOS[1]+offset[1], newLOS[2]+offset[2], newLOS[3]+offset[3]]		#stub
	canvas.create_line(temp,width=2,arrow=LAST,fill='red',tag='los')		#stub
	#print "in lookLeft: tempLOS: ", temp
	#objId = canvas.find_overlapping(newLOS[0],newLOS[1],newLOS[2],newLOS[3])
	#print " in lookLeft: objID: ", objId
	if len(objId) > 1:
		print "looking left at:",canvas.itemcget(objId[1],'tag')
	else:
		print "looking left at:",canvas.itemcget(objId,'tag')
	#canvas.create_line(newLOS,width=2,arrow=LAST,fill='red',tag='los')
	canvas.update()
	#print objId



######################################################--------------- locomotion ---------------############

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



def moveBot(dir,id):
	global gv
	gv._move[dir](id)        #refer to dictionary above
	gv._LOS = map(add,gv._LOS,gv._nlosOffset[dir])
	gv._COM = map(add,gv._COM,gv._comOffset[dir])
	lookLeft(gv._LOS,dir,gv._COM)
	temp = map(add,gv._LOS,gv._feelerOffset[dir])
	feeler = [temp[2],temp[3],temp[0],temp[1]]
	#print #
	#print "for ", dir
	#print " feeler: ", feeler
	#print #
	stop = canvas.find_overlapping(feeler[0],feeler[1],feeler[2],feeler[3])  #stop when it comes within certain dist of obstacle
	if stop != ():
		print "stopped for:", canvas.itemcget(int(stop[0]),'tag')
	canvas.update()
	time.sleep(.2)
	return stop



def enterRoom(id, rLength):
	global gv

	time.sleep(2)
	dir = "up"
	ypos = canvas.coords(id)[3]	#3rd one is y position
	while ypos > rLength-20:  #going thru entrance
		gv._move[dir](id)        #refer to dictionary above
		ypos = canvas.coords(id)[3]	
		canvas.update()
		time.sleep(.2)

	gv._LOS = getLOS(id)
	#newLOS = getLOS(id)
	coords = canvas.coords(id)
	gv._COM = getCOM(coords)
	gv._LOS = turnLeft(id,gv._LOS,gv._COM)



###############################################################-------- start/stop ---------###############

def startBot(id,rmLength,rmWidth):
	#print "in startBot()"
	#get key event to start robot
	global gv

	enterRoom(id,rmLength)
	for dirxn in gv._travelPlan:
		stop = ()
		while stop == ():
			stop = moveBot(dirxn,id)
		gv._LOS = turnRight(id,gv._LOS,gv._COM)



def stopBot():
	#get key event to stop robot
	print "in stopBot()"



######################################################-------------- I/O -----------###########

def getKeyIn():
	#print "in getKeyIn()"
	global canvas

	def keyCtrl(event):
		#print "in keyCtrl()"
		#print "key pressed:",event.keysym
		tag = 'bot1'

		if event.keysym == 'Up':
			print "key up"
			move(tag,dir)
		if event.keysym == 'Down':
			print "key down"			
		return "break"

	#print "before bind call"

	canvas.bind_all('<Key>',keyCtrl)



####################################################--------------- test/main ---------------############

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
gv = GlobalVariables(canvas)
canvas.grid(row=1,column=1)
#getKeyIn()
drawGrid()
#doorcenter, doorwidth, roomLength, roomwidth = drawRoom()
#tag = makeRobots(numRobots,doorcenter, doorwidth, roomLength)
#startBot(tag,roomLength,roomwidth)
#testRotate()
root.mainloop()
