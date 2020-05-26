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
import utils as ut

import joinMunicipalitiesInAdminRegions as joinMuni

def metroAreaAdminRegions():            
    with open(centroidPath, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        centroidDF = pd.read_csv( centroidPath )
    
    with open(metroAreasCSV, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        metroAreasDF = pd.read_csv( metroAreasCSV )
    munisMetroL=metroAreasDF[MetroArea]
        
    
    munisT=centroidDF["NOM_MUN"]; nomMunis=[]; cveMunis=centroidDF["CVE_MUN"]; centMunis=centroidDF[["X","Y"]]
    for nomMuni in munisT:
        nomMunis.append(unicodedata.normalize('NFC', nomMuni.decode('utf8')))
    
    munisMetro=[]
    for muni in munisMetroL:
        muni=unicodedata.normalize('NFC', muni.decode('utf8'))
#         matched=np.find(muni==nomMunis)  #TODO: more efficient     
#         if len(matched)==0:
#         matching = [s for s in nomMunis if muni in s]
#         matched = ut.getIndexPositions(nomMunis, muni)      
        matched=[]; matchedName=[]
        for id, nomMuni in zip( xrange( len(nomMunis) ), nomMunis ):
            if abs(len(muni)-len(nomMuni))<4 and ut.numberOfMatchedLetters(nomMuni,muni)>len(muni)-4:
                matched.append(id); matchedName.append(nomMuni)
  
        
        if len(matched)==1:
            munisMetro.append(ut.municipality(muni, centMunis.values[matched[0]], cveMunis[matched[0]]))
        elif len(matched)>1:
            print ("matched names{}".format(matchedName))
#             TODO: compare matched coords or CVES  with MTY
        else:
            print ("matched {}".format(matched))
            
            
            
        
        
        
    dropIdxsB=[]
    print(casosDF.shape)
    casosDF.insert(0,'X',0.0); casosDF.insert(1,'Y',0.0)
    print(casosDF.shape)
    for idx, casosMun in casosDF.iterrows():
        centroidMun=centroidDF[casosMun["cve_ent"]==centroidDF['CVE_MUN']]        
        encoded1 = unicodedata.normalize('NFC', casosMun["nombre"].decode('utf8'))
        encoded2 = unicodedata.normalize('NFC', centroidMun["NOM_MUN"].values[0].decode('utf8'))
        
        if np.sum(casosMun["cve_ent"]==centroidDF['CVE_MUN'])==1 and ut.numberOfMatchedLetters(encoded1,encoded2)<3:
            casosDF.at[idx,'X']=centroidMun['X'].values[0]
            casosDF.at[idx,'Y']=centroidMun['Y'].values[0]
#             dropIdxsB.append(centroidMun.idx)#(casosMun["cve_ent"])
        else: 
            print("Not the same name casos {} centroid {}".format(casosMun["nombre"], encoded2))  
              
    casosDF.to_csv(covCasos.replace('.',"Centroids."),index=False)
    print(covCasos.replace( '.',"Centroids." ) )
#     dfB.drop(dropIdxsB, inplace = True)
#     return dfMerged


def adminRegionsByMunicipalities():
    muniCasesPts=np.array([list(casosCentroidsDF['X'].values),list(casosCentroidsDF['Y'].values)]); muniCasesPts=muniCasesPts.transpose()
    new_cmap = ut.rand_cmap(50000, type='bright', first_color_black=True, last_color_black=False, verbose=False)
    tGeoLocInv=np.array(tGeoLoc)#TODO: the latitude and longitude coordinates are in the wrong order
    tGeoLocInv[:,[0, 1]] = tGeoLocInv[:,[1, 0]]
    vorInv = Voronoi(tGeoLocInv)
    voronoi_plot_2d(vorInv,show_vertices=False,point_size=0.9)
    plt.plot(muniCasesPts[:,0], muniCasesPts[:,1], 'rx',ms=0.9); plt.show()
    
    plt.plot(muniCasesPts[144,0], muniCasesPts[144,1], 'k^',ms=5.9); print("Muni {}".format(casosCentroidsDF['nombre'].values[144]) )#PalenqueMuni
    plt.plot(muniCasesPts[129,0], muniCasesPts[129,1], 'c^',ms=5.9); print("Muni {}".format(casosCentroidsDF['nombre'].values[129]) )#PalenqueMun
    
    plt.plot(tGeoLocInv[20,0], tGeoLocInv[20,1], 'ks',ms=2.9); print("AdminReg {}".format(tGeoLocName[20]) )
    plt.plot(tGeoLocInv[25,0], tGeoLocInv[25,1], 'cs',ms=2.9); print("AdminReg {}".format(tGeoLocName[25]) )
    
    MobilityNodesVoronoiKdtree = cKDTree(tGeoLocInv)
    # sanAndresChol = [-98.2897525067248 ,19.0241411772732]; test_point_dist, sanPedroChol = MobilityNodesVoronoiKdtree.query(sanAndresChol); 
    # tGeoLocName[sanPedroChol]
    palenqueDist, palenqueAdminRegIdx = MobilityNodesVoronoiKdtree.query(muniCasesPts[144]);tGeoLocName[palenqueAdminRegIdx]
    
    test_point_dist, test_point_regions = MobilityNodesVoronoiKdtree.query(muniCasesPts)
    plt.scatter(muniCasesPts[:,0], muniCasesPts[:,1], c=test_point_regions,cmap=new_cmap, s=5.5)#'Set3'
    
    casosCentroidsDF.insert(2,'PolygonID',-1);casosCentroidsDF.insert(3,'PolygonName','AAAA');
    casosCentroidsDF.insert(4,'PolygonPositionX','-1.0'); casosCentroidsDF.insert(5,'PolygonPositionY','-1.0')
    
    muniPolyIDs=[]; muniPolyAdminNames=[]; muniPolyPositionsX=[];muniPolyPositionsY=[];
    for testPtRegion in test_point_regions:
        muniPolyIDs.append(tReg[testPtRegion]); muniPolyAdminNames.append(tGeoLocName[testPtRegion]);
        muniPolyPositionsX.append(str(tGeoLocInv[testPtRegion,0]));muniPolyPositionsY.append(str(tGeoLocInv[testPtRegion,1]))
    
    casosCentroidsDF['PolygonID']=muniPolyIDs; casosCentroidsDF['PolygonName']=muniPolyAdminNames; 
    casosCentroidsDF['PolygonPositionX']=muniPolyPositionsX; casosCentroidsDF['PolygonPositionY']=muniPolyPositionsY
    casosCentroidsDF.to_csv(covCasos.replace('.',"CentroidsWithAdminRegFB."),index=False)
    keepIds=['PolygonID','PolygonName','PolygonPositionX','PolygonPositionY','cve_ent','nombre']
    sumIds= list(casosCentroidsDF)
    for kId in keepIds+['X','Y']:  sumIds.remove(kId)
    
    df = pd.DataFrame(columns = keepIds+sumIds)
    
    casosCentroidsDF['cve_ent']=casosCentroidsDF['cve_ent'].transform(lambda x: str(x))
    municipiosInsideReg=[]; emptyAdminRegions=[]
    for adminRegID, adminRegName, idx, adminGeoLoc in zip(tReg, tGeoLocName, xrange(len(tGeoLocName)), tGeoLocInv):
        casosSameAdminRegionDF = casosCentroidsDF[casosCentroidsDF['PolygonID']==adminRegID]
        municipiosInsideReg.append([adminRegName, len(casosSameAdminRegionDF)-1 ])
        sumAdminReg=pd.concat( [ casosSameAdminRegionDF[['cve_ent','nombre']].agg(lambda x: ', '.join(x)).T, casosSameAdminRegionDF[sumIds].sum().T ] )         
    #     casosSameAdminRegionDF[['PolygonID','PolygonName','PolygonPosition']].head(1)    
    #     sumAdminReg=pd.concat( [casosSameAdminRegionDF[['PolygonID','PolygonName','PolygonPosition']].head(1), casosSameAdminRegionDF[['cve_ent','nombre']].agg(lambda x: ', '.join(x)).T, casosSameAdminRegionDF[sumIds].sum().T ] ) 
    #     casosSameAdminRegionDF[['nombre']].agg(lambda x: ', '.join(x));    casosSameAdminRegionDF[['cve_ent']].agg(lambda x: ', '.join(x))    
    #     casosSameAdminRegionDF[['cve_ent','nombre']].agg(lambda x: ', '.join(x));    df.append(, ignore_index=True)
    #     df=df.append(data2k, ignore_index=True, sort=False)
        if len(casosSameAdminRegionDF[keepIds[0]].head(1).values)>0:
            df=df.append(sumAdminReg, ignore_index=True, sort=False)
            for keID in keepIds[0:4]: df.at[idx-len(emptyAdminRegions),keID]=casosSameAdminRegionDF[keID].head(1).values[0]
        else:
            emptyAdminRegions.append(adminRegName); #print("Missing elements {} {}".format(adminRegID, adminRegName)); 
            plt.plot(adminGeoLoc[0], adminGeoLoc[1], 'g*',ms=14); 
                
    df.to_csv(covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo)),index=False)
    print("Missing elements {} {}".format(emptyAdminRegions, len(emptyAdminRegions) ) )


