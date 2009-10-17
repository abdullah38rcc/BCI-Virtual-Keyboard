import socket
mySocket = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
mySocket.bind ( ( '', 2727 ) )
mySocket.listen ( 1 )

print "in sck_serv:"

while True:
   channel, details = mySocket.accept()
   print 'We have opened a connection with', details
   print channel.recv ( 100 )
   channel.send ( 'Green-eyed monster.' )
   channel.close()