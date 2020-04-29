from qgis.core import QgsProject #QGIS3
pathToCasesCentrois = "/data/covid/casos/Casos_Diarios_Estado_Nacional_ConfirmadosCentroids.csv"

#Add points
uri = "file:/{}?delimiter=,&crs=epsg:4326&xField=X&yField=Y".format(pathToCasesCentrois)
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






##########################################################################################################################3




##########################################################################################################################3



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
