import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/CoronavirusMovementAdministrativeRegions"#CoronavirusMovementAdministrativeRegionsPerDay ·/2020-04-02_0000.csv"
mobiTemp="/data/covid/CoronavirusMovementAdministrativeRegions/2020-04-AAAA.csv"


metric='flow'; metricTh=60
##################################################################################################################################################################################
title="Municipalities with displacement larger 30 km"
metricPerFile=[]
for timePoint in sorted(os.listdir(allMobi)):
    with open(os.path.join(allMobi, timePoint), 'r') as f:  #os.path.join(allMobi, timePoint)
        df = pd.read_csv( os.path.join(allMobi, timePoint) )
    dfMX=df[df[metric]>60]
    dfMore30K=dfMX[dfMX['length_km']>30][metric]
    metricPerFile.append( [timePoint.replace('.csv',''), np.max(dfMore30K), np.min(dfMore30K), len(dfMore30K)] )

listMaxMetric=[x[1] for x in metricPerFile]
xAxis=[x for x in range(len(metricPerFile))]
fig = plt.figure(figsize=(11.0, 5.0));ax = fig.add_subplot(111);
_=plt.xticks(xAxis,[x[0][8:13] for x in metricPerFile], rotation='vertical');plt.show()
ax.plot(xAxis,listMaxMetric,'o-', label="{} Max".format(metric) );
listMinMetric=[x[2] for x in metricPerFile]
ax.plot(xAxis,listMinMetric,'cx-', label="Min")

listNumMunMetric=[x[3] for x in metricPerFile]# "Number of municipalities with more than 30 km metric disp\\ {}".format(listNumMunMetric)
ax2 = ax.twinx(); ax2.plot(xAxis,listNumMunMetric,'r^-', label="municipalities num")
ax.set_ylabel(r"{} flow".format(metric)); ax.legend(fontsize="small", loc=6)
ax2.set_ylabel(r"Number of municipalities"); ax2.legend(fontsize="small", loc=5);plt.grid();plt.show()
metricRange = [min(listMinMetric), max(listMaxMetric)]; idxMetricRange=[listMinMetric.index(metricRange[0]), listMaxMetric.index(metricRange[1]) ];
metricRangeStr="{} min={}\nmax={} in series".format(metric, metricPerFile[idxMetricRange[0]],metricPerFile[idxMetricRange[1]]); print(metricRangeStr)
fig.suptitle("{}, out of {} in MX\n {}".format(title,dfMX.shape[0], metricRangeStr) )
fig.savefig(os.path.join(mobiVisuRes,title.replace(' ', metric)+".png"), bbox_inches='tight')
#Result # Metricline min=['2020-04-02_0000', 5303.1999999999998, 10.0, 2296] max=['2020-04-08_0000', 5455.8000000000002, 10.0, 2091] in series



##################################################################################################################################################################################

for hpd in allMobi:
    df = pd.read_csv (r'/data/covid/MexicoCoronavirusDiseasePreventionMapApr032020IdMovementbetweenAdministrativeRegions_2020-04-020800.csv')
df = pd.read_csv (r"/data/covid/CoronavirusMovementAdministrativeRegions/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-03 0000.csv")
maxbaselinePerFile.append( [timePoint, df[df['length_km']>30]['n_baseline'].max()] )

# block 1 - simple stats
mean1 = df['Salary'].mean()
sum1 = df['Salary'].sum()
df30k = df['length_km']>30
