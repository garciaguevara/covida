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

def computeMobilityMatrix(dayRange):    
    if os.path.exists(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo)):
        with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'rb') as matchTreeFile:
            tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay = pickle.load(matchTreeFile)    
    
#     adminRegPerDay=[]; totalReg=[];totalGeoLoc=[]; totalGeoLocName=[];
#     totalRegSet=set([]); totalLargerChangeLoc=[]       
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo))
        if os.path.exists(mobMatrixFile.replace("csv", "mtx")):
            print ("Mobility matrix exists {}".format(mobMatrixFile.replace("csv", "mtx"))); continue
        with open(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
            mobiDF = pd.read_csv( mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)) )
        
        mobility=lil_matrix( ( len(tReg), len(tReg) ), dtype=int64 ) #csr_matrix
        
#         admRegIdStart=mobiDF.start_polygon_id.unique(); admRegIdEnd=mobiDF.end_polygon_id.unique();
#         admRegSetStart=set(admRegIdStart);admRegSetEnd=set(admRegIdEnd)        

#         #split geometry
#         test = mobiDF["geometry"].str.replace("LINESTRING \(", "", n=1)
#         test=test.str.replace("\)", "", n=1)
#         test = test.str.split(",", n=1, expand=True)            
#         #TODO: geometry with start end lat lons
#         testStart = test[0].str.split(" ", n=1, expand=True);    testEnd = test[1].str.split(" ", n=2, expand=True)#testEnd=test.str.replace(",", "", n=1)
#         mobiDF["geoStartLat"]= testStart[1].astype('float64');    mobiDF["geoStartLon"]= testStart[0].astype('float64')#convert_objects(convert_numeric=True) #
#         mobiDF["geoEndLat"]= testEnd[2].astype('float64');    mobiDF["geoEndLon"]= testEnd[1].astype('float64')
#         geoLoc=[]; geoLocName=[]; largerChangeLoc=[]        
#         test = pd.DataFrame(columns = ['start_lon', 'start_lat','end_lon', 'end_lat'])
#         test['start_lon']=mobiDF['start_lon'].transform(lambda x: "LINESTRING ("+str(x))
#         test['start_lat']=mobiDF['start_lat'].transform(lambda x: " "+str(x)+", ")
#         test['end_lon']=mobiDF['end_lon'].transform(lambda x: str(x)+" ")
#         test['end_lat']=mobiDF['end_lat'].transform(lambda x: str(x)+")")            
#         mobiDF["geometryStartEnd"]= test[['start_lon', 'start_lat','end_lon', 'end_lat']].agg(''.join, axis=1)
# #         df['period'] = df[['Year', 'quarter', ...]].agg('-'.join, axis=1)#         mobiDF[['start_lon', 'start_lat','end_lon', 'end_lat']].agg( lambda x: ', '.join(str(x)), axis=1 ) 
        for mobIdx,admRegID, admRegName in zip(xrange(len(tReg)), tReg, tGeoLocName): #TODO: Only look for non added, or compare the diff coordinates
            if len(mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values)>0:
                idName=mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values[0]
                if admRegName!=idName:
                    print("AdminRegions name {} diff {}".format(admRegName,idName) )
            else:
                 print("AdminRegions name not found in mobility data {} diff {}".format(admRegName,mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values) )
                 
            O_idD=mobiDF[mobiDF['start_polygon_id']==admRegID]['end_polygon_id']
            #indices = np.where( np.in1d( tReg, list(O_idD) ) )[0] #NOT SORTED!!
            #BAD sort
#             xe = np.outer([1,]*len(tReg), O_idD)
#             ye = np.outer(tReg, [1,]*len(O_idD))
#             junk, indices = np.where(np.equal(xe, ye))
            tReg=np.array(tReg)
            O_idD=np.array(list(O_idD))            
            
            index = np.argsort(tReg)
            sorted_x = tReg[index]
            sorted_index = np.searchsorted(sorted_x, O_idD)
            yindex = np.take(index, sorted_index, mode="clip")
