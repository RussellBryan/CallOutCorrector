import xml.etree.ElementTree as ET
import os

all_data=os.listdir('/Users/admin/Desktop/datas')

audio_folders = []
for n in all_data:
    if 'audio' in n:
        audio_folders.append(n)

speech_files = []
for n in all_data:
    if 'speech' in n:
        speech_files.append(n)


def setfiles(self, index):
    self.audio = os.listdir('/Users/admin/Desktop/datas/' + audio_folders[index])
    self.speech = '/Users/admin/Desktop/datas/' + speech_files[index]
    
def setcalls(self, speech_file):
    tree=ET.parse(speech_file)
    root=tree.getroot()
    self.utters=root.findall("./turn/user_input/")
    self.hyps=root.findall("./turn/user_input/utterance/")


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
class CallOut:
    def __init__(self):
        self.words=allwords(trial.hyps[0])
        self.confidence=trial.hyps[0].attrib['confidence']
        self.time=trial.utters[0].attrib['start']
        self.index = 0

    def nextcall(self):
        if self.index == len(trial.hyps) -1 :
            trial.nexttrial()
            self.__init__()
        else:
            self.index += 1
            self.words = allwords(trial.hyps[self.index])
            self.confidence = trial.hyps[self.index].attrib['confidence']
            self.time = trial.utters[self.index].attrib['start']
        
    def lastcall(self):
        if self.index == 0:
            trial.lasttrial()
            self.__init__()
        else:
            self.index -= 1
            self.words = allwords(trial.hyps[self.index])
            self.confidence = trial.hyps[self.index].attrib['confidence']
            self.time = trial.utters[self.index].attrib['start']
        
    def disp(self):
        print self.words
        print "Time Stamp:", self.time
        print "Confidence:", self.confidence
