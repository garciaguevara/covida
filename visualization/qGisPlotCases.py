from qGisPlotMobData import *

##########################################################################################################################3
# pathToCasesCentroids = "/data/covid/casos/01_05/Casos_Diarios_Estado_Nacional_ConfirmadosCentroids.csv"
# vlayerCases=plotCases(pathToCasesCentroids) 
pathCasesAdminRegCum = "/data/covid/casos/01_05/Casos_Diarios_Estado_Nacional_ConfirmadosCentroidsPerAdminRegionsByStartPtCumulative.csv"
# vlayerCasesAdminReg=plotCases(pathCasesAdminReg, posIdx=['PolygonPositionX','PolygonPositionY'],nLetters=7) #TODO: copy visu style
lCasesAdminRegCum=plotCases(pathCasesAdminRegCum, posIdx=['PolygonPositionX','PolygonPositionY'],nLetters=7) #TODO: copy visu style
lCasesAdminRegCum.renderer().setClassAttribute("20-04-2020")#copy style before using
lCasesAdminRegCum.triggerRepaint()
qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/casos/01_05/{}.png'.format(casesIt))
# casesIt="TOTALES" #"20-04-2020"# vlayerCasesAdminReg.renderer().setClassAttribute(casesIt)


##########################################################################################################################3
# BaselineMax=['2020-04-08_0000', 5455.8000000000002, 10.0, 2091]# in series 3 per day
# flow min=['2020-04-12_MX', 2152, 61, 182.85438596491227, 570]
#Trajectory base file length>30km n_crisis >60
metricMax=['2020-04-02_MX', 4635, 61, 215.47416020671835, 774] #ByStartPt  #in series
mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay"##/geoStart #"/data/covid/CoronavirusMovementAdministrativeRegionsPerDay"#/2020-04-02_0000.csv"
filterStr="length_km>30 AND n_crisis>60"; 
filterDir=filterStr.replace(">","").replace(" ","")
title="Trajectories with displacement {}".format(filterStr)
pathToMob=os.path.join(allMobi, metricMax[0]+".csv")
vlayerBase=plotTrajectory(pathToMob, filter=filterStr) #wkt="geometryStartEnd",
# uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField=geometry&wktType=Line".format(os.path.join(allMobi, metricMax[0]+".csv"))
# vlayerBase = QgsVectorLayer(uri,metricMax[0][5:13],'delimitedtext')
# QgsProject.instance().addMapLayer(vlayerBase) #QGIS3
# vlayerBase.setSubsetString("start_polygon_name = end_polygon_name ") #AND percent_change  > 0
qgis.utils.iface.mapCanvas().saveAsImage('{}/{}/{}.png'.format(mobiVisuRes,filterDir, metricMax[0] ) )

#Next days trajectories
metricMax=['2020-04-17_MX', 4635, 61, 215.47416020671835, 774] #in series
pathToMob=os.path.join(allMobi, metricMax[0]+".csv")
vlayerNew=plotTrajectory(pathToMob, filter=filterStr)
# uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField=geometry&wktType=Line".format(os.path.join(allMobi, metricMax[0]+".csv"))
# vlayerNew = QgsVectorLayer(uri,metricMax[0][5:13],'delimitedtext')
# QgsProject.instance().addMapLayer(vlayerNew) #QGIS3
# vlayerNew.setSubsetString("length_km>30 AND flow >60.0 ") #AND percent_change  > 0

changeActiveLayerAndPasteStyle(vlayerBase, vlayerNew)
# qgis.utils.iface.setActiveLayer(vlayer)
# iface.actionCopyLayerStyle().trigger()
# qgis.utils.iface.setActiveLayer(vlayerNew)
# iface.actionPasteLayerStyle().trigger()

qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/visuRes/{}.png'.format(metricMax[0]))


#Start points
##########################################################################################################################3
plotStartPoints(pathToMob, filter=None,nLetters=8)
# uri = "file:/{}?delimiter=,&crs=epsg:4326&xField=start_lon&yField=start_lat".format(os.path.join(allMobi, metricMax[0]+".csv"))
# vlayerStartPts = QgsVectorLayer(uri,metricMax[0][5:13]+'StartPts','delimitedtext')
# QgsProject.instance().addMapLayer(vlayerStartPts) #QGIS3
# ml = QgsMapCanvasLayer(vlayerNew)
# ml.setVisible(False)







##########################################################################################################################3
###########################################################################################################
#REVIEWED
#Plot cases
pathToCasesCentroids = "/data/covid/casos/Casos_Diarios_Estado_Nacional_ConfirmadosCentroids.csv"
vlayerCases=plotCases(pathToCasesCentroids) #TODO: copy visu style
uri = "file:/{}?delimiter=,&crs=epsg:4326&xField=X&yField=Y".format(pathToCasesCentroids)
vlayerCases = QgsVectorLayer(uri,'Cases','delimitedtext')
QgsProject.instance().addMapLayer(vlayerCases) #QGIS3

#Add lines # "length_km">30AND"n_baseline">14.6 # low high mobility and change
from qgis.core import QgsProject #QGIS3
dataset='2020-04-02 1600'
pathToMob = "/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_{}.csv".format(dataset)
uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField=geometry&wktType=Line".format(pathToMob)
vlayerBase = QgsVectorLayer(uri,dataset,'delimitedtext')
QgsProject.instance().addMapLayer(vlayerBase) #QGIS3
vlayerBase.setSubsetString("start_polygon_name = end_polygon_name") #length_km<30
qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/visu/020800.png')

dataset='2020-04-02_1600'
allMobi="/data/covid/CoronavirusMovementAdministrativeRegions/"
uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField=geometry&wktType=Line".format(os.path.join(allMobi, dataset+".csv"))
vlayer = QgsVectorLayer(uri,'{}_A'.format(dataset),'delimitedtext')
QgsProject.instance().addMapLayer(vlayer) #QGIS3
vlayer.setSubsetString("start_polygon_name = end_polygon_name ") #AND percent_change  > 0

qgis.utils.iface.setActiveLayer(vlayerBase)
iface.actionCopyLayerStyle().trigger()
qgis.utils.iface.setActiveLayer(vlayer)
iface.actionPasteLayerStyle().trigger()

#######################################################################################################################3

# vlayer.getFeatures("\'length_km\' > 20 ")vlayer.GetFeature(0)
# filename = os.path.splitext(os.path.basename(fullname))[0]
pathToMob = "//data/covid/CoronavirusMovementAdministrativeRegions/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_{}.csv".format(dataset)
uri = 'file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s'%(pathToMob , 'EPSG:4326', ',', "start_lon", "start_lat")
layer = QgsVectorLayer(uri, '{}_A'.format(dataset), 'delimitedtext')#fullname
QgsProject.instance().addMapLayer(vlayerBase) #QGIS3# QgsVectorFileWriter.writeAsVectorFormat(layer, outdir + '/' + filename + '.shp', 'CP1250', None, 'ESRI Shapefile')
vlayerBase.setSubsetString("start_polygon_name = end_polygon_name")


outdir="/data/covid"
uri = 'file:///Users/ep9k/Desktop/SandraMonson/CountByZip.csv?delimiter=,'
csv_file = QgsVectorLayer(uri, 'Patient Data', 'delimitedtext')
QgsProject.instance().addMapLayer(csv_file)
