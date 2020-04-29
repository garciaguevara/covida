import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from qgis.core import QgsProject #QGIS3
# BaselineMax=['2020-04-08_0000', 5455.8000000000002, 10.0, 2091]# in series 3 per day

# flow min=['2020-04-12_MX', 2152, 61, 182.85438596491227, 570]
metricMax=['2020-04-02_MX', 4635, 61, 215.47416020671835, 774] #in series

mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/fb26PerDay"#"/data/covid/CoronavirusMovementAdministrativeRegionsPerDay"#/2020-04-02_0000.csv"
title="Municipalities with displacement larger 30 km"

#Add lines base file
uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField=geometry&wktType=Line".format(os.path.join(allMobi, metricMax[0]+".csv"))
vlayerBase = QgsVectorLayer(uri,metricMax[0][5:13],'delimitedtext')
QgsProject.instance().addMapLayer(vlayerBase) #QGIS3
vlayerBase.setSubsetString("start_polygon_name = end_polygon_name ") #AND percent_change  > 0


qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/visuRes/{}.png'.format(metricMax[0]))

#Add lines base file
uri = "file:/{}?delimiter=,&crs=epsg:4326&xField=start_lon&yField=start_lat".format(os.path.join(allMobi, metricMax[0]+".csv"))
vlayerStartPts = QgsVectorLayer(uri,metricMax[0][5:13]+'StartPts','delimitedtext')
QgsProject.instance().addMapLayer(vlayerStartPts) #QGIS3
uri = "file:/{}?delimiter=,&crs=epsg:4326&xField=end_lon&yField=end_lat".format(os.path.join(allMobi, metricMax[0]+".csv"))
vlayerEndPts = QgsVectorLayer(uri,metricMax[0][5:13]+'EndPts','delimitedtext')
QgsProject.instance().addMapLayer(vlayerEndPts) #QGIS3





#Add lines next days
metricMax=['2020-04-17_MX', 4635, 61, 215.47416020671835, 774] #in series
uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField=geometry&wktType=Line".format(os.path.join(allMobi, metricMax[0]+".csv"))
vlayerNew = QgsVectorLayer(uri,metricMax[0][5:13],'delimitedtext')
QgsProject.instance().addMapLayer(vlayerNew) #QGIS3
vlayerNew.setSubsetString("length_km>30 AND flow >60.0 ") #AND percent_change  > 0


qgis.utils.iface.setActiveLayer(vlayer)
iface.actionCopyLayerStyle().trigger()
qgis.utils.iface.setActiveLayer(vlayerNew)
iface.actionPasteLayerStyle().trigger()

ml = QgsMapCanvasLayer(vlayerNew)
ml.setVisible(False)

qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/visuRes/{}.png'.format(metricMax[0]))
