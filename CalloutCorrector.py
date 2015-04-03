from Tkinter import *
import os

from ReadXml import *
from pygame import mixer
from pandas import DataFrame

data= 0
current_call = CallOut()

def gonext(event):
    sim_time_ms = ( int(current_call.time) - int(trial.time) )
    sim_time = str(sim_time_ms/60000) + ':' + str(sim_time_ms % 60000 / 1000)  + ':' + str(sim_time_ms %60000 %1000)
    new_row = [subject, trial.index + 1, trial.time, current_call.time, current_call.index + 1, sim_time,
               current_call.words, display_call.get()]
    global data
    if data == 0:
        data = [new_row]
    else:
        data.append(new_row)

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

root.focus_force()
root.mainloop()

DF = DataFrame(data)
cols = [ ['Subject #', 'Trial #', 'Trial Start Time', 'ASR Utterance' , 'ASR Utterance Timestamp',
          'Simulation Time of ASR Utterance', 'Spoken Utterance', 'Actual Utterance'] ] 
DF.columns = cols
DF.to_csv('Subject33Data_1.csv')
