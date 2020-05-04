import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy.sparse import *
from scipy import io
from scipy import *
import pickle
import unicodedata
from matplotlib.colors import LinearSegmentedColormap
import colorsys
import numpy as np

mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos="/data/covid/casos/01_05/Casos_Diarios_Estado_Nacional_Confirmados.csv" #/data/covid/casos/27_04
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
baselinePerFile=[]; getCountry='MX'#'GT'#
joinByMobGeo="ByStartPt"#""

def computeMobilityMatrix(dayRange):    
    if os.path.exists(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo)):
        with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'rb') as matchTreeFile:
            tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay = pickle.load(matchTreeFile)    
    
#     adminRegPerDay=[]; totalReg=[];totalGeoLoc=[]; totalGeoLocName=[];
#     totalRegSet=set([]); totalLargerChangeLoc=[]       
    for day in range(dayRange[0],dayRange[1]): #
        with open(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
            mobiDF = pd.read_csv( mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)) )
        
        mobility=lil_matrix( ( len(tReg), len(tReg) ), dtype=int16 ) #csr_matrix
        
        admRegIdStart=mobiDF.start_polygon_id.unique(); admRegIdEnd=mobiDF.end_polygon_id.unique();
        admRegSetStart=set(admRegIdStart);admRegSetEnd=set(admRegIdEnd)        
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
        for admRegID, admRegName in zip(tReg, tGeoLocName): #TODO: Only look for non added, or compare the diff coordinates
            if len(mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values)>0:
                idName=mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values[0]
                if admRegName!=idName:
                    print("AdminRegions name {} diff {}".format(admRegName,idName) )
            else:
                 print("AdminRegions name not found in mobility data {} diff {}".format(admRegName,mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values) )
                 
            O_idD=mobiDF[mobiDF['start_polygon_id']==admRegID]['end_polygon_id']
            indices = np.where(np.in1d(tReg, list(O_idD)))[0]
            
            O_flowD=mobiDF[mobiDF['start_polygon_id']==admRegID]['n_crisis']
            mobility[0,indices]=list(O_flowD) #np.mean(mobility[0,:]); np.max(mobility[0,:]); #np.std(mobility[0,:]);
                
        mobMatrixFile="{}mobMatrices/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo))
        io.mmwrite(mobMatrixFile.replace("csv", "mtx"), mobility)



dayRange=[2,26]
computeMobilityMatrix(dayRange)
    
    
    
    
    