##################################################################################################################################################################################
def main():
    dayRange=[2,23] #TODO: Separate from 23/04 where only state info is given
    if os.path.exists(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo)):
        with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'rb') as matchTreeFile:
            tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay = pickle.load(matchTreeFile)
    else:
        tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay=joinMuni.mergeMobilityCoord(dayRange)    
    
    ##################################################################################################################################################################################
    if  not os.path.exists( metroAreasCSV.replace('.csv',"AdminReg.pkl") ):
    #     with open(covCasos, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
    #         casosDF = pd.read_csv( covCasos )
    #     muniName= casosDF.nombre.unique();muniCVE= casosDF.cve_ent.unique()
    #     print("Total municipios number with cases by CVE {} and by Name {}".format(muniCVE.size, muniName.size) )
        metroAreaAdminRegions()    
    with open( metroAreasCSV.replace('.csv',"AdminReg.pkl") ) as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
         metroAreasAdminReg = pd.read_csv( metroAreasCSV.replace('.csv',"AdminReg.pkl") )
    ##################################################################################################################################################################################
    
#     adminRegionsByMunicipalities()


#TODO: factorize paths and files for all scripts


mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos="/data/covid/casos/12_05/Casos_Diarios_Municipio_Confirmados_20200512.csv" #/data/covid/casos/27_04 # 01_05/Casos_Diarios_Estado_Nacional_Confirmados 

centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
metroAreasCSV="/data/covid/maps/metroAreas.csv"
baselinePerFile=[]; getCountry='MX'; MetroArea="MTY"; metroType=""#2nd";#'GT'#

joinByMobGeo="ByStartPt"#""

    

if __name__ == "__main__":
    main()


