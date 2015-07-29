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

valid_calls = res.dropna().query('-1< t < 5')

def GenData(calls, parameter):
    # actual value +/- err for grouping
    calls.groupby([parameter, 'Subject']).mean().reset_index().groupby(parameter).t.agg(["mean", "sem", "count"]
        ).to_csv(parameter + ' sbjs sem.csv', float_format='%11.2f')

    # data for testing significance
    calls.groupby([parameter, 'Subject']).t.agg(["mean", "count"]).reset_index(
        ).to_csv(parameter + ' mean_count.csv', index=False, float_format='%11.2f')


    # a fine plot
    d = calls.groupby([parameter, 'Subject']).t.mean().reset_index().groupby(parameter).t.plot(kind='kde')
    plt.legend();
    plt.xlabel('Time')
    plt.savefig(parameter + ".pdf"); plt.clf();


os.chdir('/Users/admin/Documents/CallOutCorrector/All')
calls = valid_calls
GenData(calls, 'Type')
GenData(calls, 'LPR')
GenData(calls, 'Mode')
# actual value +/- err for grouping
all_sbj = calls.groupby('Subject').t.mean()
overall = pd.DataFrame([all_sbj.mean(), all_sbj.sem(), all_sbj.count()]).T
overall.columns = ['mean', 'sem', 'count']
overall.to_csv('overall sbjs sem.csv', index=False)
# data for testing significance
calls.groupby('Subject').t.agg(["mean", "count"]).to_csv('overall mean_count.csv', index=False )
# a fine plot
calls.groupby('Subject').t.mean().plot(kind='kde')
plt.xlabel('Time')
plt.legend(); plt.savefig("overall.pdf"); plt.clf()

os.chdir('/Users/admin/Documents/CallOutCorrector/Altitude')
calls = valid_calls.query('Type == "Altitude"')
GenData(calls, 'LPR')
GenData(calls, 'Mode')
GenData(calls,'Timing')

os.chdir('/Users/admin/Documents/CallOutCorrector/Fuel')
calls = valid_calls.query('Type == "Fuel"')
GenData(calls, 'LPR')
GenData(calls, 'Mode')

os.chdir('/Users/admin/Documents/CallOutCorrector/')
