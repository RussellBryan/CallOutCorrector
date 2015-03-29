from Tkinter import *
import os

from ReadXml import *
from pygame import mixer

current_call = CallOut()

def gonext(event):
    current_call.nextcall()
    display_call.delete(0, END)
    display_call.insert(0, current_call.words)
    playcall()

def goback():
    current_call.lastcall()
    display_call.delete(0, END)
    display_call.insert(0, current_call.words)
    playcall()

def playcall():
    mixer.Sound(directory + audio_folders[trial.index] + '/' + current_call.audio).play()


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

mixer.init(frequency=15000)

root.mainloop()
