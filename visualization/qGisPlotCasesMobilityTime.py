from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets#from PyQt5.QtGui import qApp
inst = QtWidgets.QApplication.instance()

#lCasesAdminRegCum = iface.mapCanvas().currentLayer()
#vlayerBase = iface.mapCanvas().currentLayer()

allMobi="/data/covid/mobility/FB/26PerDay"
mobiVisuRes="/data/covid/visuRes"
dayRange=[3,23]
filterStr="length_km>30 AND n_crisis>60"; filterDir=filterStr.replace(">","").replace(" ","")
for day in range(dayRange[0],dayRange[1]):
#day =15
    date="{:02d}-04-2020".format(day)
    lCasesAdminRegCum.renderer().setClassAttribute(date)    
    pathToMob="{}/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX".format(day))
    vlayerNew=plotTrajectory(pathToMob, filter=filterStr)        
    changeActiveLayerAndPasteStyle(vlayerBase, vlayerNew)
    
    lCasesAdminRegCum.triggerRepaint()
    vlayerNew.triggerRepaint()
    inst.processEvents()
    print("Save file {}/{}".format(filterDir, date))
#    time.sleep(1.5)
    qgis.utils.iface.mapCanvas().saveAsImage('{}/{}/{}.png'.format(mobiVisuRes,filterDir, date ) )
    vlayerBase=vlayerNew