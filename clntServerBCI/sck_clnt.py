import socket
newSck = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
newSck.connect(('localhost',2727))
newSck.send('1')
newSck.recv(100)
newSck.close()