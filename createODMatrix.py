import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/fb26PerDay"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="/data/covid/fb26PerDay/2020-04-AAAA.csv"
covCasos="/data/covid/casos/Casos_Diarios_Estado_Nacional_Confirmados.csv"
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
#Join databases per day
# title="Municipalities with displacement larger 30 km per day"
baselinePerFile=[]; getCountry='MX'#'GT'#

# def computeFlow(dataMob):
#     dataMob.insert(20,'flow',0)
#     for idx, traj in dataMob.iterrows():
#         dataMob.at[idx,'flow']=traj['n_baseline']+traj['n_difference'] #dataMob.head(1)['flow']

import unicodedata


def numberOfNonMatchLetters(a,b):
    u=zip(a,b)
    d=dict(u)    
    x=0
    for i,j in d.items():
        if i==j:
            x=+1
    return x


def addCentroidToMunicipalCases(casosDF):            
    with open(centroidPath, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        centroidDF = pd.read_csv( centroidPath )
    
    dropIdxsB=[]
    print(casosDF.shape)
    casosDF.insert(0,'X',0.0); casosDF.insert(1,'Y',0.0)
    print(casosDF.shape)
    for idx, casosMun in casosDF.iterrows():
        centroidMun=centroidDF[casosMun["cve_ent"]==centroidDF['CVE_MUN']]
        
        encoded1 = unicodedata.normalize('NFC', casosMun["nombre"].decode('utf8'))
        encoded2 = unicodedata.normalize('NFC', centroidMun["NOM_MUN"].values[0].decode('utf8'))

        
        if np.sum(casosMun["cve_ent"]==centroidDF['CVE_MUN'])==1 and numberOfNonMatchLetters(encoded1,encoded2)<3:
            casosDF.at[idx,'X']=centroidMun['X'].values[0]
            casosDF.at[idx,'Y']=centroidMun['Y'].values[0]
#             dropIdxsB.append(centroidMun.idx)#(casosMun["cve_ent"])
        else: 
            print("Not the same name casos {} centroid {}".format(casosMun["nombre"], encoded2))  
              
    casosDF.to_csv(covCasos.replace('.',"Centroids."),index=False)
    print(covCasos.replace( '.',"Centroids." ) )
#     dfB.drop(dropIdxsB, inplace = True)
#     return dfMerged


with open(covCasos, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
     casosDF = pd.read_csv( covCasos )
adminRegPerDay=[]; totalReg=set([])
for day in range(2,26): #
    with open(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        mobiDF = pd.read_csv( mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)) )
        #     with open(mobiTemp.replace('AAAA',"{:02d} 0800".format(day)), 'r') as f:
        #         df08 = pd.read_csv( mobiTemp.replace('AAAA',"{:02d} 0800".format(day)) )
        #     with open(mobiTemp.replace('AAAA',"{:02d} 1600".format(day)), 'r') as f:
        #         df16 = pd.read_csv( mobiTemp.replace('AAAA',"{:02d} 1600".format(day)) )
        # admRegNameStart=mobiDF.start_polygon_name.unique(); admRegNameEnd=mobiDF.end_polygon_name.unique();admRegNameStart.size; admRegNameEnd.size
    admRegIdStart=mobiDF.start_polygon_id.unique(); admRegIdEnd=mobiDF.end_polygon_id.unique();
    admRegSetStart=set(admRegIdStart);admRegSetEnd=set(admRegIdEnd)

    if admRegIdStart.size == admRegIdEnd.size and len( admRegSetEnd.difference(admRegSetStart) ) == 0:
        if len( totalReg.difference(admRegSetStart) ) != 0 or len(admRegSetStart.difference(totalReg)) :  
            totalReg=totalReg.union(admRegSetStart); #print("totalReg size start {}".format(len(totalReg)))
            totalReg=totalReg.union(admRegSetEnd); #print("totalReg size end {}".format(len(totalReg)))
    else: 
        print("Different Id startEnd size {} ".format( len( admRegSetEnd.difference(admRegSetStart) ) ) )

print("TotalReg mobility municipios size end {}".format(len(totalReg)))

muniName= casosDF.nombre.unique();muniCVE= casosDF.cve_ent.unique()
print("Total municipios number with cases by CVE {} and by Name {}".format(muniCVE.size, muniName.size) )

addCentroidToMunicipalCases(casosDF)



# casosDFmx= casosDF[getCountry== casosDF['country']];df08mx=df08[getCountry==df08['country']];df16mx=df16[getCountry==df16['country']]
# # computeFlow( casosDFmx);computeFlow(df08mx); computeFlow(df16mx);
# 
# #  casosDFmx['start_polygon_name']['end_polygon_name']  casosDFmx.head(1)['n_baseline']
# casosDFmxMerged=mergeMobilities( casosDFmx, df08mx);print( casosDFmxMerged.shape)
# casosDFmxMerged=mergeMobilities( casosDFmxMerged, df16mx);print( casosDFmxMerged.shape)
# 
# casosDFmxMerged.to_csv(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)),index=False)
# print(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)))

#  casosDFmx= casosDFmx[1:10];df08mx=df08mx[1:10];df16mx=df16mx[1:10]
# areSame =  casosDFmx['start_polygon_name']==df08mx['start_polygon_name']
# for muni in areSame:
#     if not muni: print("ERROR {}".format(muni) ); break;
#
#
# dfSum= casosDFmx['n_baseline']+df08mx['n_baseline']
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
