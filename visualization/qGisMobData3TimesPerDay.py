from qGisPlotMobData import *

pathToMob = "/data/covid/MexicoCoronavirusDiseasePreventionMapApr032020IdMovementbetweenAdministrativeRegions_2020-04-020800.csv"
plotStartPoints(pathToMob)

#Plot base trajectory "vlayerBase" same start and point local movement 
dataset='2020-04-02 1600'
pathToMob = "/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_{}.csv".format(dataset)
vlayerBase=plotTrajectory(pathToMob, filter="start_polygon_name = end_polygon_name")
qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/visu/020800.png')

#Plot new "vlayer" trajectory local movement 
dataset='2020-04-02_1600'
allMobi="/data/covid/CoronavirusMovementAdministrativeRegions/"
pathToMob = os.path.join(allMobi, dataset+".csv")
vlayer=plotTrajectory(pathToMob, filter="start_polygon_name = end_polygon_name") #AND percent_change  > 0

changeActiveLayerAndPasteStyle(vlayerBase, vlayer)


#TODO: Consider filtering
#    Visu 30  (largest) baseline(changes in timepoints?) -> "length_km>30 AND n_baseline >14.0" 
#
##########################################################################################################################3

pathToCasesCentroids = "/data/covid/casos/Casos_Diarios_Estado_Nacional_ConfirmadosCentroids.csv"
vlayerCases=plotCases(pathToCasesCentroids) #TODO: copy visu style

##########################################################################################################################3
# vlayer.getFeatures("\'length_km\' > 20 ")vlayer.GetFeature(0)
# filename = os.path.splitext(os.path.basename(fullname))[0]
# pathToMob = "//data/covid/CoronavirusMovementAdministrativeRegions/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_{}.csv".format(dataset)
# uri = 'file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s'%(pathToMob , 'EPSG:4326', ',', "start_lon", "start_lat")
# layer = QgsVectorLayer(uri, '{}_A'.format(dataset), 'delimitedtext')#fullname
# QgsProject.instance().addMapLayer(vlayerBase) #QGIS3# QgsVectorFileWriter.writeAsVectorFormat(layer, outdir + '/' + filename + '.shp', 'CP1250', None, 'ESRI Shapefile')
# vlayerBase.setSubsetString("start_polygon_name = end_polygon_name")# 
# outdir="/data/covid"
# uri = 'file:///Users/ep9k/Desktop/SandraMonson/CountByZip.csv?delimiter=,'
# csv_file = QgsVectorLayer(uri, 'Patient Data', 'delimitedtext')
# QgsProject.instance().addMapLayer(csv_file)
