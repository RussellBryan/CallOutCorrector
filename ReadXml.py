import xml.etree.ElementTree as ET
import os

os.chdir('/Users/admin/Desktop/')
tree=ET.parse('speech_test.xml')
root=tree.getroot()

utters=root.findall("./turn/user_input/")
hyps=root.findall("./turn/user_input/utterance/")


callout=[]
for hyp in hyps:
    callout.append([word.text for word in hyp])

def allwords(hypothesis):
    words=hypothesis[0].text
    for token in hypothesis[1:]:
        words += " " + token.text
    return words

class CallOut:
    def __init__(self):
        self.words=allwords(hyps[0])
        self.confidence=hyps[0].attrib['confidence']
        self.time=utters[0].attrib['start']
        self.index = 0

    def nextcall(self):
        self.index += 1
        self.words = allwords(hyps[self.index])
        self.confidence = hyps[self.index].attrib['confidence']
        self.time = utters[self.index].attrib['start']

    def lastcall(self):
        self.index -= 1
        self.words = allwords(hyps[self.index])
        self.confidence = hyps[self.index].attrib['confidence']
        self.time = utters[self.index].attrib['start']
        
    def disp(self):
        print Call.words
        print "Time Stamp:", Call.time
        print "Confidence:", Call.confidence


def test():
    Call=CallOut()
    CallOut.disp(Call)
    CallOut.nextcall(Call)
    CallOut.disp(Call)
    CallOut.lastcall(Call)
    CallOut.disp(Call)





