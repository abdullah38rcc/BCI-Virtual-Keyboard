import circlespell
from socket import *

host = "localhost"
port = 21567
#port = 2727
buf = 1024
addr = (host,port)


mySocket = socket ( AF_INET, SOCK_DGRAM)
mySocket.bind (addr)
#mySocket.listen ( 1 )

#circlespell()

print "in circle spell server:"
count = 0

while 1:
	decision, channel = mySocket.recvfrom(buf)
	print decision
	#circle_spell.update(decision)
	#print 'We have opened a connection with', details
	#print channel.recv ( 100 )
	#channel.send ( 'Green-eyed monster.' )
	count = count + 1
	if count == 5:
		break
channel.close()