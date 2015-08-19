import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats, integrate
import seaborn as sns
import os

res = pd.DataFrame.from_csv('callout_results.csv')
Type = []
Timing = []
for i in range(15304):
    ID = res.iloc[i]['ID']
    t = res.iloc[i]['t']
    if t<0:
        time = 'Anticipated'
    else:
        time = 'Late'
    if ID != -1:
        if ID in [4, 9, 13, 18]: #Fuel Callouts
            typ = 'Fuel'
        else:
            typ = 'Altitude'
    Type.append(typ)
    Timing.append(time)
res['Type'] = pd.Series(Type)
res['Timing'] = pd.Series(Timing)

calls = res.dropna().query('-1< t < 5')

allcalls = calls.groupby('ID').t
allcalls.plot(yerr=allcalls.sem(), marker='*', linestyle='None')
plt.ylabel('Time Delay (s)')
plt.xlabel('Callout ID')
plt.xticks(range(20))
plt.savefig('TimeDelaybyCallout.pdf')
plt.clf()

lpr = calls.query("LPR==True").groupby('ID').t
lpr.mean().plot(yerr=lpr.sem(), marker='*', linestyle='None', label='LPR')
nlpr = calls.query("LPR==False").groupby('ID').t
nlpr.mean().plot(yerr=nlpr.sem(), marker='*', linestyle='None', label='No LPR')
plt.ylabel('Time Delay (s)')
plt.xlabel('Callout ID')
plt.legend()
plt.xticks(range(20))
plt.savefig('LPR_Time_Delay.pdf')
plt.clf()

pitch = calls.query('Mode=="PITCH"').groupby('ID').t
pitch.mean().plot(yerr=pitch.sem(), marker='*', linestyle='None', label='PITCH')
axis = calls.query('Mode=="2-AXIS"').groupby('ID').t
axis.mean().plot(yerr=axis.sem(), marker='*', linestyle='None', label='2-AXIS')
rod = calls.query('Mode=="2-AXIS+ROD"').groupby('ID').t
rod.mean().plot(yerr=rod.sem(), marker='*', linestyle='None', label='2-AXIS+ROD')
plt.ylabel('Time Delay (s)')
plt.xlabel('Callout ID')
plt.legend()
plt.xticks(range(20))
plt.savefig('Mode_Time_Delay.pdf')
