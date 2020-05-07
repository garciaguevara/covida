import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
mobiVisuRes="/data/covid/visuRes"
# allMobi="/data/covid/CoronavirusMovementAdministrativeRegions"#CoronavirusMovementAdministrativeRegionsPerDay  /2020-04-02_0000.csv"
mobiTemp="/data/covid/CoronavirusMovementAdministrativeRegions/2020-04-AAAA.csv"

allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)

metric='n_crisis'; metricTh=60; trajectoryLength=30
##################################################################################################################################################################################
# Plot metric stats for all days mobility

title="Trajectories with displacement larger than {} km ".format(trajectoryLength)
metricPerFile=[]
dayRange=[2,23]
for day in range(dayRange[0],dayRange[1]): #   
    mobiAtDay=mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day))   
    with open(mobiAtDay, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        dfMX = pd.read_csv( mobiAtDay )
#     dfMX=df[df[metric]>metricTh]
    dfMore30K=dfMX[dfMX['length_km']>trajectoryLength][metric]
    _, timePoint=os.path.split(mobiAtDay)
    metricPerFile.append( [timePoint.replace('.csv',''), np.max(dfMore30K), np.min(dfMore30K), len(dfMore30K)] )

listMaxMetric=[x[1] for x in metricPerFile]
xAxis=[x for x in range(len(metricPerFile))]
fig = plt.figure(figsize=(11.0, 5.0));ax = fig.add_subplot(111);
_=plt.xticks(xAxis,[x[0][8:13] for x in metricPerFile], rotation='vertical');plt.show()
ax.plot(xAxis,listMaxMetric,'o-', label="{} Max".format(metric) );
listMinMetric=[x[2] for x in metricPerFile]
ax.plot(xAxis,listMinMetric,'cx-', label="Min")

listNumMunMetric=[x[3] for x in metricPerFile]# "Number of municipalities with more than 30 km metric disp\\ {}".format(listNumMunMetric)
ax2 = ax.twinx(); ax2.plot(xAxis,listNumMunMetric,'r^-', label="Trajectories num")
ax.set_ylabel(r"{} flow".format(metric)); ax.legend(fontsize="small", loc=6)
ax2.set_ylabel(r"Number of trajectories"); ax2.legend(fontsize="small", loc=5);plt.grid();plt.show()
metricRange = [min(listMinMetric), max(listMaxMetric)]; idxMetricRange=[listMinMetric.index(metricRange[0]), listMaxMetric.index(metricRange[1]) ];
metricRangeStr="{} min={}max={} {}".format(metric, metricPerFile[idxMetricRange[0]][0],metricPerFile[idxMetricRange[1]][0],metricRange); print(metricRangeStr)
fig.suptitle("{}\n {}".format(title, metricRangeStr) )
fig.savefig(os.path.join(mobiVisuRes,title.replace(' ', '_')+metric+".png"), bbox_inches='tight')
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
