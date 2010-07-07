"""
This class generates HTML pages
"""
from Tag import *
import os

class genHTML:
	def __init__(self):
		self.tagList = []						#list of tags in order of appearance
		self.fname = "generatedHTML.html"		#newly generated html file
		self._start()
		
		

	def _start(self):
		html = self._newTag('html',1)
		body = self._newTag('body',2)
		para = self._newTag('p',0)
		para.text = "This is a python generated HTML page."
		self._write(para.text,1)
		self._closeTags(self.tagList)
		
		
	"""
	create a new tag object, write it to file, add it to tag list, return object
	args: tag name, number of new lines after tag
	"""
	def _newTag(self,tagNm, nl):
		tmp = Tag(tagNm)
		self.tagList.insert(0,tmp.tagName)
		self._write(tmp._openTag(), nl)
		return tmp
	
	
	"""
	This function generates all the closing tags for the tags in the tag list
	Args: ordered tag list
	"""
	def _closeTags(self,tlist):
		close = Tag()
		for item in tlist:
			#print item
			self._write(close._closeTag(item),1)



	"""
	This function creates file self.fname if it doesn't exist and writes to it
	Args: tag, number of newlines
	"""
	def _write(self,data,numNL):
		if not os.path.exists(self.fname):
			fd = open(self.fname, 'w')
			fd.write(data)
		else:
			fd = open(self.fname, 'a')
			fd.write(data)

		if numNL !=0:
			#print "not zero"
			for i in range(1,numNL + 1):				
				fd.write('\n')

		fd.close()