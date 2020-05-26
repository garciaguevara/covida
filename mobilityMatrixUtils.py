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


class mobilityMatrixMetric:
    def __init__(self,dateMob, maxMob,maxTrajMob, maxOffDiagMob,maxTrajOffDiagMob):
        self.date=dateMob        
        self.max=maxMob
        self.maxTraj=maxTrajMob        
        self.maxOffDiag=maxOffDiagMob
        self.maxTrajOffDiag=maxTrajOffDiagMob
        
class municipality:
    def __init__(self,name, coord,cve):
        self.name=name        
        self.coord=coord
        self.cve=cve        
#         self.maxOffDiag=maxOffDiagMob
#         self.maxTrajOffDiag=maxTrajOffDiagMob

class metroAreaAdminReg:
    def __init__(self,name, polyID,coord):
        self.PolygonName=name        
        self.PolygonID=polyID
        self.coord=coord
        self.cves_mun=[]        
#         self.maxOffDiag=maxOffDiagMob
#         self.maxTrajOffDiag=maxTrajOffDiagMob
def compareMatchedCoords(matched, centMunisPts, metroPt, limDist=False):    
    tree = spatial.KDTree(centMunisPts[matched]) #KDTree(
    nearest_dist, nearest_idx = tree.query(metroPt, k=1) #.query_radius(points, r=1.5)   
    if limDist and nearest_dist>limDist:
        print( "WARNING Nearest dist {}".format(nearest_dist) )
    return matched[nearest_idx]


def plotMobmatrix(mobMetroArea,namesMetroArea,ax,fig, verbLeg=True,limDef=None, sTitle=""):
    cmap=ut.fixInitialValueColorMap()
    if limDef is None:
#         pos=ax.imshow(mobMetroArea, aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50]    
        normMobMetroAreaPer100k=colors.PowerNorm(gamma=0.5, clip=True);normMobMetroAreaPer100k.autoscale(mobMetroArea)
#        WARNING: pcolormesh DOES NOT WORK DIAG!!!
        pos=ax.pcolor(mobMetroArea, cmap=cmap, norm=normMobMetroAreaPer100k, edgecolors='w', linewidth=0.005 ) #[:50,:50]   
    else:
#         pos=ax.imshow(mobMetroArea, aspect='equal', cmap=cmap, vmax=limDef, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50]    
        normMobMetroAreaPer100k=colors.PowerNorm(gamma=0.5,vmax=limDef, clip=False);
        pos=ax.pcolor(mobMetroArea, cmap=cmap, norm=normMobMetroAreaPer100k, edgecolors='w', linewidth=0.005 ) #[:50,:50]   
        
    xAxis=[x+0.5 for x in range(len(namesMetroArea))] #xAxis=[x for x in range(len(namesMetroArea))];
    
#     plt.xticks(xAxis,[unicode(x,'utf-8')[:4] for x in namesMetroArea], rotation='vertical')        
    ax.set_xticks(xAxis); ax.set_xticklabels( [unicode(x,'utf-8')[:4] for x in namesMetroArea], rotation='vertical' )
    fig.colorbar(pos, ax=ax); 
    
    if verbLeg:
        ax.set_ylabel("Origin " +sTitle); 
#         plt.yticks(xAxis, [unicode(x,'utf-8') for x in namesMetroArea])
        ax.set_yticks(xAxis); ax.set_yticklabels( [unicode(x,'utf-8') for x in namesMetroArea] )
    else:
        namesMetroAreaStr=[]
        for idx, x in zip(xrange(len(namesMetroArea)),namesMetroArea):
#             if idx ==11:
#                 print ("Id={}".format(idx))
            namesMetroAreaStr.append( unicode(str(idx)+' '+x,'utf-8')[:7] )        
        ax.set_yticks(xAxis); ax.set_yticklabels( namesMetroAreaStr );#plt.yticks(xAxis,namesMetroAreaStr)
        ax.set_title(sTitle)
    
    ax.set_xlabel("Destination"); 


#colors.LogNorm(vmin=mobMetroArea.toarray().min()+.0000000001, vmax=mobMetroArea.toarray().max())
#         plt.clim(10, np.max(mobMetroArea.toarray()) );                
#         fig = plt.figure(figsize=(11.0, 5.0));ax2 = fig.add_subplot(111);
#         plt.spy(mobMetroArea, markersize=4)
# fig = plt.figure(figsize=(11.0, 5.0));ax = fig.add_subplot(111);
# pos=ax.imshow(mobility[:200,:200].toarray(), aspect='auto', cmap='jet', norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50]
# #colors.LogNorm(vmin=mobMetroArea.toarray().min()+.0000000001, vmax=mobMetroArea.toarray().max())
# fig.colorbar(pos, ax=ax)
#         pcm = ax[0].pcolor(X, Y, Z, norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
#         fig.colorbar(pcm, ax=ax[0], extend='max')
def cumCasesPer100k(casosMetroDF,populationsMetro,day):
    dateStrList=[];
    dateStr="{:02d}-04-2020".format(day)
    date_1 = datetime.datetime.strptime(dateStr, "%d-%m-%Y")        
    for dRange in xrange(-1,2):
        dateRange=date_1 + datetime.timedelta(days=dRange)
        dateRangeStr="{:02d}-{:02d}-2020".format(dateRange.day,dateRange.month)
        dateStrList.append(dateRangeStr)
        
    casesCum3Days=casosMetroDF[dateStrList].to_numpy().astype(np.double) #cum3=casesCum3Days*100000.0/populationsMetro[:,None]
    return casesCum3Days*100000.0/populationsMetro[:,None], dateStrList #casesCum3Days[1,2]*100000.0/populationsMetro[:,None][1]
    

    
    
def main():
    dayRange=[2,23]
#     computeMobilityMatrix(dayRange)
#     getMobilityPerMetropolitanAreaMatrix(dayRange) #, normalize=False
#     mobilityWithCasesPer100kMetro(dayRange)
    
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

    