#             mask = tReg[yindex] != O_idD
#             result = np.ma.array(yindex, mask=mask)
            
            O_flowD=mobiDF[mobiDF['start_polygon_id']==admRegID]['n_crisis']
#             if mobIdx==45: print("Find negative mobility at {} add {}".format(mobility[45,46], list(O_flowD)))
            mobility[mobIdx,yindex]=list(O_flowD) #np.mean(mobility[0,:]); np.max(mobility[0,:]); #np.std(mobility[0,:]);
        
        negMob=np.where(mobility.toarray()<0)
        io.mmwrite(mobMatrixFile.replace("csv", "mtx"), mobility)
        
        fig = plt.figure(figsize=(11.0, 11.0));ax = fig.add_subplot(111);
        ax.spy(mobility.toarray(), markersize=1); ax.set_ylabel("Origin"); ax.set_xlabel("Destination")        
        _,mobDate=os.path.split(mobMatrixFile); fig.suptitle("AdminRegions facebook mobility Matrix {}".format(mobDate.replace("_MXByStartPt.csv","")));
        fig.savefig(mobMatrixFile.replace("csv", "png").replace("mobMatrices", "mobMatrices/plots"), bbox_inches='tight');
        
        cmap=ut.fixInitialValueColorMap()
        fig2 = plt.figure(figsize=(11.0, 11.0));ax2 = fig2.add_subplot(111);
        pos2=ax2.imshow(mobility.toarray(), aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50] 
        fig2.colorbar(pos2, ax=ax2) ;ax2.set_ylabel("Origin"); ax2.set_xlabel("Destination")
        #'Ecatepec de Morelos'->'Iztapalapa' mobility[714,706];tGeoLocName[714];tGeoLocName[706];mobility[682,682];

def getMetroByDistance(tGeoLocInv,ptMTY):
    tree = spatial.KDTree(tGeoLocInv) #KDTree(
    nearest_dist, nearest_idx = tree.query(ptMTY, k=21) #.query_radius(points, r=1.5)     
    return nearest_idx

def getMetroByMobility(muniID,dayRange,secondOrder=False):
#     TODO: Add filter per 100k population
    
    mobToMuniFrom=[]; mobToMuniFromSet=set([])
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo))
        mobility=io.mmread(mobMatrixFile.replace("csv", "mtx") ).tocsr()
        mobToMuni=mobility[:, muniID]
        mobToMuniFrom.append( mobToMuni.nonzero()[0] )
        #TODO: Sort by mobility
        mobToMuniFromSet=mobToMuniFromSet.union( set(mobToMuni.nonzero()[0].tolist()) )
        
        
#         mobMetroArea=lil_matrix( ( len(metroIdx), len(metroIdx) ), dtype=int64 )
    
    munisIdx = np.sort( list(mobToMuniFromSet) ).tolist()
    
    print("Length 1st order muni {}".format(len(mobToMuniFromSet)))
    
    if secondOrder == "2nd":
        munisIdx=getMetro2ndOrderByMobility(munisIdx,dayRange)
    
    
    return munisIdx


def getMetro2ndOrderByMobility(munisIdx,dayRange):
    mobToMuniFrom=[]; mobToMuniFromSet=set([])
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo))
        mobility=io.mmread(mobMatrixFile.replace("csv", "mtx") ).tocsr()
        mobToMuni=mobility[:, munisIdx]
        mobToMuniFrom.append( mobToMuni.nonzero()[0] )
        mobToMuniFromSet=mobToMuniFromSet.union( set(mobToMuni.nonzero()[0].tolist()) ); 
    
    #TODO: Sort by mobility
    print("Length 2nd order muni {}".format(len(mobToMuniFromSet)))
    munisIdx = np.sort( list(mobToMuniFromSet) ).tolist()
    return munisIdx
