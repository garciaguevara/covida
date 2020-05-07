
dates=["20-04-2020"]#
for date in dates:
    vlayerCasesAdminReg.renderer().setClassAttribute(date)
    
    vlayerCasesAdminReg.triggerRepaint()
    qgis.utils.iface.mapCanvas().saveAsImage('/data/covid/casos/01_05/{}.png'.format(date))