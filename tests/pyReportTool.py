"""
This script runs a python script and captures its output, compiling it to a pretty report in an html file.
"""

import subprocess

def openScript(sname):
	cmd = "python " + sname
	#child = subprocess.Popen("python hello.py", shell=True)
	#child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	#rslt = child.communicate()[0]
	rslt = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
	#print rslt
	return rslt
	
#def htmlReport():


def genTags(txt):	
	



fname = "hello.py"
#fname = 'sortNumWords.py'
output = openScript(fname)
