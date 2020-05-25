import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.gridspec as gridspec
from matplotlib import ticker

import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial import Voronoi, voronoi_plot_2d
from scipy import spatial #from sklearn.neighbors import KDTree
from scipy.sparse import *
from scipy import io
from scipy import *
import pickle
import datetime
import unicodedata
from matplotlib.colors import LinearSegmentedColormap
import colorsys
import numpy as np
import matplotlib.colors as colors
import utils as ut
import casesStats as caSts

def computeMobilityMatrix(dayRange):    
    if os.path.exists(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo)):
        with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'rb') as matchTreeFile:
            tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay = pickle.load(matchTreeFile)    
    
#     adminRegPerDay=[]; totalReg=[];totalGeoLoc=[]; totalGeoLocName=[];
#     totalRegSet=set([]); totalLargerChangeLoc=[]       
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo))
        if os.path.exists(mobMatrixFile.replace("csv", "mtx")):
            print ("Mobility matrix exists {}".format(mobMatrixFile.replace("csv", "mtx"))); continue
        with open(mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
            mobiDF = pd.read_csv( mobiTempPerDay.replace('AAAA',"{:02d}_MX".format(day)) )
        
        mobility=lil_matrix( ( len(tReg), len(tReg) ), dtype=int64 ) #csr_matrix
        
        admRegIdStart=mobiDF.start_polygon_id.unique(); admRegIdEnd=mobiDF.end_polygon_id.unique();
        admRegSetStart=set(admRegIdStart);admRegSetEnd=set(admRegIdEnd)        
#         #split geometry
#         test = mobiDF["geometry"].str.replace("LINESTRING \(", "", n=1)
#         test=test.str.replace("\)", "", n=1)
#         test = test.str.split(",", n=1, expand=True)            
#         #TODO: geometry with start end lat lons
#         testStart = test[0].str.split(" ", n=1, expand=True);    testEnd = test[1].str.split(" ", n=2, expand=True)#testEnd=test.str.replace(",", "", n=1)
#         mobiDF["geoStartLat"]= testStart[1].astype('float64');    mobiDF["geoStartLon"]= testStart[0].astype('float64')#convert_objects(convert_numeric=True) #
#         mobiDF["geoEndLat"]= testEnd[2].astype('float64');    mobiDF["geoEndLon"]= testEnd[1].astype('float64')
#         geoLoc=[]; geoLocName=[]; largerChangeLoc=[]        
#         test = pd.DataFrame(columns = ['start_lon', 'start_lat','end_lon', 'end_lat'])
#         test['start_lon']=mobiDF['start_lon'].transform(lambda x: "LINESTRING ("+str(x))
#         test['start_lat']=mobiDF['start_lat'].transform(lambda x: " "+str(x)+", ")
#         test['end_lon']=mobiDF['end_lon'].transform(lambda x: str(x)+" ")
#         test['end_lat']=mobiDF['end_lat'].transform(lambda x: str(x)+")")            
#         mobiDF["geometryStartEnd"]= test[['start_lon', 'start_lat','end_lon', 'end_lat']].agg(''.join, axis=1)
# #         df['period'] = df[['Year', 'quarter', ...]].agg('-'.join, axis=1)#         mobiDF[['start_lon', 'start_lat','end_lon', 'end_lat']].agg( lambda x: ', '.join(str(x)), axis=1 ) 
        for mobIdx,admRegID, admRegName in zip(xrange(len(tReg)), tReg, tGeoLocName): #TODO: Only look for non added, or compare the diff coordinates
            if len(mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values)>0:
                idName=mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values[0]
                if admRegName!=idName:
                    print("AdminRegions name {} diff {}".format(admRegName,idName) )
            else:
                 print("AdminRegions name not found in mobility data {} diff {}".format(admRegName,mobiDF[mobiDF['start_polygon_id']==admRegID].head(1)['start_polygon_name'].values) )
                 
            O_idD=mobiDF[mobiDF['start_polygon_id']==admRegID]['end_polygon_id']
            #indices = np.where( np.in1d( tReg, list(O_idD) ) )[0] #NOT SORTED!!
            #BAD sort
#             xe = np.outer([1,]*len(tReg), O_idD)
#             ye = np.outer(tReg, [1,]*len(O_idD))
#             junk, indices = np.where(np.equal(xe, ye))
            tReg=np.array(tReg)
            O_idD=np.array(list(O_idD))            
            
            index = np.argsort(tReg)
            sorted_x = tReg[index]
            sorted_index = np.searchsorted(sorted_x, O_idD)
            yindex = np.take(index, sorted_index, mode="clip")
#             mask = tReg[yindex] != O_idD
#             result = np.ma.array(yindex, mask=mask)
            
            O_flowD=mobiDF[mobiDF['start_polygon_id']==admRegID]['n_crisis']
#             if mobIdx==45: print("Find negative mobility at {} add {}".format(mobility[45,46], list(O_flowD)))
            mobility[mobIdx,yindex]=list(O_flowD) #np.mean(mobility[0,:]); np.max(mobility[0,:]); #np.std(mobility[0,:]);
        
        negMob=np.where(mobility.toarray()<0)
        io.mmwrite(mobMatrixFile.replace("csv", "mtx"), mobility)
        
        fig = plt.figure(figsize=(11.0, 11.0));ax = fig.add_subplot(111);
        ax.spy(mobility.toarray(), markersize=1); ax.set_ylabel("Origin"); ax.set_xlabel("Destination")        
        _,mobDate=os.path.split(mobMatrixFile); fig.suptitle("AdminRegions facebook mobility Matrix {}".format(mobDate.replace("_MXByStartPt.csv","")));
        fig.savefig(mobMatrixFile.replace("csv", "png").replace("mobMatrices", "mobMatrices/plots"), bbox_inches='tight');
        
        cmap=ut.fixInitialValueColorMap()
        fig2 = plt.figure(figsize=(11.0, 11.0));ax2 = fig2.add_subplot(111);
        pos2=ax2.imshow(mobility.toarray(), aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50] 
        fig2.colorbar(pos2, ax=ax2) ;ax2.set_ylabel("Origin"); ax2.set_xlabel("Destination")
        #'Ecatepec de Morelos'->'Iztapalapa' mobility[714,706];tGeoLocName[714];tGeoLocName[706];mobility[682,682];
        

def plotMobmatrix(mobMetroArea,namesMetroArea,ax,fig, verbLeg=True,limDef=None, sTitle=""):
    cmap=ut.fixInitialValueColorMap()
    if limDef is None:
        pos=ax.imshow(mobMetroArea, aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50]    
    else:
        pos=ax.imshow(mobMetroArea, aspect='equal', cmap=cmap, vmax=limDef, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50]    
    
    xAxis=[x for x in range(len(namesMetroArea))]; 
    
    plt.xticks(xAxis,[unicode(x,'utf-8')[:4] for x in namesMetroArea], rotation='vertical')        
    fig.colorbar(pos, ax=ax); 
    
    if verbLeg:
        ax.set_ylabel("Origin " +sTitle); plt.yticks(xAxis, [unicode(x,'utf-8') for x in namesMetroArea])
    else:
        namesMetroAreaStr=[]
        for idx, x in zip(xrange(len(namesMetroArea)),namesMetroArea):
            namesMetroAreaStr.append( unicode(str(idx)+' '+x[:4],'utf-8') )
        plt.yticks(xAxis,namesMetroAreaStr)
        ax.set_title(sTitle)
    
    ax.set_xlabel("Destination"); 

def getMobilityPerMetropolitanAreaMatrix(dayRange): #, normalize=False
    maxMobiFile=allMobi+"mobMatrices/metro/MTY/plots/raw/maxPerDay.pkl"
    if os.path.exists(maxMobiFile) :
        return 
#         with open(maxMobiFile, 'rb') as extentFilePkl: #save selected hypothesis
#             mobMaxPerDay=pickle.load(extentFilePkl)
#         maxDefList=[]; maxDefOffDiagList=[]
#         for mobMax in mobMaxPerDay:
#             maxDefList.append(mobMax.max);
#             maxDefOffDiagList.append(mobMax.maxOffDiag)
#         maxDef=np.max(maxDefList);maxDefOffDiag=np.max(maxDefOffDiagList);
#     elif os.path.exists(maxMobiFile) and not normalize: return
#     else: maxDef=None;maxDefOffDiag=None
        
    ptMTY=[-100.31109249700000419, 25.64490731320000094]#LINESTRING (-100.283203125 25.562238774210538) 
    ptTeran=[-99.41303383000000338, 25.27589694790000152] #LINESTRING (-99.629296875 25.330469955007835
    if os.path.exists(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo)):
        with open(allMobi+"mobilityCoordMerged{}.pkl".format(joinByMobGeo), 'rb') as matchTreeFile:
            tReg, tGeoLoc,tGeoLocName, tLargerChangeLoc, adminRegPerDay = pickle.load(matchTreeFile)    

    #TODO: def getMetroByMobility():
    
    #TODO: def getMetroByDistance():
    tGeoLocInv=np.array(tGeoLoc)#TODO: the latitude and longitude coordinates are in the wrong order
    tGeoLocInv[:,[0, 1]] = tGeoLocInv[:,[1, 0]]; tReg=np.array(tReg); tGeoLocName=np.array(tGeoLocName)
    tree = spatial.KDTree(tGeoLocInv) #KDTree(
    nearest_dist, nearest_idx = tree.query(ptMTY, k=21) #.query_radius(points, r=1.5)     
    namesMetroArea=tGeoLocName[list(nearest_idx)]
    print("Admin Regions within metropolitan area {}".format(tGeoLocName[list(nearest_idx)]) )
    with open(covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo)), 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        casosCentroidsDF = pd.read_csv( covCasos.replace('.',"CentroidsPerAdminRegions{}.".format(joinByMobGeo)) )
    
    df = pd.DataFrame()
    for nearIdx in nearest_idx:
        metroAdminReg = casosCentroidsDF[casosCentroidsDF['PolygonID']==tReg[nearIdx] ]
        df=df.append(metroAdminReg, ignore_index=True, sort=False)

    df.to_csv(covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}.".format(joinByMobGeo,MetroArea)),index=False)
    print("MetroArea {}\n".format( covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}.".format(joinByMobGeo,MetroArea)) ) )
    caSts.computeCumulativeCases(covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}.".format(joinByMobGeo,MetroArea)))
    
    mobMaxPerDay=[]; #totalReg=[];totalGeoLoc=[]; totalGeoLocName=[];#     totalRegSet=set([]); totalLargerChangeLoc=[] 
      
    #TODO: def extractMobilityFromMunicpalities():
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/2020-04-AAAA.csv".format(allMobi).replace('AAAA',"{:02d}_MX{}".format(day,joinByMobGeo))
        mobility=io.mmread(mobMatrixFile.replace("csv", "mtx") ).tocsr()
        
        mobMetroArea=lil_matrix( ( len(nearest_idx), len(nearest_idx) ), dtype=int64 )
        for idxMetroR, idxR in zip(xrange(len(nearest_idx)), nearest_idx):
            for idxMetroC, idxC in zip(xrange(len(nearest_idx)), nearest_idx):
                mobMetroArea[idxMetroR, idxMetroC]=mobility[idxR, idxC] #mobility[nearest_idx[4], nearest_idx[4]]

        mobMatrixFile="{}mobMatrices/{}/2020-04-AAAA.csv".format(allMobi,"metro/MTY").replace('AAAA',"{:02d}_MX{}{}".format(day,joinByMobGeo,MetroArea))
        io.mmwrite(mobMatrixFile.replace("csv", "mtx"), mobMetroArea)        
        
        fig = plt.figure(figsize=(12.0, 5.0)); ax = fig.add_subplot(121); mobMetroArea=mobMetroArea.toarray()
        plotMobmatrix(mobMetroArea,namesMetroArea,ax, fig)#,limDef=maxDef        
        maxMob = np.max(mobMetroArea); muni = np.argmax(mobMetroArea)
        muniOrg=muni/len(namesMetroArea); muniDest=muni%len(namesMetroArea)
        maxTraj="{}->{}_{}->{}".format(namesMetroArea[muniOrg], namesMetroArea[muniDest], nearest_idx[muniOrg], nearest_idx[muniDest])
        
        _,mobDate=os.path.split(mobMatrixFile); dateMetro=mobDate.replace("_MXByStartPt{}.csv".format(MetroArea)," "+MetroArea)               
        
#         mask = np.ones(mobMetroArea.shape, dtype=bool); np.fill_diagonal(mask, 0); 
#         maxOffDiag = mobMetroArea[mask].max(); maxOffDiagNumi = mobMetroArea[mask].argmax();        
        np.fill_diagonal(mobMetroArea, 0); maxOffDiag = mobMetroArea.max(); muniOffDiag = mobMetroArea.argmax()
        muniOrg=muniOffDiag/len(namesMetroArea); muniDest=muniOffDiag%len(namesMetroArea); #mobMetroArea[muniOrg,muniDest]
        maxTrajOffDiag="{}->{}_{}->{}".format(namesMetroArea[muniOrg], namesMetroArea[muniDest], nearest_idx[muniOrg], nearest_idx[muniDest])         
        ax2 = fig.add_subplot(122); plotMobmatrix(mobMetroArea,namesMetroArea,ax2, fig, verbLeg=False) #, limDef=maxDefOffDiag

        mobMaxPerDay.append( ut.mobilityMatrixMetric( dateMetro, maxMob, unicode(maxTraj,'utf-8'), maxOffDiag, unicode(maxTrajOffDiag,'utf-8') ) )    
              
        fig.suptitle( unicode("AdminRegions facebook mobility Matrix {} OffDiag max {} traj {}".format( dateMetro, maxOffDiag, maxTrajOffDiag), 'utf-8') );
        fig.savefig(mobMatrixFile.replace("csv", "png").replace("metro/MTY", "metro/MTY/plots/raw"), bbox_inches='tight')

    with open(maxMobiFile, 'wb') as extentFilePkl: #save selected hypothesis
        pickle.dump(mobMaxPerDay, extentFilePkl)
        #Test #namesMetroArea[5];namesMetroArea[12];mobMetroArea[5,12]
#         fig2 = plt.figure(figsize=(11.0, 11.0));ax2 = fig2.add_subplot(111);
#         pos2=ax2.imshow(mobility.toarray(), aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50] 
#         fig2.colorbar(pos2, ax=ax2) ;mobility[682,682]

#colors.LogNorm(vmin=mobMetroArea.toarray().min()+.0000000001, vmax=mobMetroArea.toarray().max())
#         plt.clim(10, np.max(mobMetroArea.toarray()) );                
#         fig = plt.figure(figsize=(11.0, 5.0));ax2 = fig.add_subplot(111);
#         plt.spy(mobMetroArea, markersize=4)
# fig = plt.figure(figsize=(11.0, 5.0));ax = fig.add_subplot(111);
# pos=ax.imshow(mobility[:200,:200].toarray(), aspect='auto', cmap='jet', norm=colors.PowerNorm(gamma=0.5) ) #[:50,:50]
# #colors.LogNorm(vmin=mobMetroArea.toarray().min()+.0000000001, vmax=mobMetroArea.toarray().max())
# fig.colorbar(pos, ax=ax)
#         pcm = ax[0].pcolor(X, Y, Z, norm=colors.LogNorm(vmin=Z.min(), vmax=Z.max()),
#         fig.colorbar(pcm, ax=ax[0], extend='max')
def cumCasesPer100k(casosMetroDF,populationsMetro,day):
    dateStrList=[];
    dateStr="{:02d}-04-2020".format(day)
    date_1 = datetime.datetime.strptime(dateStr, "%d-%m-%Y")        
    for dRange in xrange(-1,2):
        dateRange=date_1 + datetime.timedelta(days=dRange)
        dateRangeStr="{:02d}-{:02d}-2020".format(dateRange.day,dateRange.month)
        dateStrList.append(dateRangeStr)
        
    casesCum3Days=casosMetroDF[dateStrList].to_numpy().astype(np.double) #cum3=casesCum3Days*100000.0/populationsMetro[:,None]
    return casesCum3Days*100000.0/populationsMetro[:,None], dateStrList #casesCum3Days[1,2]*100000.0/populationsMetro[:,None][1]
    
def mobilityWithCasesPer100kMetro(dayRange):
    maxMobiFile=allMobi+"mobMatrices/metro/MTY/plots/raw/maxPerDay.pkl"
    if os.path.exists(maxMobiFile):
        with open(maxMobiFile, 'rb') as extentFilePkl: #save selected hypothesis
            mobMaxPerDay=pickle.load(extentFilePkl)
        maxDefList=[]; maxDefOffDiagList=[]
        for mobMax in mobMaxPerDay:
            maxDefList.append(mobMax.max);
            maxDefOffDiagList.append(mobMax.maxOffDiag)
        maxDef=np.max(maxDefList);maxDefOffDiag=np.max(maxDefOffDiagList);
    else: maxDef=None;maxDefOffDiag=None
    
    casosMetroPath=covCasos.replace('.',"CentroidsPerAdminRegions{}_Metro{}Cumulative.".format(joinByMobGeo,MetroArea))

    with open(casosMetroPath, 'r') as f:  #os.path.join(allMobi, timePoint) #print("{:02d}".format(day))
        casosMetroDF = pd.read_csv( casosMetroPath )
    namesMetroArea=casosMetroDF['PolygonName']; populationsMetro=casosMetroDF['poblacion'].to_numpy().astype(np.double)

    maxMobiFilePer100k=allMobi+"mobMatrices/metro/MTY/plots/per100k/maxPerDayPer100k.pkl"
    if os.path.exists(maxMobiFilePer100k):
        with open(maxMobiFilePer100k, 'rb') as extentFilePkl: #save selected hypothesis
            maxMobOffDiag=pickle.load(extentFilePkl)
    else:
        maxMobOffDiag=[]
        for day in range(dayRange[0],dayRange[1]): #
            mobMatrixFile="{}mobMatrices/{}/2020-04-AAAA.csv".format(allMobi,"metro/MTY").replace('AAAA',"{:02d}_MX{}{}".format(day,joinByMobGeo,MetroArea))
            mobMetroArea=io.mmread(mobMatrixFile.replace("csv", "mtx") ).toarray()
            
            fig = plt.figure(figsize=(20.0, 14.0)); ax = fig.add_subplot(221); plotMobmatrix(mobMetroArea,namesMetroArea,ax, fig, limDef=maxDef ) 
            mobMetroAreaOffDiag=np.copy(mobMetroArea)
            np.fill_diagonal(mobMetroAreaOffDiag, 0);
            ax2 = fig.add_subplot(222); plotMobmatrix(mobMetroAreaOffDiag,namesMetroArea,ax2, fig, limDef=maxDefOffDiag, verbLeg=False, sTitle='OffDiag'  ) 
            
            mobMetroAreaPer100k=(mobMetroArea*100000.0/populationsMetro[:,None])#mobMetroArea[3,1]*100000.0/populationsMetro[:,None][3] mobMetroAreaPer100k[3,1]
            ax3 = fig.add_subplot(223); plotMobmatrix(mobMetroAreaPer100k,namesMetroArea,ax3, fig, sTitle='per100k') 
    
            mobMetroOffDiagPer100k=(mobMetroAreaOffDiag*100000.0/populationsMetro[:,None])        
            
            maxOffDiag = mobMetroOffDiagPer100k.max(); muniOffDiag = mobMetroOffDiagPer100k.argmax(); maxMobOffDiag.append(maxOffDiag)
            muniOrg=muniOffDiag/len(namesMetroArea); muniDest=muniOffDiag%len(namesMetroArea); #mobMetroArea[muniOrg,muniDest]
            maxTrajOffDiag="{}->{}".format(namesMetroArea[muniOrg], namesMetroArea[muniDest])     
            
            ax4 = fig.add_subplot(224); plotMobmatrix(mobMetroOffDiagPer100k,namesMetroArea,ax4, fig, verbLeg=False)
    
            _,mobDate=os.path.split(mobMatrixFile); dateMetro=mobDate.replace("_MXByStartPt{}.csv".format(MetroArea)," "+MetroArea)  
            fig.suptitle( unicode("AdminRegions facebook mobility Matrix {} OffDiag Per100k  max {} traj {}".format( dateMetro, maxOffDiag, maxTrajOffDiag), 'utf-8') );
            fig.savefig(mobMatrixFile.replace("csv", "png").replace("metro/MTY", "metro/MTY/plots/per100k"), bbox_inches='tight')
        with open(maxMobiFilePer100k, 'wb') as extentFilePkl: #save selected hypothesis
            pickle.dump(maxMobOffDiag,extentFilePkl)

    lastDateStr="{:02d}-04-2020".format(dayRange[1]+1)
    limCases=np.max(casosMetroDF[lastDateStr].to_numpy().astype(np.double)*100000.0/populationsMetro[:,None].transpose())
    spaceBC=np.empty((len(namesMetroArea),4));spaceBC[:] = np.NaN
    
    normMobMetroAreaPer100k=colors.PowerNorm(gamma=0.5,vmax=np.max(maxMobOffDiag), clip=False)
#         normMobMetroAreaPer100k.autoscale(mobMetroAreaPer100k)#,vmax=np.max(maxMobOffDiag)
#         sm = mpl.cm.ScalarMappable(cmap=cmap, norm=normMobMetroAreaPer100k)
#         sm.set_array([])
    cmap=ut.fixInitialValueColorMap()
    muniCumCasesTH=1.0; deltaCasesTH=4.0;mobiTH=4.0 #per100k
    for day in range(dayRange[0],dayRange[1]): #
        mobMatrixFile="{}mobMatrices/{}/2020-04-AAAA.csv".format(allMobi,"metro/MTY").replace('AAAA',"{:02d}_MX{}{}".format(day,joinByMobGeo,MetroArea))
        mobMetroArea=io.mmread(mobMatrixFile.replace("csv", "mtx") ).toarray()
        mobMetroAreaPer100k=(mobMetroArea*100000.0/populationsMetro[:,None])

        casesCum3DaysPer100k, dateStrList =cumCasesPer100k(casosMetroDF,populationsMetro, day)
        cum3DPer100kFut, dateFutList =cumCasesPer100k(casosMetroDF,populationsMetro, day+14)
                
        fig = plt.figure(figsize=(14.0, 9.0));  gs = gridspec.GridSpec(ncols=4, nrows=10, figure=fig)#        gs = fig.add_gridspec(4, 4)
        
        ax = fig.add_subplot( gs[0:7, 2:4] );
        pos=ax.pcolormesh(mobMetroAreaPer100k, cmap=cmap, norm=normMobMetroAreaPer100k, edgecolors='w', linewidth=0.01) #[:50,:50] 
#         pos=ax.imshow(mobMetroAreaPer100k, aspect='equal', cmap=cmap, norm=colors.PowerNorm(gamma=0.5), vmax=np.max(maxMobOffDiag), interpolation='None') #[:50,:50] 
#         plt.yticks(xAxis,[unicode(x,'utf-8')[:4] for x in namesMetroArea]) 
#         plt.xticks(xAxis,[unicode(x,'utf-8')[:4] for x in namesMetroArea], rotation='vertical')
        xAxis=[x+0.5 for x in range(len(namesMetroArea))]
        ax.set_yticks(xAxis); ax.set_yticklabels( [unicode(x,'utf-8')[:4] for x in namesMetroArea] )
        ax.set_xticks(xAxis); ax.set_xticklabels( [unicode(x,'utf-8')[:4] for x in namesMetroArea], rotation='vertical' )
        ax.set_ylabel("Origin");ax.set_xlabel("Destination")
        fig.colorbar(pos, ax=ax) ;                
#         # Major ticks
#         ax.grid(color='w', linestyle='-', linewidth=2)
#         ax.set_xticks(np.arange(0, mobMetroAreaPer100k.shape[0], 1));
#         ax.set_yticks(np.arange(0, mobMetroAreaPer100k.shape[1], 1))
#         # Labels for major ticks
#         ax.set_xticklabels(np.arange(1, mobMetroAreaPer100k.shape[0]+1, 1));
#         ax.set_yticklabels(np.arange(1, mobMetroAreaPer100k.shape[1]+1, 1));#          
#         # Minor ticks
#         ax.set_xticks(np.arange(-.5, mobMetroAreaPer100k.shape[0], 1), minor=True);
#         ax.set_yticks(np.arange(-.5, mobMetroAreaPer100k.shape[1], 1), minor=True);        
        # Gridlines based on minor ticks
#         ax.grid(which='minor', color='w', linestyle='-', linewidth=2)
        _,mobDate=os.path.split(mobMatrixFile); fig.suptitle("AdminRegions mobility per 100k {} OffDiagVmax={}".format(mobDate.replace("_MXByStartPt{}.csv".format(MetroArea)," "+MetroArea), np.max(maxMobOffDiag) ) );
        
        ax1 = fig.add_subplot(gs[0:7, :2]);  
        casesPer100kPF=np.concatenate((casesCum3DaysPer100k,spaceBC,cum3DPer100kFut ), axis=1)
        for i in xrange(4): dateStrList.append(".")
        dateStrList+=dateFutList        
        pos=ax1.pcolormesh(casesPer100kPF,  cmap=cmap, vmax=limCases,  edgecolors='w', linewidth=0.01 ) #[:50,:50] aspect='equal', norm=colors.PowerNorm(gamma=0.5),
#         plt.yticks(xAxis,[unicode(x,'utf-8') for x in namesMetroArea])
#         plt.xticks(xAxis[:len(dateStrList)],[unicode(x,'utf-8')[:5] for x in dateStrList], rotation='vertical')
        ax1.set_yticks(xAxis); ax1.set_yticklabels( [unicode(x,'utf-8') for x in namesMetroArea] )
        ax1.set_xticks(xAxis[:len(dateStrList)]); ax1.set_xticklabels( [unicode(x,'utf-8')[:5] for x in dateStrList], rotation='vertical' )
        ax1.set_xlabel("Date"); ax1.set_ylabel("Cases per 100k"); fig.colorbar(pos, ax=ax1)
        
        deltaCasesPer100k=(cum3DPer100kFut-casesCum3DaysPer100k)
        deltaCasesMax=np.max(deltaCasesPer100k,axis=1); casesCumMax=np.max(casesCum3DaysPer100k,axis=1);
        muniLargeIncre = np.where(deltaCasesMax>deltaCasesTH)[0]
        
        for muniL in muniLargeIncre:        
            orgMunisMob=mobMetroAreaPer100k[:,muniL]#.tolist()
            orgMunisIdx=np.where(orgMunisMob>mobiTH)[0].tolist() #ox=[]; dx=[]; dy=[];orgMunis=[]
            for idx in xrange(len(orgMunisIdx)):
#                 ox.append(3); dx.append(4); dy.append(muniL+0.5); 
#                 orgMunis.append(orgMunisIdx[idx]+0.5)                
                if casesCumMax[orgMunisIdx[idx]]>muniCumCasesTH:
                    colMap=cmap(normMobMetroAreaPer100k( orgMunisMob[orgMunisIdx[idx]] ) )
                    pl = plt.plot([3,7],[(orgMunisIdx[idx]+0.5), muniL+0.5],color=colMap)            
#             plt.quiver(ox, orgMunis, dx, dy, color=cmap(norm( orgMunisMob[orgMunisIdx].tolist() )) , scale=2,angles='xy')

        ax4 = fig.add_subplot(gs[8:11, 2:4]);
        pos=ax4.pcolormesh(deltaCasesPer100k.transpose(),  cmap=cmap, edgecolors='w', linewidth=0.01 ) #[:50,:50] aspect='equal',vmax=limCases, ,  norm=colors.PowerNorm(gamma=0.5)
#         plt.yticks(xAxis[:len(dateFutList)],[unicode(x,'utf-8')[:5] for x in dateFutList])
#         plt.xticks(xAxis,[unicode(x,'utf-8')[:5] for x in namesMetroArea ], rotation='vertical')
#         ax4 = fig.add_subplot(223); 
        ax4.set_yticks(xAxis[:len(dateFutList)]); ax4.set_yticklabels( [unicode(x,'utf-8')[:5] for x in dateFutList] )
        ax4.set_xticks(xAxis); ax4.set_xticklabels( [unicode(x,'utf-8')[:5] for x in namesMetroArea ], rotation='vertical' )
        ax4.set_xlabel("Cases per 100k delta"); ax4.set_ylabel("Date-14")

        cb=fig.colorbar(pos, ax=ax4); tick_locator = ticker.MaxNLocator(nbins=5)
        cb.locator = tick_locator;  cb.update_ticks()
        fig.savefig(mobMatrixFile.replace("csv", "png").replace("metro/MTY", "metro/MTY/plots/casesPer100k"), bbox_inches='tight');
    
    
def main():
    dayRange=[2,23]
    computeMobilityMatrix(dayRange)
    getMobilityPerMetropolitanAreaMatrix(dayRange) #, normalize=False
    mobilityWithCasesPer100kMetro(dayRange)
    
mobiVisuRes="/data/covid/visuRes"
allMobi="/data/covid/mobility/FB/26PerDay/"#/2020-04-02_0000.csv"
# mobiTemp="/data/covid/fb26/Mexico Coronavirus Disease Prevention Map Apr 03 2020 Id  Movement between Administrative Regions_2020-04-AAAA.csv"
mobiTempPerDay="{}2020-04-AAAA.csv".format(allMobi)
covCasos= "/data/covid/casos/12_05/Casos_Diarios_Municipio_Confirmados_20200512.csv" #"/data/covid/casos/12_05/Casos_Diarios_Estado_Nacional_Confirmados_20200512.csv" #/data/covid/casos/27_04
centroidPath="/data/covid/maps/Mapa_de_grado_de_marginacion_por_municipio_2015/IMM_2015/IMM_2015centroids.csv"
##################################################################################################################################################################################
baselinePerFile=[]; getCountry='MX'#'GT'#
joinByMobGeo="ByStartPt";  MetroArea="MTY"      #""    

if __name__ == "__main__":
    main()

    