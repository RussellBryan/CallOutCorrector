import xml.etree.ElementTree as ET
import os
import re


directory = '/Users/admin/Desktop/subjects/'
subjects = os.listdir(directory)
for s in subjects:
    if 'Subject' not in s:
        subjects.remove(s)


def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def setfiles(self, ind):
    self.audio = os.listdir(subject.dir + subject.audio_folders[ind])
    self.speech = subject.dir + subject.speech_files[ind]
    
def setcalls(self, speech_file):
    tree=ET.parse(speech_file)
    root=tree.getroot()
    self.utters=root.findall("./turn/user_input/")
    self.hyps=root.findall("./turn/user_input/utterance/")
    self.time = root[0].attrib['start']
    self.wintime = speech_file[-23:-4]
    self.ncalls = len(self.hyps)

def setsubj(self):
        self.all_data=os.listdir(self.dir)
        self.audio_folders = []
        for n in self.all_data:
            if 'audio' in n:
              self.audio_folders.append(n)
        self.audio_folders = natural_sort(self.audio_folders)
        self.speech_files = []
        for n in self.all_data:
            if 'speech' in n:
                self.speech_files.append(n)
        self.speech_files = natural_sort(self.speech_files)
        if self.speech_files[0][16] == '_':
            sef.id = self.speech_files[0][15]
        else:
            self.id = self.speech_files[0][15:17]
class Subject():
    def __init__(self):
        self.index = 0
        self.dir=directory + subjects[self.index] +'/Experiment/audio/'
        setsubj(self)

    def nextsubj(self):
        self.index += 1
        self.dir=directory + subjects[self.index] +'/Experiment/audio/'
        setsubj(self)

subject = Subject()
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
trial = Trial()

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
