from PyQt5.QtCore import QTimer
#lCasesAdminRegCum = iface.mapCanvas().currentLayer() #Copy and paste with respective layer
#vlayerBase = iface.mapCanvas().currentLayer()

#day=2
#date="{:02d}-04-2020".format(day)
#qgis.utils.iface.mapCanvas().saveAsImage('{}/{}/{}.png'.format(mobiVisuRes,filterDir, date ) )

allMobi="/data/covid/mobility/FB/26PerDay"
mobiVisuRes="/data/covid/visuRes"
dayRange=[3,25]
filterStr="length_km>30 AND n_crisis>60"; filterDir=filterStr.replace(">","").replace(" ","")

day=dayRange[0]

def prepareMap():
    global vlayerBase
    date="{:02d}-04-2020".format(day)
    lCasesAdminRegCum.renderer().setClassAttribute(date)    
    pathToMob="{}/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX".format(day))
    lCasesAdminRegCum.triggerRepaint()
    
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
    
    