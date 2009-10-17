from socket import *

host = "localhost"
port = 21567
#port = 2727
buf = 1024
addr = (host,port)

newSck = socket(AF_INET,SOCK_DGRAM)
#newSck.connect(('localhost',2727))

decision = 0

while (1):
	#data = "%s" % (decision)
	data = "hello"
	if decision == 1:
		break
	else:
		if(newSck.sendto(data,addr)):
			print "Sending message '",data,"'....."
	data = 1

#newSck.send('1')
#newSck.recv(100)
newSck.close()