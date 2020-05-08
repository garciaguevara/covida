import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial import Voronoi, voronoi_plot_2d
import pickle
import unicodedata
from matplotlib.colors import LinearSegmentedColormap
import colorsys
import numpy as np

mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos="/data/covid/casos/01_05/Casos_Diarios_Estado_Nacional_Confirmados.csv" #/data/covid/casos/27_04
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
#Join databases per day
# title="Municipalities with displacement larger 30 km per day"
baselinePerFile=[]; getCountry='MX'#'GT'#

joinByMobGeo="ByStartPt"#""

casesPerAdmReg=covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo))
with open(casesPerAdmReg, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
    df = pd.read_csv( casesPerAdmReg )

df.loc[:, '05-01-2020':'01-05-2020']=df.loc[:, '05-01-2020':'01-05-2020'].cumsum(axis=1)

df.to_csv(casesPerAdmReg.replace('.csv', 'Cumulative.csv'),index=False)
print("Missing elements {} {}".format(emptyAdminRegions, len(emptyAdminRegions) ) )