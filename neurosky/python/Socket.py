#socket class
import socket

class Socket:
	def __init__(self):
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def _connect(self,host,port):
		try:
			self._sock.connect((host,port))
		except Exception,e:
			print e
		
	def _send(self,msg):
		try:
			self._sock.sendall(msg)
		except Exception,e:
			print e
	
	def _receieve(self):
		try:
			msg = self._sock.recv(4096)
			return msg
		except Exception,e:
			print e