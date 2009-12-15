# particle filter simulation
# last edit: 12/14
##########################################----------QUESTIONS----------------############
# 
########################################----------BUGS------------------------###############
# 
#########################################---------CURRENTLY WORKING ON--------###############
# gps(),filter()

import time

# create room map
# args: room size as array(height,width)
# rtn: figure, room grid
def createRoom(sz):
	room = zeros( (sz[0], sz[1]),bool)
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
	x = randint(1,sz[1])
	y = randint(1,sz[0])
	if rm[y,x]:
		#print "in wall: coord:", [x,y]
		return randRoboLoc(sz,rm)
	#print "not in wall: coord:", [x,y]
	return [x,y]


# args: room dims[width,height], figure number, room coords (width x height array)
# rtns: [x,y] coords
def createRobo(sz,fig,room):
	roboLoc = randRoboLoc(sz,room)
	fig.set_visible(0)
	clf()
	imshow(room, interpolation="nearest")
	plot([roboLoc[0]],[roboLoc[1]],'sr')
	axis([0,sz[1],0,sz[0]])
	fig.set_visible(1)
	draw()
	#print room.size
	return roboLoc


# args: room dims[width,height], number of samples
# rtns: numsamples x 2 array of uniformly drawn samples from 0-width and 0-height
def sampleUniform(dims,num):
	tmp = dims[0]
	locx = uniform(0,tmp[0],num)				#samples from a uniform distribution (low,high,size)
	locy = uniform(0,tmp[1],num)			
	return [locx,locy]


# args: location[x,y], error, num samples
# rtns: [normal(locx,sigma),normal(locy,sigma)]
def GPS(loc,sigma,N):
	nx = normal(loc[0],sigma,N)
	ny = normal(loc[1],sigma,N)
	return [nx,ny]
	


def start():
	#test()
	N = 50							#number of particles
	sz = array([30,40])					#room dimensions
	sigmaGps = 0.2						#gps noise

	fig,room = createRoom(sz)
	rloc = createRobo(sz,fig,room)
	#belState = sampleUniform(sz,N)				#belief state
	#print belState
	#gps = normal(rloc[0],sigmaGps,N)			#distribution of gps readings
	#print mean(gps)
	


##########################------------main----------------############
start()
  
