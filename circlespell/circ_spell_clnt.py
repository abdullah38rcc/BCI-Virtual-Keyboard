from socket import *
import time, curses, random

host = "localhost"
port = 21567
addr = (host,port)
buf = 1024

newSck = socket(AF_INET,SOCK_STREAM)
#newSck.connect(('localhost',2727))

#init curses module
#stdscr = curses.initscr()
#curses.cbreak()
#stdscr.keypad(1)

#simulate misclassifications
errArr = [1,0,1,1,0,1,1,1,1,1]   #find out code for replicating ones

while(1):
	#get keypress
	ch = stdscr.getch()

	#time to aqcuire and analyze signal
	#time.sleep(1.5)

	#error code 
	bool = random.choice(errArr)
	if bool == 0:
		if ch == 258:
			ch = 259
		else:
			ch == 258

	if ch == ord('q'):  #quit
		break
	elif ch == 258:     #down key
	  	decision = 0  
	elif ch == 259:     #up key
		decision = 1

	data = "%s" % (decision)	
	newSck.sendto(data,addr)
	#newSck.recv(100)


#return terminal to normal behavior
curses.nocbreak()
stdscr.keypad(0)
curses.endwin()

newSck.close()