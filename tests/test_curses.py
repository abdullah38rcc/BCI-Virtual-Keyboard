import sys, tty, termios

#fd = sys.stdin.fileno()
#old_settings = termios.tcgetattr(fd)
#tty.setraw(sys.stdin.fileno())
#ch = sys.stdin.read(1)

#ch = stdscr.getch()

import curses, time
stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1) 

try:
# Run your code here
    #ch = sys.stdin.read()
    ch = stdscr.getch()

    #ch = chr(ch)
    #if ch == curses.KEY_UP: 
       #print

    #curses.echo()
    if ch == 258:
       x = 3
       print("key down pressed")
       #print(ch)
       #stdscr.addch(20,25,ch)
       #stdscr.refresh() 
    elif ch == ord('q'):
       curses.echo()
       x = 3
       print(x)
    #print(ord(ch))
    #print(ch)
    pass
finally:
    time.sleep(1.5) 
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    print(ch)






 