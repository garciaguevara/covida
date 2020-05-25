import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib import ticker

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy import spatial #from sklearn.neighbors import KDTree
from scipy.sparse import *
from scipy import io
from scipy import *
import pickle
import datetime
import unicodedata
from matplotlib.colors import LinearSegmentedColormap
import colorsys
import numpy as np
import matplotlib.colors as colors
import utils as ut
import casesStats as caSts

import mobilityMatrixUtils as mobMU
    
def mobilityWithCasesPer100kMetro(dayRange):
    maxMobiFile=allMobi+"mobMatrices/metro/{}/plots/raw/maxPerDay.pkl".format(MetroArea)
    if os.path.exists(maxMobiFile):
        with open(maxMobiFile, 'rb') as extentFilePkl: #save selected hypothesis
            mobMaxPerDay=pickle.load(extentFilePkl)
        maxDefList=[]; maxDefOffDiagList=[]
        for mobMax in mobMaxPerDay:
            maxDefList.append(mobMax.max);
            maxDefOffDiagList.append(mobMax.maxOffDiag)
        maxDef=np.max(maxDefList);maxDefOffDiag=np.max(maxDefOffDiagList);
    else: maxDef=None;maxDefOffDiag=None
    
    casosMetroPath=covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}Cumulative.".format(joinByMobGeo,MetroArea))

    with open(casosMetroPath, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        casosMetroDF = pd.read_csv( casosMetroPath )
    namesMetroArea=casosMetroDF['PolygonName']; populationsMetro=casosMetroDF['poblacion'].to_numpy().astype(np.double)

    maxMobiFilePer100k=allMobi+"mobMatrices/metro/{}/plots/per100k/maxPerDayPer100k.pkl".format(MetroArea)
    if os.path.exists(maxMobiFilePer100k):
        with open(maxMobiFilePer100k, 'rb') as extentFilePkl: #save selected hypothesis
            maxMobOffDiag=pickle.load(extentFilePkl)
    else:
        maxMobOffDiag=[]
        for day in range(dayRange[0],dayRange[1]): #
            mobMatrixFile="{}mobMatrices/metro/{}/2020-04-AAAA.csv".format(allMobi,MetroArea).replace('AAAA',"{:02d}_MX{}{}".format(day,joinByMobGeo,MetroArea))
            mobMetroArea=io.mmread(mobMatrixFile.replace("csv", "mtx") ).toarray()
            
            fig = plt.figure(figsize=(20.0, 14.0)); ax = fig.add_subplot(221); mobMU.plotMobmatrix(mobMetroArea,namesMetroArea,ax, fig, limDef=maxDef ) 
            mobMetroAreaOffDiag=np.copy(mobMetroArea)
            np.fill_diagonal(mobMetroAreaOffDiag, 0);
            ax2 = fig.add_subplot(222); mobMU.plotMobmatrix(mobMetroAreaOffDiag,namesMetroArea,ax2, fig, limDef=maxDefOffDiag, verbLeg=False, sTitle='OffDiag'  ) 
            
            mobMetroAreaPer100k=(mobMetroArea*100000.0/populationsMetro[:,None])#mobMetroArea[3,1]*100000.0/populationsMetro[:,None][3] mobMetroAreaPer100k[3,1]
            ax3 = fig.add_subplot(223); mobMU.plotMobmatrix(mobMetroAreaPer100k,namesMetroArea,ax3, fig, sTitle='per100k') 
    
            mobMetroOffDiagPer100k=(mobMetroAreaOffDiag*100000.0/populationsMetro[:,None])        
            
            maxOffDiag = mobMetroOffDiagPer100k.max(); muniOffDiag = mobMetroOffDiagPer100k.argmax(); maxMobOffDiag.append(maxOffDiag)
            muniOrg=muniOffDiag/len(namesMetroArea); muniDest=muniOffDiag%len(namesMetroArea); #mobMetroArea[muniOrg,muniDest]
            maxTrajOffDiag="{}->{}".format(namesMetroArea[muniOrg], namesMetroArea[muniDest])     
            
            ax4 = fig.add_subplot(224); mobMU.plotMobmatrix(mobMetroOffDiagPer100k,namesMetroArea,ax4, fig, verbLeg=False)
    
            _,mobDate=os.path.split(mobMatrixFile); dateMetro=mobDate.replace("_MXByStartPt{}.csv".format(MetroArea)," "+MetroArea)  
            fig.suptitle( unicode("AdminRegions facebook mobility Matrix {} OffDiag Per100k  max {} traj {}".format( dateMetro, maxOffDiag, maxTrajOffDiag), 'utf-8') );
            fig.savefig(mobMatrixFile.replace("csv", "png").replace("metro/"+MetroArea, "metro/"+MetroArea+"/plots/per100k"), bbox_inches='tight')
        with open(maxMobiFilePer100k, 'wb') as extentFilePkl: #save selected hypothesis
            pickle.dump(maxMobOffDiag,extentFilePkl)

    lastDateStr="{:02d}-04-2020".format(dayRange[1]+1)
    limCases=np.max(casosMetroDF[lastDateStr].to_numpy().astype(np.double)*100000.0/populationsMetro[:,None].transpose())
    spaceBC=np.empty((len(namesMetroArea),4));spaceBC[:] = np.NaN
    
    normMobMetroAreaPer100k=colors.PowerNorm(gamma=0.5,vmax=np.max(maxMobOffDiag), clip=False)
#         normMobMetroAreaPer100k.autoscale(mobMetroAreaPer100k)#,vmax=np.max(maxMobOffDiag)
#         sm = mpl.cm.ScalarMappable(cmap=cmap, norm=normMobMetroAreaPer100k)
#         sm.set_array([])
    cmap=ut.fixInitialValueColorMap()
    muniCumCasesTH=1.0; deltaCasesTH=4.0;mobiTH=4.0 #per100k
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/metro/{}/2020-04-AAAA.csv".format(allMobi,MetroArea).replace('AAAA',"{:02d}_MX{}{}".format(day,joinByMobGeo,MetroArea))
        mobMetroArea=io.mmread(mobMatrixFile.replace("csv", "mtx") ).toarray()
        mobMetroAreaPer100k=(mobMetroArea*100000.0/populationsMetro[:,None])

        casesCum3DaysPer100k, dateStrList =mobMU.cumCasesPer100k(casosMetroDF,populationsMetro, day)
        cum3DPer100kFut, dateFutList =mobMU.cumCasesPer100k(casosMetroDF,populationsMetro, day+14)
                
        fig = plt.figure(figsize=(14.0, 9.0));  gs = gridspec.GridSpec(ncols=4, nrows=10, figure=fig)#        gs = fig.add_gridspec(4, 4)
        
        ax = fig.add_subplot( gs[0:7, 2:4] );
        pos=ax.pcolor(mobMetroAreaPer100k, cmap=cmap, norm=normMobMetroAreaPer100k, edgecolors='w', linewidth=0.01) #[:50,:50] 
#         pos=ax.imshow(mobMetroAreaPer100k, aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5), vmax=np.max(maxMobOffDiag), interpolation='None') #[:50,:50] 
#         plt.yticks(xAxis,[unicode(x,'utf-8')[:4] for x in namesMetroArea]) 
#         plt.xticks(xAxis,[unicode(x,'utf-8')[:4] for x in namesMetroArea], rotation='vertical')
        xAxis=[x+0.5 for x in range(len(namesMetroArea))]
        ax.set_yticks(xAxis); ax.set_yticklabels( [unicode(x,'utf-8')[:4] for x in namesMetroArea] )
        ax.set_xticks(xAxis); ax.set_xticklabels( [unicode(x,'utf-8')[:4] for x in namesMetroArea], rotation='vertical' )
        ax.set_ylabel("Origin");ax.set_xlabel("Destination")
        fig.colorbar(pos, ax=ax) ;                
#         # Major ticks
#         ax.grid(color='w', linestyle='-', linewidth=2)
#         ax.set_xticks(np.arange(0, mobMetroAreaPer100k.shape[0], 1));
#         ax.set_yticks(np.arange(0, mobMetroAreaPer100k.shape[1], 1))
#         # Labels for major ticks
#         ax.set_xticklabels(np.arange(1, mobMetroAreaPer100k.shape[0]+1, 1));
#         ax.set_yticklabels(np.arange(1, mobMetroAreaPer100k.shape[1]+1, 1));#          
#         # Minor ticks
#         ax.set_xticks(np.arange(-.5, mobMetroAreaPer100k.shape[0], 1), minor=True);
#         ax.set_yticks(np.arange(-.5, mobMetroAreaPer100k.shape[1], 1), minor=True);        
        # Gridlines based on minor ticks
#         ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
        _,mobDate=os.path.split(mobMatrixFile); fig.suptitle("AdminRegions mobility per 100k {} OffDiagVmax={}".format(mobDate.replace("_MXByStartPt{}.csv".format(MetroArea)," "+MetroArea), np.max(maxMobOffDiag) ) );
        
        ax1 = fig.add_subplot(gs[0:7, :2]);  
        casesPer100kPF=np.concatenate((casesCum3DaysPer100k,spaceBC,cum3DPer100kFut ), axis=1)
        for i in xrange(4): dateStrList.append(".")
        dateStrList+=dateFutList        
        pos=ax1.pcolor(casesPer100kPF,  cmap=cmap, vmax=limCases,  edgecolors='w', linewidth=0.01 ) #[:50,:50] aspect='equal', norm=colors.PowerNorm(gamma=0.5),
#         plt.yticks(xAxis,[unicode(x,'utf-8') for x in namesMetroArea])
#         plt.xticks(xAxis[:len(dateStrList)],[unicode(x,'utf-8')[:5] for x in dateStrList], rotation='vertical')
        ax1.set_yticks(xAxis); ax1.set_yticklabels( [unicode(x,'utf-8') for x in namesMetroArea] )
        ax1.set_xticks(xAxis[:len(dateStrList)]); ax1.set_xticklabels( [unicode(x,'utf-8')[:5] for x in dateStrList], rotation='vertical' )
        ax1.set_xlabel("Date"); ax1.set_ylabel("Cases per 100k"); fig.colorbar(pos, ax=ax1)
        
        deltaCasesPer100k=(cum3DPer100kFut-casesCum3DaysPer100k)
        deltaCasesMax=np.max(deltaCasesPer100k,axis=1); casesCumMax=np.max(casesCum3DaysPer100k,axis=1);
        muniLargeIncre = np.where(deltaCasesMax>deltaCasesTH)[0]
        
        for muniL in muniLargeIncre:        
            orgMunisMob=mobMetroAreaPer100k[:,muniL]#.tolist()
            orgMunisIdx=np.where(orgMunisMob>mobiTH)[0].tolist() #ox=[]; dx=[]; dy=[];orgMunis=[]
            for idx in xrange(len(orgMunisIdx)):
#                 ox.append(3); dx.append(4); dy.append(muniL+0.5); 
#                 orgMunis.append(orgMunisIdx[idx]+0.5)                
                if casesCumMax[orgMunisIdx[idx]]>muniCumCasesTH:
                    colMap=cmap(normMobMetroAreaPer100k( orgMunisMob[orgMunisIdx[idx]] ) )
                    pl = plt.plot([3,7],[(orgMunisIdx[idx]+0.5), muniL+0.5],color=colMap)            
#             plt.quiver(ox, orgMunis, dx, dy, color=cmap(norm( orgMunisMob[orgMunisIdx].tolist() )) , scale=2,angles='xy')

        ax4 = fig.add_subplot(gs[8:11, 2:4]);
        pos=ax4.pcolor(deltaCasesPer100k.transpose(),  cmap=cmap, edgecolors='w', linewidth=0.01 ) #[:50,:50] aspect='equal',vmax=limCases, ,  norm=colors.PowerNorm(gamma=0.5)
#         plt.yticks(xAxis[:len(dateFutList)],[unicode(x,'utf-8')[:5] for x in dateFutList])
#         plt.xticks(xAxis,[unicode(x,'utf-8')[:5] for x in namesMetroArea ], rotation='vertical')
#         ax4 = fig.add_subplot(223); 
        ax4.set_yticks(xAxis[:len(dateFutList)]); ax4.set_yticklabels( [unicode(x,'utf-8')[:5] for x in dateFutList] )
        ax4.set_xticks(xAxis); ax4.set_xticklabels( [unicode(x,'utf-8')[:5] for x in namesMetroArea ], rotation='vertical' )
        ax4.set_xlabel("Cases per 100k delta"); ax4.set_ylabel("Date-14")

        cb=fig.colorbar(pos, ax=ax4); tick_locator = ticker.MaxNLocator(nbins=5)
        cb.locator = tick_locator;  cb.update_ticks()
        fig.savefig(mobMatrixFile.replace("csv", "png").replace("metro/"+MetroArea, "metro/"+MetroArea+"/plots/casesPer100k"), bbox_inches='tight');
    
    
def main():
    dayRange=[2,23]
#     computeMobilityMatrix(dayRange)
#     getMobilityPerMetropolitanAreaMatrix(dayRange) #, normalize=False
    mobilityWithCasesPer100kMetro(dayRange)
    
mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos= "/data/covid/casos/12_05/Casos_Diarios_Municipio_Confirmados_20200512.csv" #"/data/covid/casos/12_05/Casos_Diarios_Estado_Nacional_Confirmados_20200512.csv" #/data/covid/casos/27_04
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
baselinePerFile=[]; getCountry='MX'#'GT'#
joinByMobGeo="ByStartPt";  MetroArea="MTY"; metroType="";MetroArea+=metroType       #""    

if __name__ == "__main__":
    main()

    