import os
import pandas as pd
import re
import xml.etree.ElementTree as ET
from text2int import *


directory = '/Users/admin/Desktop/subjects/'
subjects = os.listdir(directory)
for s in subjects:
    if 'Subject' not in s:
        subjects.remove(s)

callout_ids = ['450 ft', '400 ft', '350 ft', '7 %', '300 ft', '250 ft', '225 ft', '200 ft', '6 %', '175 ft', '150 ft',
               '140 ft', '5 %', '130 ft', '120 ft', '110 ft', '100 ft', '4 %']
def callid(call):
    global callout_ids
    if call in callout_ids:
        return callout_ids.index(call) + 1
    else:
        return -1

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)
subjects = natural_sort(subjects)

def allwords(hypothesis):
    words=hypothesis[0].text
    for token in hypothesis[1:]:
        words += " " + token.text
    return words

def setcall(self, ind):
        self.words = allwords(trial.hyps[ind])
        self.confidence = trial.hyps[ind].attrib['confidence']
        self.time = trial.utters[ind].attrib['start']
        self.audio = trial.audio[ind]
        self.timestamp = self.audio[-23:-4]

def setfiles(self, ind):
    self.audio = os.listdir(sub_dir + audio_folders[ind])
    self.speech = sub_dir + speech_files[ind]
    
def setcalls(self, speech_file):
    tree=ET.parse(speech_file)
    root=tree.getroot()
    self.utters=root.findall("./turn/user_input/")
    self.hyps=root.findall("./turn/user_input/utterance/")
    self.time = root[0].attrib['start']
    self.wintime = speech_file[-23:-4]
    self.ncalls = len(self.hyps)

class Trial():
    def __init__(self):
        self.index = 0
        setfiles(self, self.index)
        setcalls(self, self.speech)

    def nexttrial(self):
        self.index += 1
        setfiles(self, self.index)
        setcalls(self, self.speech)

    def lasttrial(self):
        self.index -= 1
        setfiles(self, self.index)
        setcalls(self, self.speech)

def allwords(hypothesis):
    words=hypothesis[0].text
    for token in hypothesis[1:]:
        words += " " + token.text
    return words

def setcall(self, ind):
        self.words = allwords(trial.hyps[ind])
        self.confidence = trial.hyps[ind].attrib['confidence']
        self.time = trial.utters[ind].attrib['start']
        self.audio = trial.audio[ind]
        self.timestamp = self.audio[-23:-4]
        
class CallOut():
    def __init__(self):
        self.index = 0
        setcall(self, self.index)
        
    def nextcall(self):
        self.index += 1
        setcall(self, self.index)
            
    def lastcall(self):
        if self.index == 0:
            trial.lasttrial()
            self.__init__()
        else:
            self.index -= 1
            setcall(self, self.index)


data = 0
for sub in subjects:
    sub_dir = directory + sub + '/Experiment/audio/'
    all_data=os.listdir(sub_dir)
    audio_folders = []
    for n in all_data:
                if 'audio' in n:
                    audio_folders.append(n)
    audio_folders = natural_sort(audio_folders)
    speech_files = []
    for n in all_data:
            if 'speech' in n:
                    speech_files.append(n)
    speech_files = natural_sort(speech_files)
    if speech_files[0][16] == '_':
        sub_id = speech_files[0][15]
    else:
                sub_id = speech_files[0][15:17]
    trial = Trial()
    call = CallOut()
    go = True
    while go:
            sim_time = int(call.time) - int(trial.time)
            hyp_callout = text2int(call.words)
            hyp_callout_id = callid(hyp_callout)
            new_row = [sub_id, trial.index + 1, sim_time, call.words,
                       hyp_callout, hyp_callout_id]

            if data == 0:
                data = [new_row]
            else:
                data.append(new_row)

            if trial.ncalls == call.index + 1:
                if trial.index == 23:
                    go = False
                else:
                    trial.nexttrial()
                    call = CallOut()
            else:
                call.nextcall()
                
                    


DF = pd.DataFrame(data)
cols = [ ['Subject ID', 'Trial ID', 'Simulation Time', 'Hypothesis', 'Hypothesis Callout', 'Hypothesis CalloutID'] ]
DF.columns = cols
DF.to_csv('All_Callout_Data.csv', index=False)






