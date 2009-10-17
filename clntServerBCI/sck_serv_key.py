from socket import *
import circlespell

# Set the socket parameters
host = "localhost"
port = 21567
buf = 1024
addr = (host,port)

# Create socket and bind to address
UDPSock = socket(AF_INET,SOCK_DGRAM)
UDPSock.bind(addr)

print "in sock server key:"

# Receive messages
while 1:
	data,addr = UDPSock.recvfrom(buf)
 	print data
	if data == '0':
		break

# Close socket
UDPSock.close()
