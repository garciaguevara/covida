import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial import Voronoi, voronoi_plot_2d
import pickle
import unicodedata
from matplotlib.colors import LinearSegmentedColormap
import colorsys
import numpy as np

def computeCumulativeCases():
    with open(casesPerAdmReg, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        df = pd.read_csv( casesPerAdmReg )
    
    df.loc[:, '07-01-2020':'12-05-2020']=df.loc[:, '07-01-2020':'12-05-2020'].cumsum(axis=1)
    
    df.to_csv(casesPerAdmReg.replace('.csv', 'Cumulative.csv'),index=False)
    print("computeCumulativeCases {}".format(casesPerAdmReg.replace('.csv', 'Cumulative.csv') ) )


def addCasesToMobility():
    pathCasesAdminRegCum = casesPerAdmReg.replace(".", "Cumulative.")
    with open(pathCasesAdminRegCum, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        casesDF = pd.read_csv( pathCasesAdminRegCum )

    dayRange=[2,23]
    for day in range(dayRange[0],dayRange[1]):
        #day =15
        pathToMob="{}/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX".format(day))
        with open(pathToMob, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
            mobPerDayDF = pd.read_csv( pathToMob )
        
        date="{:02d}-04-2020".format(day)#         casesPerDay=casesDF[date]         
        mobPerDayDF.insert(mobPerDayDF.shape[1],'CumCasesStart',-1);
        mobPerDayDF.insert(mobPerDayDF.shape[1],'PoblacionStart',-1);
        admRegIdStart=mobPerDayDF.start_polygon_id.unique()
        for admRegID in admRegIdStart:
            O_idD=mobPerDayDF[mobPerDayDF['start_polygon_id']==admRegID]
            if len(casesDF[casesDF['PolygonID']==admRegID][date].get_values()) >0 :
                O_idD['CumCasesStart']=casesDF[casesDF['PolygonID']==admRegID][date].get_values()[0]
                O_idD['PoblacionStart']=casesDF[casesDF['PolygonID']==admRegID]["poblacion"].get_values()[0]           
                
                mobPerDayDF[mobPerDayDF['start_polygon_id']==admRegID]=O_idD                 
            else: print ("Start adminReg {} not in trajectories {}".format(admRegID, date) )
            

        mobPerDayDF.to_csv(pathToMob.replace("Day/","Day/wCases/").replace('.',"Cases."),index=False) 
        print("Add cases to mobility {}".format(pathToMob) )

mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos="/data/covid/casos/12_05/Casos_Diarios_Municipio_Confirmados_20200512.csv" #/data/covid/casos/27_04 # 01_05/Casos_Diarios_Estado_Nacional_Confirmados  #TODO: factorize paths and files for all scripts
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
#Join databases per day
# title="Municipalities with displacement larger 30 km per day"
baselinePerFile=[]; getCountry='MX'#'GT'#

joinByMobGeo="ByStartPt"#""
casesPerAdmReg=covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo))


# computeCumulativeCases()
addCasesToMobility()


