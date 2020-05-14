from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets#from PyQt5.QtGui import qApp
import cv2
import matplotlib.pyplot as plt

# inst = QtWidgets.QApplication.instance()
#lCasesAdminRegCum = iface.mapCanvas().currentLayer()
#vlayerBase = iface.mapCanvas().currentLayer()

allMobi="/data/covid/mobility/FB/26PerDay"
mobiVisuRes="/data/covid/visuRes/length_km30/n_crisis60CumCasesPer100k10"
dayRange=[2,23]
filterStr="length_km>30 AND n_crisis>60"; filterDir=filterStr.replace(">","").replace(" ","")
cumCasesScale = cv2.imread('/data/covid/visuRes/length_km30/n_crisis60CumCasesPer100k10/cumCasesScale.png')
trajScale = cv2.imread('/data/covid/visuRes/length_km30/n_crisis60CumCasesPer100k10/trajScale.png')
dayLetter=['J','V','S','D','L','M','Mi']
for day in range(dayRange[0],dayRange[1]):
#day =15
    date="{:02d}-04-2020".format(day) #02-04-2020Per100k
    
#     Add image scales    #################################################################
#     mapIm = cv2.imread('{}/{}Per100k_{}.png'.format(mobiVisuRes, date, dayLetter[day%7-dayRange[0]] ) )
#     plt.imshow(mapIm); plt.show()
#     plt.imshow( mapIm[ 550:(550+cumCasesScale.shape[0]), 350:(350+cumCasesScale.shape[1]), :] ); plt.show()    
#     mapIm[ 550:(550+cumCasesScale.shape[0]), 350:(350+cumCasesScale.shape[1]), :]=cumCasesScale
#     mapIm[ 250:(250+trajScale.shape[0]), 1090:(1090+trajScale.shape[1]), :]=trajScale
#     mapIm[ (mapIm.shape[0]-cumCasesScale.shape[0]):, :cumCasesScale.shape[1], :]=cumCasesScale #mapIm.shape[0]-
#     mapIm[ :trajScale.shape[0], (mapIm.shape[1]-trajScale.shape[1]):, :]=trajScale
#     cv2.imwrite('{}/{}_{}.png'.format(mobiVisuRes, date, dayLetter[day%7-dayRange[0]] ), mapI
    lCasesAdminRegCum.renderer().setClassAttribute(date)    
    pathToMob="{}/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX".format(day))
    vlayerNew=plotTrajectory(pathToMob, filter=filterStr)        
    changeActiveLayerAndPasteStyle(vlayerBase, vlayerNew)
     
    lCasesAdminRegCum.triggerRepaint()
    vlayerNew.triggerRepaint()
#     inst.processEvents()
    print("Save file {}/{}".format(filterDir, date))
#    time.sleep(1.5)
    qgis.utils.iface.mapCanvas().saveAsImage('{}/{}/{}.png'.format(mobiVisuRes,filterDir, date ) )    
 
    vlayerBase=vlayerNew