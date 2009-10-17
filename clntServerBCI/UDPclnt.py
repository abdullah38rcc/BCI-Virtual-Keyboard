#UDP socket client interface

from socket import *
from decimal import *
import curses

port = 20320
host = "136.152.183.189"
addr = (host,port)
buf = 1024
pos = 10

sock = socket(AF_INET,SOCK_DGRAM)
data = "%s %f" % ("1st val",pos)
sock.sendto(data,addr)

stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)




try:
    for i in range(1,10):
       ch = stdscr.getch()
       if ch == 258:
         pos =- pos
       elif ch == 259:
         pos += pos
       data = "%s %f" % ("yCursPos",pos)
       sock.sendto(data,addr)
    pass
finally:
    #time.sleep(1.5)
    sock.close()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    
