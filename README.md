# CallOutCorrector
Simple GUI comparing ASR output with actual audio files

CalloutCorrector.py: Runs GUI allowing user to compare audio to ASR output

Files Used by CalloutCorrector.py:

config.py: Used to set the directory containing all ASR output for all subjects.
  subjectId defines which subject's data is being analyzed
  
text2int.py: Used to convert text output of ASR into number of ft or fuel percentage. ie: "four hundred feet" to "400 ft"

ReadXml.py: Used to extract relevant data from ASR output XML files. Data is organized into Trial() and CallOut() objects.

Files Used for Analysis:

CsvGen2.py: Similar to ReadXml.py. Used to generate csv file of relevant data from all subjects. 
  directory defines the path to the file containing all ASR output from all subjects
  
Analysis.py: Used to create DataFrame objects demonstrating the how often ASR output is correct.
  calls becomes a DataFrame from a csv containing the output from CalloutCorrector.py combined for all subjects
