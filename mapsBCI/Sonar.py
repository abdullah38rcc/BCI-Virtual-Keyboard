# sonar class
# last edit: 11/8
#################################################
##########CURRENTLY WORKING ON###################
#point on plane
#ping(): check if wave travels maxDist then return []

import time
from math import *

class Sonar:
	
	def __init__(self):
		self._prvDst = 0		#previous distance to object detected by sonar
		self._prvTime = 0		#previous time sonar was called
		self._currDist = 0		#current distance to object
		self._currTime = 0		
		self._mxWavDist = 100		#max dist wave can travel
		self._wavRtn = 0		#current distance + mxWavDist



	#args: globalVariables object, direction
	#returns: distance to closest obstacle in wave's path 
	def _ping(self,gv,dirxn):
		self._resetConsts()
		wave = gv._LOS	#init wave to line of sight vector
		print "in ping"
		#print "wave: ", wave
		obstacle = []
		while obstacle == []:
			wave = self._waveTravel(wave,gv,dirxn)
			#obstacle = gv._canvas.find_overlapping(wave[0],wave[1],wave[2],wave[3])
			obstacle = self._hitSumthin(wave,gv)
			print "obstacle:",obstacle
		return abs(map(self._subtract,gv._currPos,obstacle))


	#args: wave vector
	#returns coords of obstacle hit by wave, or []
	def _hitSumthin(self,wav,gv):
		wavTip = wav[2:4]
		#return self._wallHit(wavTip,gv) or self._objHit(wavTip,gv)
		return self._wallHit(wavTip,gv)



	#args: last coord of wave, globalVariable instance
	#returns: coords of wall if a wall was hit, else nuthin
	def _wallHit(self,wv,gv):
		for key in gv._walls:
			if self._pointOnLine(wv,gv._walls[key]):	#gv._walls{wallName:wallCoord}
				return gv._walls[key]



	#args: point,line
	#returns: True if point is on line, else False
	def _pointOnLine(self,pt,line):
		#compare slopes from pt to line[0:1], and line[0:1] to line[2:3]
		#cross multiply to get rid of fractions
		return (pt[0]-line[0])*(line[3]-line[1]) == (line[2]-line[0])*(pt[1]-line[1])

			


	#reset constants
	def _resetConsts(self):
		self._prvDst = self._currDist
		self._prvTime = self._currTime
		self._currTime = time.time()
		self._wavRtn = self._currDist + self._mxWavDist



	#args: wave coordinates, globalVariables object, direction robot is travelling
	#returns: updated wave vector position
	def _waveTravel(self,wv,gv,d):
		print "in waveTravel"
		print "wave:", wv
		wv = map(self._add,wv,gv._feelerOffset[d])	#add offset so find_overlapping doesn't return robot iteself
		if self._rtnWave(wv):
			return []
		return wv



	#args: wave coords
	#returns: True if wave's traveled maxDist, else False
	def _rtnWave(self,wave):
		tmp = map(self._subtract,self._wavRtn,wave)
		if tmp > 0:
			return True
		return False



	#returns calculated velocity based on measurements
	def _getVelocity(self):
		delD = self._currDist - self._prevDst
		delT = self._currTime - self._prevTime
		return delD / delT



	def _add(self,x,y):
		#print "in add"
		#print "x:", x
		#print "y:", y
		#print "-" * 10
		return x + y


	def _subtract(self,x,y):
		return x - y
