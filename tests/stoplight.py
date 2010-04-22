#Stoplight class
import time

class Stoplight:
	def __init__(self,timing):		#times[green delay,yellow delay,red delay]
		self.start(timing)
	
	def start(self,times):
		tyming = {"green":times[0],"yellow":times[1],"red":times[2]}
		colors = ["green","yellow","red"]
		while True:
			for color in colors:
				print "turning", color
				self.delay(tyming[color])		

	def delay(self,t):
		#print "delaying for " + str(t) + " seconds"
		print #
		time.sleep(t)