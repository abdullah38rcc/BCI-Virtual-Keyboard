import time

sz = array([[30,40]])
room = rand( sz[0,0], sz[0,1] )
room[:,0]=1
room[:,-1]=1
room[0,:]=1
room[-1,:]=1
robo[15,16]

pt = rand(50,2) * sz 
while 1:
  ## Graphics
  f = figure(1)
  f.set_visible(0)
  clf()
  # Show room map
  imshow(room, interpolation="nearest")
  #show robot
  plot(robo,'xr')
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
  
  
