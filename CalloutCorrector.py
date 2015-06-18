from Tkinter import *
import os

from Config import *
from ReadXml import *
from text2int import *

from pygame import mixer
from pandas import DataFrame


def callid(call):
    global callout_ids
    if call in callout_ids:
        return callout_ids.index(call) + 1
    else:
        return -1


def gonext(event):
    sim_time = (float(current_call.time) - float(trial.time)) / 1000
    hyp_callout = text2int(current_call.words)
    hyp_callout_id = callid(hyp_callout)
    tran_callout = text2int(display_call.get())
    tran_callout_id = callid(tran_callout)
    new_row = [subject, trial.index + 1, trial.wintime, sim_time, current_call.words,
               hyp_callout, hyp_callout_id, display_call.get(),
               tran_callout, tran_callout_id, current_call.confidence, '']
    global data
    if data == 0:
        data = [new_row]
    else:
        data.append(new_row)

    current_call.nextcall()
    display_call.delete(0, END)
    display_call.insert(0, current_call.words)
    trial_disp_str.set(trial.index + 1)
    playcall()


def goback():
    current_call.lastcall()
    display_call.delete(0, END)
    display_call.insert(0, current_call.words)
    del data[-1]
    playcall()


def playcall():
    audio_filename = os.path.join(directory, audio_folders[trial.index], current_call.audio)
    display_filename.set(current_call.audio)
    mixer.Sound(audio_filename).play()

data = 0
current_call = CallOut()
callout_ids = ['450 ft', '400 ft', '350 ft', '7 %', '300 ft', '250 ft', '225 ft', '200 ft', '6 %', '175 ft', '150 ft',
               '140 ft', '5 %', '130 ft', '120 ft', '110 ft', '100 ft', '4 %']

root = Tk()
frame = Frame(root, height=500, width=900)
root.bind('<Return>', gonext)

Label(root, text='Trial:').grid(row=0, column=0)
trial_disp_str = StringVar()
trial_disp_str.set(trial.index + 1)
Label(root, textvariable=trial_disp_str).grid(row=0, column=1)


Label(root, text='Did they say:').grid(row=1, column=0)

display_call = Entry(root, width=25)
display_call.grid(row=1, column=1)
display_call.insert(1, current_call.words)

Label(root, text='File:').grid(row=2, column=0)
display_filename = StringVar()
display_filename.set('')
Label(root, textvariable=display_filename).grid(row=2, column=1)

back = Button(root, text='Back', command=goback)
back.grid(row=3, column=0)

replay = Button(root, text='Replay', command=playcall)
replay.grid(row=3, column=1)

mixer.init(frequency=15000)

root.focus_force()
root.mainloop()

DF = DataFrame(data)
cols = [['Subject ID', 'Trial ID', 'Windows Timestamp', 'Simulation Timestamp', 'Hypothesis', 'Hypothesis Callout', 'Hypothesis CalloutID',
         'Transcribed Utterance', 'Transcribed Callout', 'Transcribed Callout ID', 'Confidence', 'ASR Scoring Time']]
DF.columns = cols
outFilename = 'dataOutput-Subject' + str(subjectId) + '.csv'
DF.to_csv(outFilename, index=False)
