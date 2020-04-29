###########################################################################################################
# Visu 30  (largest) baseline(changes in timepoints?)

from qgis.core import QgsProject #QGIS3
pathToMob = "/data/covid/CoronavirusMovementAdministrativeRegions/2020-04-02_MX.csv"
#Add lines
uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField=geometry&wktType=Line".format(pathToMob)
vlayerNew = QgsVectorLayer(uri,'04-02_MX','delimitedtext')
QgsProject.instance().addMapLayer(vlayerNew) #QGIS3
vlayerNew.setSubsetString("length_km>30 AND n_baseline >14.0" ) #AND country = MX ##Does not reads text

qgis.utils.iface.setActiveLayer(vlayer)
iface.actionCopyLayerStyle().trigger()
qgis.utils.iface.setActiveLayer(vlayerNew)
iface.actionPasteLayerStyle().trigger()

qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/visu/020800.pn

###########################################################################################################

fullName = "/data/covid/CoronavirusMovementAdministrativeRegions/Mexico%20Coronavirus%20Disease%20Prevention%20Map%20Apr%2003%202020%20Id%20%20Movement%20between%20Administrative%20Regions_2020-04-020%20800.csv"
uri = "file:///%s?crs=%s&delimiter=%s&xField=%s&yField=%s&decimal=%s" % (fullname, 'EPSG:4326', ';', 'x', 'y', ',')

# uri = "file:///some/path/file.csv?delimiter={}&crs=EPSG:4723&wktField={}".format(";", "shape")

uri = "file://%s?delimiter=%s&crs=%s&wktField=%s&wktType=%s" % (fullName, 'EPSG:4326', ';', 'geometry', 'Line')
#uri="file://%s?delimiter=;&type=csv;detectTypes=yes;type=vector; wkbType=LineString;crs=EPSG:4326;spatialIndex=no;subsetIndex=no;watchFile=no"%(pathToMob)

pathToMob="/data/covid/MexicoCoronavirusDiseasePreventionMapApr032020IdMovementbetweenAdministrativeRegions_2020-04-020800.csv"

uri="file://%s?delimiter=;&type=csv;detectTypes=yes;wktField=geometry;crs=EPSG:4326;spatialIndex=no;subsetIndex=no;watchFile=no"%(pathToMob)

layer = QgsVectorLayer(uri, 'mobilityPercentChange', 'delimitedtext')
layer.isValid()

QgsProject.instance().addMapLayer(vlayer)

vlayer = iface.addVectorLayer(pathToMob, "mobilityPercentChange", "ogr")
if not vlayer:
  print("Layer failed to load!")

QgsProject.instance().mapLayers()

uri = "{}?delimiter={}&xField={}&yField={}".format(pathToMob,",", "start_lon", "start_lat")
vlayer = QgsVectorLayer(uri, "mobilityPercentChangeB", "delimitedtext")
layer.isValid()
QgsProject.instance().addMapLayers([vlayer])
vlayer = iface.addVectorLayer(pathToMob, "mobilityPercentChangeB", "ogr")

ayer = iface.activeLayer()
ayer.setDataSource(uri,"mobilityPercentChangeB", "delimitedtext")







QgsProject.instance().addMapLayer(layer)






layerPath="/data/covid/CoronavirusMovementAdministrativeRegions/Mexico%20Coronavirus%20Disease%20Prevention%20Map%20Apr%2003%202020%20Id%20%20Movement%20between%20Administrative%20Regions_2020-04-02%200800.csv"
vlayer = iface.addVectorLayer(layerPath, '04-02 0800 mobilityPercentChange', "ogr")
if not vlayer:
  print("Layer failed to load!")


QgsProject.instance().addMapLayer(layer)




source= expanded="1">

source="file:///data/covid/CoronavirusMovementAdministrativeRegions/Mexico%20Coronavirus%20Disease%20Prevention%20Map%20Apr%2003%202020%20Id%20%20Movement%20between%20Administrative%20Regions_2020-04-02%200000.csv?type=csv&amp;detectTypes=yes&amp;wktField=geometry&amp;geomType=Line&amp;crs=EPSG:4326&amp;spatialIndex=no&amp;subsetIndex=no&amp;watchFile=no&amp;subset=%22length_km%22%20%3E%2030%20%20AND%20%22n_baseline%22%20%3E%2014.6" name="04-02 0000 Crisis" expanded="0">
