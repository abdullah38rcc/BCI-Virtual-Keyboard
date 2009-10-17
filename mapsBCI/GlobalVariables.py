#global variables class for mapsBCI
# last edit: 9/21
##########TODO##############
###############CHANGES##########################
######################BUGS#######################
##############CURRENTLY WORKING ON##########

class GlobalVariables:
	def __init__(self, canvas):
		self._canvas = canvas
		self._travelPlan = ['left','up','right','down','left']		#plan for traveling round a room
		self._LOS = []		#line of sight
		self._COM = []		#center of mass
		self._move = {"left":self._left, "right":self._right, "up":self._up, "down":self._down}		#dict of fxns for moving
		self._nlosOffset = {"left":[-2,0,-2,0],"up":[0,-2,0,-2],"right":[2,0,2,0],"down":[0,2,0,2]}
		self._feelerOffset = {"left":[-1,0,70,0],"up":[0,-5,0,70],"right":[1,0,-70,0],"down":[0,5,0,-70]}
		self._comOffset = {"left":[-2,0],"up":[0,-2],"right":[2,0],"down":[0,2]}

	def _left(self, id):
		self._canvas.move(id,-2,0)



	def _right(self, id):
		self._canvas.move(id,2,0)



	def _up(self, id):
		self._canvas.move(id,0,-2)



	def _down(self, id):
		self._canvas.move(id,0,2)
