import xml.etree.ElementTree as ET
import os
import re


directory = '/Users/admin/Desktop/Subject33/Experiment/audio/'
all_data=os.listdir(directory)

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

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
    subject = speech_files[0][15]
else:
    subject = speech_files[0][15:17]

def setfiles(self, index):
    self.audio = os.listdir(directory + audio_folders[index])
    self.speech = directory + speech_files[index]
    
def setcalls(self, speech_file):
    tree=ET.parse(speech_file)
    root=tree.getroot()
    self.utters=root.findall("./turn/user_input/")
    self.hyps=root.findall("./turn/user_input/utterance/")
    self.time = root[0].attrib['start']
    self.wintime = speech_file[-23:-4]


class Trial():
    def __init__(self):
        self.index =0 
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

trial=Trial()


def setcall(self, index):
        self.words = allwords(trial.hyps[index])
        self.confidence = trial.hyps[index].attrib['confidence']
        self.time = trial.utters[index].attrib['start']
        self.audio = trial.audio[index]
        
class CallOut:
    def __init__(self):
        self.index = 0
        setcall(self, self.index)
        
    def nextcall(self):
        if self.index == len(trial.hyps) -1 :
            trial.nexttrial()
            self.__init__()
        else:
            self.index += 1
            setcall(self, self.index)
            
    def lastcall(self):
        if self.index == 0:
            trial.lasttrial()
            self.__init__()
        else:
            self.index -= 1
            setcall(self, self.index)
