"""
This class is a generic Tag class
"""

class Tag:
	def __init__(self,n="",t=""):
		self.tagName = n
		self.text = t
		#print "in Tag init"
	
	def _openTag(self):
		s = "<" + self.tagName + ">"
		return s
		
	def _closeTag(self,tname):
		s = "</" + tname + ">"
		return s