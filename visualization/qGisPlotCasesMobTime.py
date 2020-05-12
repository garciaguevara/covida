from PyQt5.QtCore import QTimer
import pandas as pd
#lCasesAdminRegCum = iface.mapCanvas().currentLayer() #Copy and paste with respective layer
#vlayerBase = iface.mapCanvas().currentLayer()

#day=2
#date="{:02d}-04-2020".format(day)
#qgis.utils.iface.mapCanvas().saveAsImage('{}/{}/{}.png'.format(mobiVisuRes,filterDir, date ) )

pathCasesAdminRegCum = "/data/covid/casos/01_05/Casos_Diarios_Estado_Nacional_ConfirmadosCentroidsPerAdminRegionsByStartPtCumulative.csv"
with open(pathCasesAdminRegCum, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
    casesDF = pd.read_csv( pathCasesAdminRegCum )




allMobi="/data/covid/mobility/FB/26PerDay"
mobiVisuRes="/data/covid/visuRes"
dayRange=[3,22]
filterStr="length_km>30 AND n_crisis>60 AND CumCases>10"; filterDir=filterStr.replace(">","").replace(" AND ","")

day=dayRange[0]

def prepareMap():
    global vlayerBase
    date="{:02d}-04-2020".format(day)
    lCasesAdminRegCum.renderer().setClassAttribute(date)    
    pathToMob="{}/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX".format(day))
    lCasesAdminRegCum.triggerRepaint()    
#    casesLargerN_DF=casesDF[casesDF[date]>minCases]['PolygonID'][:120]    
#    filterStrDate=filterStr# When more than 130 municipaloties it fails!!!
#    print ("filterStr {}. \n{} of municipalities more than {} cases".format(filterStrDate,len(casesLargerN_DF),minCases ) )
#    for lCase, idC in zip(casesLargerN_DF, range(len(casesLargerN_DF)) ):
#        if idC == 0: filterStrDate+=" and ("
#        if not idC == len(casesLargerN_DF)-1: filterStrDate+="start_polygon_id={} or ".format(lCase)
#        else: filterStrDate+="start_polygon_id={} ) ".format(lCase)    
    
    vlayerNew=plotTrajectory(pathToMob, filter=filterStr)        
    changeActiveLayerAndPasteStyle(vlayerBase, vlayerNew)    
    vlayerNew.triggerRepaint()        
    vlayerBase=vlayerNew    
    QTimer.singleShot(1000, exportMap) # Wait a second and export the map

def exportMap():
    global day    
    #    time.sleep(1.5)
    date="{:02d}-04-2020".format(day)
    qgis.utils.iface.mapCanvas().saveAsImage('{}/{}/{}.png'.format(mobiVisuRes,filterDir, date ) )
    print("Save file {}/{}".format(filterDir, date))    
    if day < dayRange[1]:
        QTimer.singleShot(1000, prepareMap) # Wait a second and prepare next map
    day += 1
    
prepareMap()



#for feature in lCasesAdminRegCum.getFeatures():
#    print(feature["01-05-2020"])
#for field in lCasesAdminRegCum.fields():
#    print(field.name(), field.typeName())
#features = lCasesAdminRegCum.getFeatures()
#for feat in features:
#    attrs = feat.attributes()
#    print (attrs[1])
    