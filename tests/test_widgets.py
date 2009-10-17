# set up a short test with Tkinter's
# Label, Entry, Button and Text widgets
# check some of the interactions

from Tkinter import *

def update():
    data = entry.get()
    # clear any old text
    text.delete(1.0, END)
    text.insert(INSERT, data)
    # clear the entry
    entry.delete(0, END)


root = Tk()
#root.wm_attributes("-topmost", 1)
#root.focus_force()
root.focusmodel()

# for testing
name = "Franko"
s = name + " is:"


#label = Label(root, text=s)
#entry = Entry(root, width=25)
button = Button(root, text="Update", command=update)
button.config(font="Courier")
text = Text(root, width=25, height=1, insertofftime=250, insertbackground='red', takefocus=1)

# place the widgets in a grid
#label.grid(row=1, column=1)
#entry.grid(row=3, column=1)
button.grid(row=1, column=1)
text.grid(row=1, column=2)

# put the cursor into entry field
#entry.focus()
text.focus()

win = Canvas(root,height=400,width=400,bg='blue')
win.create_text(200,200,text="test", font="Courier 34",fill='red')
win.grid(row=2,column=1)

root.mainloop()