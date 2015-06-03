import pandas as pd

calls = pd.read_csv('transcribed_callouts.csv')

correct = []
for ind in range(len(calls['Transcribed Callout ID'])):
    hyp = calls['Hypothesis CalloutID'][ind]
    tran = calls['Transcribed Callout ID'][ind]
    correct.append(str(hyp) in str(tran))

correct = pd.Series(data=correct, name='Correct?')

calls = pd.concat([calls, correct], axis=1)




trial_avg = calls.groupby('Trial ID').mean()['Correct?']
subject_avg = calls.groupby('Subject ID').mean()['Correct?']
call_avg = calls.groupby('Hypothesis CalloutID').mean()['Correct?']
total_avg = calls.mean()['Correct?']


