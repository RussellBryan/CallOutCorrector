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
  directory is a string variable that defines the path to the folder containing all ASR output for all subjects
  
    this folder should contain a folder for each subject labeled "Subject[#]"
    
      each subject folders should contain a folder named "Experiment" with in this folder there should be folders of audio files that corespond to ASR output XML files such that a path to a particular audio file should have the form,
      
      directory + 'Subject30/Experiment/audio/audio-subject_30_trial_1_12-12-2014_14_04_30'
      
  From this input of a path to subject data, this script will output a csv of with columns; 'Subject ID', 'Trial ID', 'Simulation Time', 'Hypothesis', 'Hypothesis Callout', 'Hypothesis CalloutID'

Analysis.py: Used to create DataFrame objects demonstrating the how often ASR output is correct.
  calls becomes a DataFrame from a csv containing the output from CalloutCorrector.py combined for all subjects
  
  the input to this script is the string 'transcribed_callouts.csv' this should be the name of a csv file with columns; 'Subject ID', 'Trial ID', 'Windows Timestamp', 'Simulation Timestamp', 'Hypothesis', 'Hypothesis Callout', 'Hypothesis CalloutID', 'Transcribed Utterance', 'Transcribed Callout', 'Transcribed Callout ID', 'Confidence', 'ASR Scoring Time'
  
  this script has no output but creates the variables; subject_avg, trial_avg, call_avg, and  total_avg which are DataFrames of the percentage ASR was correct
  
