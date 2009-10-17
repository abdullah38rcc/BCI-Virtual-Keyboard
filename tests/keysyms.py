# A small convenience contributed by effbot that
# prints the keysym when a key is pressed. 

import Tkinter                                                          
                                                                        
def callback(e):                                                        
    print e.keysym, repr(e.char)                                        
                                                                        
w = Tkinter.Frame(width=512, height=512)                                
w.bind("<KeyPress>", callback)                                          
w.focus_set()                                                           
w.pack()                                                                                                                                          
w.mainloop() 
