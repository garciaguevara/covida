from PyQt5.QtCore import QTimer
import pandas as pd
import cv2 as cv
import datetime
#vlayerBase = iface.mapCanvas().currentLayer() #Copy and paste with respective layer
#lCasesAdminRegCumFuture = iface.mapCanvas().currentLayer() 
#lCasesAdminRegCum = iface.mapCanvas().currentLayer() 


#day=2
#date="{:02d}-04-2020".format(day)
#qgis.utils.iface.mapCanvas().saveAsImage('{}/{}/{}.png'.format(mobiVisuRes,filterDir, date ) )

# pathCasesAdminRegCum = "/data/covid/casos/01_05/Casos_Diarios_Estado_Nacional_ConfirmadosCentroidsPerAdminRegionsByStartPtCumulative.csv"
# with open(pathCasesAdminRegCum, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
#     casesDF = pd.read_csv( pathCasesAdminRegCum )

wCases="wCases"
allMobi="/data/covid/mobility/FB/26PerDay/{}".format(wCases)
mobiVisuRes="/data/covid/visuRes"
dayRange=[2,22]
filterStr="length_km>30 AND (n_crisis/PoblacionStart)*100000.0>10.0 AND (CumCasesStart/PoblacionStart)*100000.0>10.0";
#filterStr="length_km>30 AND n_crisis>60 AND (CumCasesStart/PoblacionStart)*100000.0>10.0"
filterDir= "length_km30"
cumCasesScale = cv.imread('/data/covid/visuRes/length_km30/casesFuture100k.png') #/data/covid/visuRes/length_km30/n_crisis60CumCasesPer100k10/cumCasesScale.png
#trajScale = cv.imread('/data/covid/visuRes/length_km30/n_crisis60CumCasesPer100k10/trajScale.png')
trajScale = cv.imread('/data/covid/visuRes/length_km30/Per100kn_crisisCumCases10/trajPer100k.png')
dayLetter=['J','V','S','D','L','M','Mi']
day=dayRange[0]
daysFuture=14

def prepareMap():
    global vlayerBase
    dateStr="{:02d}-04-2020".format(day)
    date="( \"{}\" / \"poblacion\" ) * 100000.0".format(dateStr) #  ( "22-04-2020"  /  "poblacion"  ) * 100000 
    lCasesAdminRegCum.renderer().setClassAttribute(date)  
    
    date_1 = datetime.datetime.strptime(dateStr, "%d-%m-%Y")
    dateFut=date_1 + datetime.timedelta(days=daysFuture)
    dateFutureStr="{:02d}-{:02d}-2020".format(dateFut.day,dateFut.month)
    dateFuture="( \"{}\" / \"poblacion\" ) * 100000.0".format(dateFutureStr) #  ( "22-04-2020"  /  "poblacion"  ) * 100000 
    lCasesAdminRegCumFuture.renderer().setClassAttribute(dateFuture)        
    
    pathToMob="{}/2020-04-AAAA{}.csv".format(allMobi,wCases.replace("w","")).replace('AAAA',"{:02d}_MX".format(day))
    lCasesAdminRegCum.triggerRepaint()    
    lCasesAdminRegCumFuture.triggerRepaint()
#    casesLargerN_DF=casesDF[casesDF[date]>minCases]['PolygonID'][:120]    
#    filterStrDate=filterStr# When more than 130 municipaloties it fails!!!
#    print ("filterStr {}. \n{} of municipalities more than {} cases".format(filterStrDate,len(casesLargerN_DF),minCases ) )
#    for lCase, idC in zip(casesLargerN_DF, range(len(casesLargerN_DF)) ):
#        if idC == 0: filterStrDate+=" and ("
#        if not idC == len(casesLargerN_DF)-1: filterStrDate+="start_polygon_id={} or ".format(lCase)
#        else: filterStrDate+="start_polygon_id={} ) ".format(lCase)    
    
    vlayerNew=plotTrajectory(pathToMob,wkt="geometryStartEnd", filter=filterStr)        
    changeActiveLayerAndPasteStyle(vlayerBase, vlayerNew)    
    vlayerNew.triggerRepaint()        
    vlayerBase=vlayerNew    
    QTimer.singleShot(1000, exportMap) # Wait a second and export the map

def exportMap():
    global day    
    #    time.sleep(1.5)
    date="{:02d}-04-2020".format(day)
    
    mobCasesIm='{}/{}/{}_{}.png'.format(mobiVisuRes,filterDir, date, dayLetter[day%7-dayRange[0]] )
    qgis.utils.iface.mapCanvas().saveAsImage( mobCasesIm )
    print("Save file {}".format(mobCasesIm) )   
    
    mapIm = cv.imread( mobCasesIm )
#     plt.imshow(mapIm); plt.show()
#     plt.imshow( mapIm[ 550:(550+cumCasesScale.shape[0]), 350:(350+cumCasesScale.shape[1]), :] ); plt.show()    
    mapIm[ (mapIm.shape[0]-cumCasesScale.shape[0]):, :cumCasesScale.shape[1], :]=cumCasesScale #mapIm.shape[0]-
    mapIm[ :trajScale.shape[0], (mapIm.shape[1]-trajScale.shape[1]):, :]=trajScale
    cv.imwrite(mobCasesIm, mapIm)
    
    
    
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
    