#         mobMetroArea=lil_matrix( ( len(metroIdx), len(metroIdx) ), dtype=int64 )
    
    
    
    return np.sort( list(mobToMuniFromSet) ).tolist()
    


def getMobilityPerMetropolitanAreaMatrix(dayRange): #, normalize=False
    maxMobiFile=allMobi+"mobMatrices/metro/{}/plots/raw/maxPerDay.pkl".format(MetroArea)
    if os.path.exists(maxMobiFile) :
        return 
#         with open(maxMobiFile, 'rb') as extentFilePkl: #save selected hypothesis
#             mobMaxPerDay=pickle.load(extentFilePkl)
#         maxDefList=[]; maxDefOffDiagList=[]
#         for mobMax in mobMaxPerDay:
#             maxDefList.append(mobMax.max);
#             maxDefOffDiagList.append(mobMax.maxOffDiag)
#         maxDef=np.max(maxDefList);maxDefOffDiag=np.max(maxDefOffDiagList);
#     elif os.path.exists(maxMobiFile) and not normalize: return
#     else: maxDef=None;maxDefOffDiag=None
    if os.path.exists(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo)):
        with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'rb') as matchTreeFile:
            tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay = pickle.load(matchTreeFile)    
    tGeoLocInv=np.array(tGeoLoc)#TODO: the latitude and longitude coordinates are in the wrong order
    tGeoLocInv[:,[0, 1]] = tGeoLocInv[:,[1, 0]]; tReg=np.array(tReg); tGeoLocName=np.array(tGeoLocName)
    
    ptMTY=[-100.31109249700000419, 25.64490731320000094]#LINESTRING (-100.283203125 25.562238774210538) ptTeran=[-99.41303383000000338, 25.27589694790000152] #LINESTRING (-99.629296875 25.330469955007835
    metroIdx=getMetroByDistance(tGeoLocInv,ptMTY)
    if metroType == "" or metroType == "2nd":
        print ( "{} Metro Area by mobility".format( tGeoLocName[metroIdx[0]] ) )
        metroIdx=getMetroByMobility(metroIdx[0],dayRange, secondOrder=metroType)
    
    namesMetroArea=tGeoLocName[list(metroIdx)]
    
    print("Admin Regions within metropolitan area {}".format(tGeoLocName[list(metroIdx)]) )
    with open(covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        casosCentroidsDF = pd.read_csv( covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo)) )
    
    df = pd.DataFrame()
    for metroID in metroIdx:
        metroAdminReg = casosCentroidsDF[casosCentroidsDF['PolygonID']==tReg[metroID] ]
        df=df.append(metroAdminReg, ignore_index=True, sort=False)

    df.to_csv(covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}.".format(joinByMobGeo,MetroArea)),index=False)
    print("MetroArea {}\n".format( covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}.".format(joinByMobGeo,MetroArea)) ) )
    caSts.computeCumulativeCases(covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}.".format(joinByMobGeo,MetroArea)))
    
    mobMaxPerDay=[]; #totalReg=[];totalGeoLoc=[]; totalGeoLocName=[];#     totalRegSet=set([]); totalLargerChangeLoc=[] 
      
    #TODO: def extractMobilityFromMunicpalities():
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo))
        mobility=io.mmread(mobMatrixFile.replace("csv", "mtx") ).tocsr()
        
        mobMetroArea=lil_matrix( ( len(metroIdx), len(metroIdx) ), dtype=int64 )
        for idxMetroR, idxR in zip(xrange(len(metroIdx)), metroIdx):
            for idxMetroC, idxC in zip(xrange(len(metroIdx)), metroIdx):
                mobMetroArea[idxMetroR, idxMetroC]=mobility[idxR, idxC] #mobility[metroIdx[4], metroIdx[4]]

        mobMatrixFile="{}mobMatrices/metro/{}/2020-04-AAAA.csv".format(allMobi,MetroArea).replace('AAAA',"{:02d}_MX{}{}".format(day,joinByMobGeo,MetroArea))
        io.mmwrite(mobMatrixFile.replace("csv", "mtx"), mobMetroArea)        
        
        fx=len(metroIdx)/1.5; fy= len(metroIdx)/2.8
        if fx<12.0:fx=12
        if fy<5.0:fy=5
        fig = plt.figure( figsize=(fx,fy) ); ax = fig.add_subplot(121); mobMetroArea=mobMetroArea.toarray()
        mobMU.plotMobmatrix(mobMetroArea,namesMetroArea,ax, fig)#,limDef=maxDef        
        maxMob = np.max(mobMetroArea); muni = np.argmax(mobMetroArea)
        muniOrg=muni/len(namesMetroArea); muniDest=muni%len(namesMetroArea)
        maxTraj="{}->{}_{}->{}".format(namesMetroArea[muniOrg], namesMetroArea[muniDest], metroIdx[muniOrg], metroIdx[muniDest])
        
        _,mobDate=os.path.split(mobMatrixFile); dateMetro=mobDate.replace("_MXByStartPt{}.csv".format(MetroArea)," "+MetroArea)               
        
