# particle filter simulation
# last edit: 12/14
##########################################----------QUESTIONS----------------############
# 
########################################----------BUGS------------------------###############
# infinite loop?
#########################################---------CURRENTLY WORKING ON--------###############
# filter()

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
	print "not in wall: coord:", [x,y]
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
	locx = uniform(1,dims[0],num)				#samples from a uniform distribution (low,high,size)
	locy = uniform(1,dims[1],num)			
	return [locx,locy]


# args: location[x,y], error, num samples
# rtns: [normal(locx,sigma),normal(locy,sigma)]
def GPS(loc,sigma,ns):
	#print "in gps:"
	nx = normal(loc[0],sigma,ns)
	ny = normal(loc[1],sigma,ns)
	#print "std dev y:", std(ny)
	#print "std dev x:", std(nx)
	#print #
	return [nx,ny]



def calcExp(smpl,ev):
	#print "in calcexp: sample:", smpl[0] 
	#print "in calcexp: sample:", smpl[1]
	print #
	mnx = mean(ev[0])
	mny = mean(ev[1])
	sdx = std(ev[0])
	sdy = std(ev[1])
	#print sd
	xnum = (smpl[0] - mnx)**2				#numerators
	ynum = (smpl[1] - mny)**2
	exp_x = xnum / sdx**2
	exp_y = ynum / sdy**2
	
	if exp_x > 3 or exp_y > 3:
		print "too far: ", smpl
		return []
	else:
		#print "close enough:", smpl
		return exp(1)**[(0 - exp_x),(0 - exp_y)]
	
	



def filter(evidence,num,sz):
	new = []							#new samples
	weights = []							#weights
	sm = 0								#sum of weights
	x =0
	while new == []:
	#while x < 4:
		print "sampling"
		samples = sampleUniform(sz,num)				#location samples
		samples = array(samples)
		for i in range(0,num):
			sample = samples[:,i]
			#print "sample",sample
			exp = calcExp(sample,evidence)
			#print exp
			if exp != []:
				print "close enough", sample
				#print "weight", exp
				#print #
				new.append(sample)
				weights.append(exp)
		x += 1
		if weights != []:
			weights = array(weights)
			sm = sum(weights[:,0],axis=0)
			print "sum along x", sm
		print "samples",new
		print "weights",weights
		print "sum", sm




def start():
	#test()
	N = 100							#number of particles
	sz = array([30,40])					#room dimensions
	sigmaGps = 2						#gps noise

	fig,room = createRoom(sz)
	rloc = createRobo(sz,fig,room)
	#print particles
	#print #
	gps = GPS(rloc,sigmaGps,N)				#distribution of gps readings
	#print mean(gps[1])
	#print std(gps[1])
	filter(gps,N,sz)


##########################------------main----------------############
start()
  
