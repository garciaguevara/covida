import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from qgis.core import QgsProject #QGIS3

#Plot fb mobility per admin regions level3
def changeActiveLayerAndPasteStyle(vlayerBase, vlayer):
    qgis.utils.iface.setActiveLayer(vlayerBase)
    iface.actionCopyLayerStyle().trigger() #TODO: turnOff base visibility
    qgis.utils.iface.setActiveLayer(vlayer)
    iface.actionPasteLayerStyle().trigger()#TODO: turnOn new layer visibility and save Image 

def plotStartPoints(pathToMob, filter=None,nLetters=8):
    #Plot start points
    # uri = "file:/{}?delimiter=,&crs=epsg:4326&xField=end_lon&yField=end_lat".format(os.path.join(allMobi, metricMax[0]+".csv"))
    # vlayerEndPts = QgsVectorLayer(uri,metricMax[0][5:13]+'EndPts','delimitedtext')
    # QgsProject.instance().addMapLayer(vlayerEndPts) #QGIS3
    uri = "file:/{}?delimiter=,&crs=epsg:4326&xField=start_lon&yField=start_lat".format(pathToMob)
    _,t=os.path.split(pathToMob); t=t.replace(".csv","")
    vlayerPts = QgsVectorLayer(uri,t[-nLetters:]+'Pts','delimitedtext'); 
    if not vlayerPts.isValid(): print("StartPts layer {} failed to load!".format(t[-nLetters:]))
    QgsProject.instance().addMapLayer(vlayerPts) #QGIS3
    if not filter is None:
        vlayerPts.setSubsetString(filter) #"start_polygon_name = end_polygon_name"        
    return vlayerPts

def plotTrajectory(pathToMob, wkt="geometry",filter=None,nLetters=8):
    uri = "file:/{}?delimiter=,&crs=epsg:4326&wktField={}&wktType=Line".format(pathToMob,wkt)
    _,t=os.path.split(pathToMob); t=t.replace(".csv","")
    vlayerBase = QgsVectorLayer(uri,t[5:11]+'Traj','delimitedtext'); 
    if not vlayerBase.isValid(): print("Traj layer {} failed to load!".format(t[-nLetters:]))    
    QgsProject.instance().addMapLayer(vlayerBase) #QGIS3
    if not filter is None:
        vlayerBase.setSubsetString(filter) #"start_polygon_name = end_polygon_name"
        #length_km<30 #"length_km">30AND"n_baseline">14.6 # low high mobility and change
    return vlayerBase

def plotCases(pathToCasesCentroids, posIdx=['X','Y'], filter=None,nLetters=8):
    #Add points cases 
    uri = "file:/{}?delimiter=,&crs=epsg:4326&xField={}&yField={}".format(pathToCasesCentroids,posIdx[0],posIdx[1])
    _,t=os.path.split(pathToCasesCentroids); t=t.replace(".csv","")
    vlayerCases = QgsVectorLayer(uri,t[-nLetters:]+'Cases','delimitedtext'); 
    if not vlayerCases.isValid(): print("Cases centroids layer {} failed to load!".format(t[-nLetters:]))
    if not filter is None:
        vlayerCases.setSubsetString(filter) 
    QgsProject.instance().addMapLayer(vlayerCases) #QGIS3
    return vlayerCases


