#         mask = np.ones(mobMetroArea.shape, dtype=bool); np.fill_diagonal(mask, 0); 
#         maxOffDiag = mobMetroArea[mask].max(); maxOffDiagNumi = mobMetroArea[mask].argmax();        
        np.fill_diagonal(mobMetroArea, 0); maxOffDiag = mobMetroArea.max(); muniOffDiag = mobMetroArea.argmax()
        muniOrg=muniOffDiag/len(namesMetroArea); muniDest=muniOffDiag%len(namesMetroArea); #mobMetroArea[muniOrg,muniDest]
        maxTrajOffDiag="{}->{}_{}->{}".format(namesMetroArea[muniOrg], namesMetroArea[muniDest], metroIdx[muniOrg], metroIdx[muniDest])         
        ax2 = fig.add_subplot(122); mobMU.plotMobmatrix(mobMetroArea,namesMetroArea,ax2, fig, verbLeg=False) #, limDef=maxDefOffDiag

        mobMaxPerDay.append( mobMU.mobilityMatrixMetric( dateMetro, maxMob, unicode(maxTraj,'utf-8'), maxOffDiag, unicode(maxTrajOffDiag,'utf-8') ) )    
              
        fig.suptitle( unicode("AdminRegions facebook mobility Matrix {} OffDiag max {} traj {}".format( dateMetro, maxOffDiag, maxTrajOffDiag), 'utf-8') );
        fig.savefig(mobMatrixFile.replace("csv", "png").replace("metro/"+MetroArea, "metro/"+MetroArea+"/plots/raw"), bbox_inches='tight')

    with open(maxMobiFile, 'wb') as extentFilePkl: #save selected hypothesis
        pickle.dump(mobMaxPerDay, extentFilePkl)
        #Test #namesMetroArea[5];namesMetroArea[12];mobMetroArea[5,12]
#         fig2 = plt.figure(figsize=(11.0, 11.0));ax2 = fig2.add_subplot(111);
#         pos2=ax2.imshow(mobility.toarray(), aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50] 
#         fig2.colorbar(pos2, ax=ax2) ;mobility[682,682]

    
def main():
    dayRange=[2,23]
    computeMobilityMatrix(dayRange)
    getMobilityPerMetropolitanAreaMatrix(dayRange) #, normalize=False
#     mobilityWithCasesPer100kMetro(dayRange)
    
mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos= "/data/covid/casos/12_05/Casos_Diarios_Municipio_Confirmados_20200512.csv" #"/data/covid/casos/12_05/Casos_Diarios_Estado_Nacional_Confirmados_20200512.csv" #/data/covid/casos/27_04
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
baselinePerFile=[]; getCountry='MX'#'GT'#
joinByMobGeo="ByStartPt";  MetroArea="MTY"; metroType=""#2nd";
MetroArea+=metroType      #""    

if __name__ == "__main__":
    main()

    