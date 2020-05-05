import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/fb26PerDay"#/2020-04-02_0000.csv"
mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="/data/covid/fb26PerDay/2020-04-AAAA.csv"
##################################################################################################################################################################################
#Join databases per day
title="Municipalities with displacement larger 30 km per day"
baselinePerFile=[]; getCountry='MX'#'GT'#

# def computeFlow(dataMob):
#     dataMob.insert(20,'flow',0)
#     for idx, traj in dataMob.iterrows():
#         dataMob.at[idx,'flow']=traj['n_baseline']+traj['n_difference'] #dataMob.head(1)['flow']

def mergeMobilities(dfA, dfB):
    print(dfB.shape)
    for idx, traj in dfA.iterrows():
        dropIdxsB=[]
        for idxB,trajB in dfB[ dfB['start_polygon_name']==traj['start_polygon_name'] ].iterrows():
            if traj['end_polygon_name'] == trajB['end_polygon_name']:
                sumBase=traj['n_baseline']+trajB['n_baseline']; sumDiff=traj['n_difference']+trajB['n_difference']
                sumCrisis=traj['n_crisis']+trajB['n_crisis']
                dfA.at[idx,'n_baseline']=sumBase # dfA.head(1)['n_baseline']; traj['n_baseline'];trajB['n_baseline'];traj['n_baseline']+trajB['n_baseline']
                dfA.at[idx,'n_difference']=sumDiff #
                dfA.at[idx,'percent_change']=sumDiff/sumBase
                dfA.at[idx,'n_crisis']=sumCrisis
                # dfA.at[idx,'flow']=sumDiff+sumBase
                dropIdxsB.append(idxB)

        dfB.drop(dropIdxsB, inplace = True)

    print(dfB.shape)
    print(dfA.shape)

    dfMerged=pd.concat([dfA, dfB], ignore_index=True,sort=False)
    print(dfMerged.shape)
    return dfMerged


for day in range(2,26): #day=3#
    with open(mobiTemp.replace('AAAA',"{:02d} 0000".format(day)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        df00 = pd.read_csv( mobiTemp.replace('AAAA',"{:02d} 0000".format(day)) )
    with open(mobiTemp.replace('AAAA',"{:02d} 0800".format(day)), 'r') as f:
        df08 = pd.read_csv( mobiTemp.replace('AAAA',"{:02d} 0800".format(day)) )
    with open(mobiTemp.replace('AAAA',"{:02d} 1600".format(day)), 'r') as f:
        df16 = pd.read_csv( mobiTemp.replace('AAAA',"{:02d} 1600".format(day)) )
    df00mx=df00[getCountry==df00['country']];df08mx=df08[getCountry==df08['country']];df16mx=df16[getCountry==df16['country']]

    # computeFlow(df00mx);computeFlow(df08mx); computeFlow(df16mx);

    # df00mx['start_polygon_name']['end_polygon_name'] df00mx.head(1)['n_baseline']
    df00mxMerged=mergeMobilities(df00mx, df08mx);print(df00mxMerged.shape)
    df00mxMerged=mergeMobilities(df00mxMerged, df16mx);print(df00mxMerged.shape)

    df00mxMerged.to_csv(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)),index=False)
    print(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)))

# df00mx=df00mx[1:10];df08mx=df08mx[1:10];df16mx=df16mx[1:10]
# areSame = df00mx['start_polygon_name']==df08mx['start_polygon_name']
# for muni in areSame:
#     if not muni: print("ERROR {}".format(muni) ); break;
#
#
# dfSum=df00mx['n_baseline']+df08mx['n_baseline']
#
# dfMore30K=dfMX[dfMX['length_km']>30]['n_baseline']
# baselinePerFile.append( [timePoint.replace('.csv',''), np.max(dfMore30K), np.min(dfMore30K), len(dfMore30K)] )
#
# listMaxBase=[x[1] for x in baselinePerFile]
# xAxis=[x for x in range(len(baselinePerFile))]
# fig = plt.figure(figsize=(11.0, 5.0));ax = fig.add_subplot(111);
# _=plt.xticks(xAxis,[x[0][8:13] for x in baselinePerFile], rotation='vertical');plt.show()
# ax.plot(xAxis,listMaxBase,'o-', label="Baseline Max");
# listMinBase=[x[2] for x in baselinePerFile]
# ax.plot(xAxis,listMinBase,'cx-', label="Min")
#
# listNumMunBase=[x[3] for x in baselinePerFile]# "Number of municipalities with more than 30 km baseline disp\\ {}".format(listNumMunBase)
# ax2 = ax.twinx(); ax2.plot(xAxis,listNumMunBase,'r^-', label="municipalities num")
# ax.set_ylabel(r"Baseline flow"); ax.legend(fontsize="small", loc=6)
# ax2.set_ylabel(r"Number of municipalities"); ax2.legend(fontsize="small", loc=5);plt.grid();plt.show()
# baselineRange = [min(listMinBase), max(listMaxBase)]; idxBaseRange=[listMinBase.index(baselineRange[0]), listMaxBase.index(baselineRange[1]) ];
# baseRangeStr="Baseline min={}\nmax={} in series".format(baselinePerFile[idxBaseRange[0]],baselinePerFile[idxBaseRange[1]]); print(baseRangeStr)
# fig.suptitle("{}, out of {} in MX\n {}".format(title,dfMX.shape[0], baseRangeStr) )
# fig.savefig(os.path.join(mobiVisuRes,title.replace(' ', '')+".png"), bbox_inches='tight')
# #Result # Baseline min=['2020-04-02 0000', 5303.1999999999998, 10.0, 2296] max=['2020-04-08 0000', 5455.8000000000002, 10.0, 2091] in series
