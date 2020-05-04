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

mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos="/data/covid/casos/01_05/Casos_Diarios_Estado_Nacional_Confirmados.csv" #/data/covid/casos/27_04
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
#Join databases per day
# title="Municipalities with displacement larger 30 km per day"
baselinePerFile=[]; getCountry='MX'#'GT'#
joinByMobGeo="ByStartPt"#""

def numberOfNonMatchLetters(a,b):
    u=zip(a,b)
    d=dict(u)    
    x=0
    for i,j in d.items():
        if i==j:
            x=+1
    return x

def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """

    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in xrange(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in xrange(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')

    return random_colormap

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

def mergeMobilityCoord(dayRange):
    adminRegPerDay=[]; totalReg=[];totalGeoLoc=[]; totalGeoLocName=[];
    totalRegSet=set([]); totalLargerChangeLoc=[]       
    for day in range(dayRange[0],dayRange[1]): #
        with open(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
            mobiDF = pd.read_csv( mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)) )
            #     with open(mobiTemp.replace('AAAA',"{:02d} 0800".format(day)), 'r') as f:
            #         df08 = pd.read_csv( mobiTemp.replace('AAAA',"{:02d} 0800".format(day)) )
            #     with open(mobiTemp.replace('AAAA',"{:02d} 1600".format(day)), 'r') as f:
            #         df16 = pd.read_csv( mobiTemp.replace('AAAA',"{:02d} 1600".format(day)) )
            # admRegNameStart=mobiDF.start_polygon_name.unique(); admRegNameEnd=mobiDF.end_polygon_name.unique();admRegNameStart.size; admRegNameEnd.size
        admRegIdStart=mobiDF.start_polygon_id.unique(); admRegIdEnd=mobiDF.end_polygon_id.unique();
        admRegSetStart=set(admRegIdStart);admRegSetEnd=set(admRegIdEnd)        
        #split geometry
        test = mobiDF["geometry"].str.replace("LINESTRING \(", "", n=1)
        test=test.str.replace("\)", "", n=1)
        test = test.str.split(",", n=1, expand=True)            
        #TODO: geometry with start end lat lons
        testStart = test[0].str.split(" ", n=1, expand=True);    testEnd = test[1].str.split(" ", n=2, expand=True)#testEnd=test.str.replace(",", "", n=1)
        mobiDF["geoStartLat"]= testStart[1].astype('float64');    mobiDF["geoStartLon"]= testStart[0].astype('float64')#convert_objects(convert_numeric=True) #
        mobiDF["geoEndLat"]= testEnd[2].astype('float64');    mobiDF["geoEndLon"]= testEnd[1].astype('float64')
        geoLoc=[]; geoLocName=[]; largerChangeLoc=[]
        
        test = pd.DataFrame(columns = ['start_lon', 'start_lat','end_lon', 'end_lat'])
        test['start_lon']=mobiDF['start_lon'].transform(lambda x: "LINESTRING ("+str(x))
        test['start_lat']=mobiDF['start_lat'].transform(lambda x: " "+str(x)+", ")
        test['end_lon']=mobiDF['end_lon'].transform(lambda x: str(x)+" ")
        test['end_lat']=mobiDF['end_lat'].transform(lambda x: str(x)+")")            
        mobiDF["geometryStartEnd"]= test[['start_lon', 'start_lat','end_lon', 'end_lat']].agg(''.join, axis=1)
#         df['period'] = df[['Year', 'quarter', ...]].agg('-'.join, axis=1)#         mobiDF[['start_lon', 'start_lat','end_lon', 'end_lat']].agg( lambda x: ', '.join(str(x)), axis=1 ) 
        
        for idStart in admRegIdStart: #TODO: Only look for non added, or compare the diff coordinates
            idName=mobiDF[mobiDF['start_polygon_id']==idStart].head(1)['start_polygon_name'].values[0]
            idLat=pd.concat( [ mobiDF[mobiDF['start_polygon_id']==idStart]['start_lat'], mobiDF[mobiDF['end_polygon_id']==idStart]['end_lat'] ], ignore_index=True, sort=False )
            idLon=pd.concat( [ mobiDF[mobiDF['start_polygon_id']==idStart]['start_lon'], mobiDF[mobiDF['end_polygon_id']==idStart]['end_lon'] ], ignore_index=True, sort=False )
            if np.abs(idLat.max()- idLat.min())<0.000001 and np.abs(idLon.mean()-idLon.max())<0.000001:
                geoLat=pd.concat( [ mobiDF[mobiDF['start_polygon_id']==idStart]['geoStartLat'], mobiDF[mobiDF['end_polygon_id']==idStart]['geoEndLat'] ], ignore_index=True, sort=False)
                geoLon=pd.concat( [ mobiDF[mobiDF['start_polygon_id']==idStart]['geoStartLon'], mobiDF[mobiDF['end_polygon_id']==idStart]['geoEndLon'] ], ignore_index=True, sort=False)
    #         mobiDF[mobiDF['start_polygon_id']==idStart]['start_lat']
    #         startLon=mobiDF[mobiDF['start_polygon_id']==idStart]['start_lon']
    #         endLat=mobiDF[mobiDF['end_polygon_id']==idStart]['end_lat']
    #         endLon=mobiDF[mobiDF['end_polygon_id']==idStart]['end_lon']
                if np.abs(geoLat.min()-geoLat.max())>0.3 or np.abs(geoLon.min()-geoLon.max())>0.3 or geoLat.std()>0.1 or geoLon.std()>0.1: #TODO: print and check max diff in hubs map 
                    print("{} GEOMETRY lat [{}, {}] u={} lon  [{}, {}] u={}".format( idName, geoLat.min(), geoLat.max(), geoLat.mean(), geoLon.min(), geoLon.max(), geoLon.mean() ) )
                    print("{} GEOMETRY lat diff={}, s={} lon diff={}, s{}".format( idName, geoLat.min()-geoLat.max(), geoLat.std(), geoLon.min()-geoLon.max(), geoLon.std() ) )
                    largerChangeLoc.append([idStart, idName,geoLat.min(), geoLat.max(), geoLat.mean()])
                
                geoLocName.append( idName )
                if joinByMobGeo == "":  geoLoc.append([geoLat.mean(), geoLon.mean()]);  #TODO: geometry back to mean geoLoc
    #                 mobiDF.at(mobiDF['start_polygon_id']==idStart, "geoStartLat") = geoLat.mean(); mobiDF.at(mobiDF['end_polygon_id']==idStart, "geoEndLat") = geoLat.mean()
    #                 mobiDF.at(mobiDF['start_polygon_id']==idStart, "geoStartLon") = geoLon.mean(); mobiDF.at(mobiDF['end_polygon_id']==idStart, "geoEndLon") = geoLon.mean()
                else: geoLoc.append([idLat.mean(), idLon.mean()]);
                    
                mobiDF[mobiDF['start_polygon_id']==idStart] = mobiDF[mobiDF['start_polygon_id']==idStart].assign( geoStartLat=geoLat.mean() ); 
                mobiDF[mobiDF['end_polygon_id']==idStart]=mobiDF[mobiDF['end_polygon_id']==idStart].assign( geoEndLat=geoLat.mean() );  
                mobiDF[mobiDF['start_polygon_id']==idStart]=mobiDF[mobiDF['start_polygon_id']==idStart].assign( geoStartLon=geoLon.mean() ); 
                mobiDF[mobiDF['end_polygon_id']==idStart]=mobiDF[mobiDF['end_polygon_id']==idStart].assign( geoEndLon=geoLon.mean() );  
    #                 geoLat=pd.concat( [ mobiDF[mobiDF['start_polygon_id']==idStart]['geoStartLat'], mobiDF[mobiDF['end_polygon_id']==idStart]['geoEndLat'] ], ignore_index=True, sort=False)
    #                 geoLon=pd.concat( [ mobiDF[mobiDF['start_polygon_id']==idStart]['geoStartLon'], mobiDF[mobiDF['end_polygon_id']==idStart]['geoEndLon'] ], ignore_index=True, sort=False)
    #                 print("{} Difference GEOMETRY lat [{}, {}] u={} lon  [{}, {}] u={}".format( idName, geoLat.min(), geoLat.max(), geoLat.mean(), geoLon.min(), geoLon.max(), geoLon.mean() ) )
            else:
                print("{} Difference  ADMIN REGION!!! lat [{}, {}] u={}  [{}, {}] u={}".format( idName, idLat.min(), idLat.max(), idLat.mean(), idLon.min(), idLon.max(), idLon.mean() ) )        #TODO: check which change it should not!!       
        
        if admRegIdStart.size == admRegIdEnd.size and len( admRegSetEnd.difference(admRegSetStart) ) == 0:
            adminRegPerDay.append(admRegIdStart.size);totalLargerChangeLoc.append(largerChangeLoc)
            if len( totalRegSet.difference(admRegSetStart) ) != 0 or len(admRegSetStart.difference(totalReg)) :  #TODO: verify diff of sets should be totalReg.                       
                for idx, idStart in enumerate(list(admRegIdStart)):
                    if idStart not in totalReg:
                        totalReg.append(idStart)
                        totalGeoLoc.append(geoLoc[idx]);
                        totalGeoLocName.append(geoLocName[idx]);
                        if day>dayRange[0]:
                            print("{} NEW ADMIN REGION {} [{}]".format( geoLocName[idx], idStart, geoLoc[idx] ) )            
    #             totalReg=list(OrderedDict.fromkeys(totalReg+list(admRegIdStart)))
    #             totalReg.append(admRegIdStart)#union sets keep order
    #             totalReg=totalReg+list(admRegIdStart); totalRegB=list(totalRegSet.union(admRegSetStart) )
    #             totalRegSet=totalRegSet.union(admRegSetStart); totalRegSet=totalRegSet.union(admRegSetEnd); #print("totalReg size end {}".format(len(totalReg)))#print("totalReg size start {}".format(len(totalReg)))            
        else: 
            print("Different Id startEnd size {}!!!!".format( len( admRegSetEnd.difference(admRegSetStart) ) ) )
        
        mobiDF.to_csv("{}geoStart/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo)),index=False)
        
    print("Merge mobility day {}".format(day) )
    with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'wb') as matchTreeFile:
        pickle.dump([totalReg, totalGeoLoc,totalGeoLocName, totalLargerChangeLoc, adminRegPerDay], matchTreeFile)      
              
    return totalReg, totalGeoLoc,totalGeoLocName, totalLargerChangeLoc, adminRegPerDay

dayRange=[2,23] #TODO: Separate from 23/04 where only state info is given

if os.path.exists(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo)):
    with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'rb') as matchTreeFile:
        tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay = pickle.load(matchTreeFile)
else:
    tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay=mergeMobilityCoord(dayRange)
    
# # Join per states
# tRegStates = tReg[-32:]; tGeoLocStates = tGeoLoc[-32:]; tGeoLocNameStates = tGeoLocName[-32:]
# tLargerChangeLocStates = tLargerChangeLoc[-3:]; adminRegPerDayStates =adminRegPerDay[-3:]
# with open(allMobi+"mobilityCoordMerged{}PerStates.pkl".format(joinByMobGeo), 'wb') as matchTreeFile:
#     pickle.dump([tRegStates, tGeoLocStates,tGeoLocNameStates, tLargerChangeLocStates, adminRegPerDayStates], matchTreeFile)  
# # Join per admin regions
# tRegAdminReg = tReg[:len(tGeoLoc)-32]; tGeoLocAdminReg = tGeoLoc[:len(tGeoLoc)-32]; tGeoLocNameAdminReg = tGeoLocName[:len(tGeoLoc)-32]
# tLargerChangeLocAdminReg = tLargerChangeLoc[:len(adminRegPerDay)-3]; adminRegGoodPerDay =adminRegPerDay[:len(adminRegPerDay)-3]
# with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'wb') as matchTreeFile:
#     pickle.dump([tRegAdminReg, tGeoLocAdminReg,tGeoLocNameAdminReg, tLargerChangeLocAdminReg, adminRegGoodPerDay], matchTreeFile)  


tRegSet=set(tReg);len(tRegSet);#tGeoLocSet=set(tGeoLoc); len(tGeoLocSet)

##################################################################################################################################################################################
if  not os.path.exists( covCasos.replace('.',"Centroids.") ):
    with open(covCasos, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        casosDF = pd.read_csv( covCasos )
    muniName= casosDF.nombre.unique();muniCVE= casosDF.cve_ent.unique()
    print("Total municipios number with cases by CVE {} and by Name {}".format(muniCVE.size, muniName.size) )
    addCentroidToMunicipalCases(casosDF)    
with open(covCasos.replace('.',"Centroids."), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
     casosCentroidsDF = pd.read_csv( covCasos.replace('.',"Centroids.") )
##################################################################################################################################################################################

muniCasesPts=np.array([list(casosCentroidsDF['X'].values),list(casosCentroidsDF['Y'].values)]); muniCasesPts=muniCasesPts.transpose()
new_cmap = rand_cmap(50000, type='bright', first_color_black=True, last_color_black=False, verbose=False)
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

casosCentroidsDF.insert(2,'PolygonID',-1);casosCentroidsDF.insert(3,'PolygonName','AAAA');casosCentroidsDF.insert(4,'PolygonPosition','-1.0, -1.0')

muniPolyIDs=[]; muniPolyAdminNames=[]; muniPolyPositions=[];
for testPtRegion in test_point_regions:
    muniPolyIDs.append(tReg[testPtRegion]); muniPolyAdminNames.append(tGeoLocName[testPtRegion]);muniPolyPositions.append(str(tGeoLocInv[testPtRegion]))

casosCentroidsDF['PolygonID']=muniPolyIDs; casosCentroidsDF['PolygonName']=muniPolyAdminNames;  casosCentroidsDF['PolygonPosition']=muniPolyPositions
casosCentroidsDF.to_csv(covCasos.replace('.',"CentroidsWithAdminRegFB."),index=False)
keepIds=['PolygonID','PolygonName','PolygonPosition','cve_ent','nombre']
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
        for keID in keepIds[0:3]: df.at[idx-len(emptyAdminRegions),keID]=casosSameAdminRegionDF[keID].head(1).values[0]
    else:
        emptyAdminRegions.append(adminRegName); #print("Missing elements {} {}".format(adminRegID, adminRegName)); 
        plt.plot(adminGeoLoc[0], adminGeoLoc[1], 'g*',ms=14); 
            
df.to_csv(covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo)),index=False)
print("Missing elements {} {}".format(emptyAdminRegions, len(emptyAdminRegions) ) )

# casosDFmx= casosDF[getCountry== casosDF['country']];df08mx=df08[getCountry==df08['country']];df16mx=df16[getCountry==df16['country']]
# # computeFlow( casosDFmx);computeFlow(df08mx); computeFlow(df16mx);# 
# #  casosDFmx['start_polygon_name']['end_polygon_name']  casosDFmx.head(1)['n_baseline']
# casosDFmxMerged=mergeMobilities( casosDFmx, df08mx);print( casosDFmxMerged.shape)
# casosDFmxMerged=mergeMobilities( casosDFmxMerged, df16mx);print( casosDFmxMerged.shape)# 
# casosDFmxMerged.to_csv(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)),index=False)
# print(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)))
#  casosDFmx= casosDFmx[1:10];df08mx=df08mx[1:10];df16mx=df16mx[1:10]
# areSame =  casosDFmx['start_polygon_name']==df08mx['start_polygon_name']
# for muni in areSame:
#     if not muni: print("ERROR {}".format(muni) ); break;#
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
