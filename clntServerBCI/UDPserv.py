# UDP socket server interface
from socket import *

host = "localhost"
port = 20320
buf = 1024
addr = (host,port)

#creat socket and bind to address
sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(addr)

#while client is sending, recieve messages, else close
while 1:
	data,daddr = sock.recvfrom(buf)
	if not data:
		print("client has closed")
		break
	else:
		print data

sock.close()
