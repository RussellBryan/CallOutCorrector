import os
import pandas as pd

from text2int import *
from ReadXml import *

subject = Subject()
trial = Trial()
current_call = CallOut()
callout_ids = ['450 ft', '400 ft', '350 ft', '7 %', '300 ft', '250 ft', '225 ft', '200 ft', '6 %', '175 ft', '150 ft',
               '140 ft', '5 %', '130 ft', '120 ft', '110 ft', '100 ft', '4 %']
def callid(call):
    global callout_ids
    if call in callout_ids:
        return callout_ids.index(call) + 1
    else:
        return -1

data = 0
go  = True

while go:
    sim_time = float(current_call.time) - float(trial.time)
    hyp_callout = text2int(current_call.words)
    hyp_callout_id = callid(hyp_callout)
    new_row = [subject.id, trial.index + 1, sim_time, current_call.words,
               hyp_callout, hyp_callout_id]

    if data == 0:
        data = [new_row]
    else:
        data.append(new_row)
    
    if current_call.index== (trial.ncalls - 1):
        if trial.index == 23:
            if subject.index==len(subjects) -1:
                go = False
            else:
                subject.nextsubj()
                trial = Trial()
                current_call = CallOut()
        else:
            trial.nexttrial()
            current_call = CallOut()
    else:
        current_call.nextcall()
    
DF = pd.DataFrame(data)
cols = [ ['Subject ID', 'Trial ID', 'Simulation Time', 'Hypothesis', 'Hypothesis Callout', 'Hypothesis CalloutID'] ]
DF.columns = cols
DF.to_csv('All_Callout_Data', index=False)
