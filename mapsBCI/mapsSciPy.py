#################----------questions----------------############
#why is graph being drawn that way?  prob with robo ending up in walls...
##################################################################
import time

# create room map
# args: room size as sz[[]]
# rtn: figure, room grid
def createRoom(sz):
	room = zeros( (sz[0,0], sz[0,1]),bool)
	room[:,0]=1
	room[:,-1]=1
	room[0,:]=1
	room[-1,:]=1
	f = figure(1)
	f.set_visible(0)
	clf()
	# Show room map
	imshow(room, interpolation="nearest")
	f.set_visible(1)
	draw()
	#print room.size
	return f,room

def test():
	sz = array([[30,40]])
	room = zeros( (sz[0,0], sz[0,1]),bool )
	room[:,0]=1
	room[:,-1]=1
	room[0,:]=1
	room[-1,:]=1

	roboLoc = (15,16)

	pt = rand(50,2) * sz 
	while 1:
	  ## Graphics
	  f = figure(1)
	  f.set_visible(0)
	  clf()
	  # Show room map
	  imshow(room, interpolation="nearest")
	  #show robot
	  plot([roboLoc[0]],[roboLoc[1]],'sr')
	  # Show particles
	  plot( pt[:,1],pt[:,0], 'oy')
	  # Set image size
	  axis([0,sz[0,1],0,sz[0,0]])
	  # Make changes visible
	  f.set_visible(1)
	  draw()
	  time.sleep(0.1)
	  ## Update particles
	  pt += randn(50,2)*0.2 + sz
	  pt %= sz


# args: room size, room grid
# rtns: robo coords
def randRoboLoc(sz,rm):
	tmp = sz[0]
	x = randint(1,tmp[0])
	y = randint(1,tmp[1])
	if rm[x,y] == 1:
		#print "in wall: coord:", [x,y]
		randRoboLoc(sz,rm)
	#print "not in wall: coord:", [x,y]
	return [x,y]


# args: room size, figure number, room coords
# rtns: robot locat
def createRobo(sz,fig,room):
	roboLoc = randRoboLoc(sz,room)
	fig.set_visible(0)
	clf()
	imshow(room, interpolation="nearest")
	plot([roboLoc[0]],[roboLoc[1]],'sr')
	axis([0,sz[0,1],0,sz[0,0]])
	fig.set_visible(1)
	draw()
	#print room.size
	return roboLoc
	


def start():
	#test()
	N = 50				#number of particles
	sz = array([[30,40]])		#room dimensions
	rofig,room = createRoom(sz)
	rloc = createRobo(sz,fig,room)
	samples = startSamples()
	
	


##########################------------main----------------############
start()
  
