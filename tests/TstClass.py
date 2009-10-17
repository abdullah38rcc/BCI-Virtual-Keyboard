#test class

class TstClass:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.lst = []
		self.dictn = {}
		
	def fxn(self):
		self.dictn = {self.y:self.x}
		return self.dictn
		
	def callFxn(self):
		return self.fxn()