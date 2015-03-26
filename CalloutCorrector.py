from Tkinter import *
import os

from ReadXml import *


current_call = CallOut()

def gonext(event):
    CallOut.nextcall(current_call)
    display_call.delete(0, END)
    display_call.insert(0, current_call.words)

def goback():
    CallOut.lastcall(current_call)
    display_call.delete(0, END)
    display_call.insert(0, current_call.words)

def playcall():
    pass


root = Tk()
frame = Frame(root, height=500, width=900)
root.bind("<Return>", gonext)

prompt = Label(root, text="Did they say:")
prompt.grid(row=0, column=0)

display_call = Entry(root)
display_call.grid(row=0, column=2)
display_call.insert(0, current_call.words)

back=Button(root, text="Back", command=goback)
back.grid(row=2, column=0)

replay=Button(root, text="Replay", command=playcall)
replay.grid(row=2, column=2)


root.mainloop()
