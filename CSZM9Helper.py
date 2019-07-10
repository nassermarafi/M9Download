from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
__author__ = 'marafi'

def GetDeterminisitcGroundMotionsAtPoints(Stations, Coordinates, BLKFile, Folder_Locations):
    import os
    import subprocess
    import numpy as np

    f = open(Folder_Locations+'TempFile.txt','w')
    f.write(''.ljust(10)+'%d\n'%len(Stations))
    for i in range(len(Stations)):
        arg1 = '%.0f.'%(Coordinates[i][0])
        arg2 = '%.0f.'%(Coordinates[i][1])
        f.write(Stations[i].ljust(9)+arg1.ljust(12)+arg2.ljust(12)+'\n')
    f.close()

    p = subprocess.Popen(Folder_Locations+'readblock.exe', stdin=subprocess.PIPE, cwd=Folder_Locations)
    p.communicate(os.linesep.join([Folder_Locations+BLKFile,Folder_Locations+'TempFile.txt','0']))
    p.wait()

    DeterministicData = []
    for i in range(len(Stations)):
        Data = np.loadtxt(Folder_Locations+Stations[i])
        # Col1: Time, Col2: x velocity, Col3: y velocity, Col4: z velocity
        # Velocity is in meters per second

        Dt = Data[1,0]-Data[0,0]
        GMDataY = np.gradient(Data[:,1],Dt)/9.81
        GMDataX = np.gradient(Data[:,2],Dt)/9.81
        GMDataZ = np.gradient(Data[:,3],Dt)/9.81

        temp = {}
        temp['Station']=Stations[i]
        temp['Dt'] = Dt
        temp['GMDataX'] = GMDataX
        temp['GMDataY'] = GMDataY
        temp['GMDataZ'] = GMDataZ

        DeterministicData.append(temp)

        os.remove(Folder_Locations+Stations[i])

    return DeterministicData

def GetBroadband(Lat, Long, BroadbandFolder='Broadbands/Data/031514/'):
    import os
    import numpy
    import utm

    EastingNorthing = utm.from_latlon(Lat,Long,10)

    BroadbandLocation = BroadbandFolder

    SWCorner = [4467300, 100080]

    def GetIMs(Easting, Northing):
        #Rounding Function
        def round_to(n,precision):
            correction = 0.5 if n >= 0 else -0.5
            return int( n/precision+correction ) * precision

        try:
            f = open(BroadbandLocation+'Locations.utm')
        except:
            f = open(BroadbandLocation + 'BroadBandLocations.utm')

        precision = 1000
        Easting = round_to(Easting,precision)
        Northing = round_to(Northing,precision)

        #Get File Namel
        for line in f.readlines():
            line = line.split()
            y = round_to(float(line[1]),precision)
            x = round_to(float(line[2]),precision)
            if Easting == x and Northing == y:
                Name = line[0]

        import numpy as np
        try:
            RS = np.loadtxt(BroadbandLocation+'/%s/RS_(%s).dat'%(Name[:3],Name))
            Ds = np.loadtxt(BroadbandLocation+'/%s/Ds_(%s).dat'%(Name[:3],Name))
            GMData = np.loadtxt(BroadbandLocation+'/%s/%s.syn'%(Name[:3],Name))
        except:
            print('error, rs or ds file not found')
            return None

        class Output():
            def __init__(self):
                self.FileName = Name
                self.Periods = RS[:,0]
                self.SaX = RS[:,1]
                self.SaY = RS[:,2]
                self.DsX595 = Ds[0]
                self.DsY595 = Ds[1]
                self.DsX575 = Ds[2]
                self.DsY575 = Ds[3]

                self.GMDataY = GMData[:,2]
                self.GMDataX = GMData[:,3]
                self.Dt = GMData[1,0]-GMData[0,0]
        return Output()

    return GetIMs(EastingNorthing[0]-SWCorner[1], EastingNorthing[1]-SWCorner[0])

def ConvertUTMToLatLon(ModelEasting, ModelNorthing):
    import utm
    SWCorner = [4467300, 100080]
    EastingUTM = ModelEasting + SWCorner[1]
    NorthinUTM = ModelNorthing + SWCorner[0]
    LatLon = utm.to_latlon(EastingUTM, NorthinUTM, 10, 'T')

    return LatLon[0], LatLon[1]

def CopyBroadbandToM9GMSetFolder(Lat, Long, BroadbandFolder='/Broadbands/Data/031514/', GMFolder = '/GroundMotions/M9GMSet/R1-031514/'):
    import numpy as np
    import os
    O = GetBroadband(Lat, Long, BroadbandFolder)

    np.savetxt(os.getcwd()+GMFolder+'SortedEQFile_(%s1).dat'%O.FileName, O.GMDataX/386.4)
    np.savetxt(os.getcwd()+GMFolder+'SortedEQFile_(%s2).dat'%O.FileName, O.GMDataY/386.4)

    Wn = (2*np.pi/O.Periods)
    np.savetxt(os.getcwd()+GMFolder+'ResponseSpectrum_(%s1).dat'%O.FileName, np.transpose([O.Periods, O.SaX/Wn*386.4, O.SaX/Wn/Wn*386.4, O.SaX]), header='NGANo: %s \n Zeta: 0.05 \n Ds5-05: %f \n Comments: \n Period, SD, SV, SA'%(O.FileName, O.DsX595))
    np.savetxt(os.getcwd()+GMFolder+'ResponseSpectrum_(%s2).dat'%O.FileName, np.transpose([O.Periods, O.SaY/Wn*386.4, O.SaY/Wn/Wn*386.4, O.SaY]), header='NGANo: %s \n Zeta: 0.05 \n Ds5-05: %f \n Comments: \n Period, SD, SV, SA'%(O.FileName, O.DsY595))

    np.savetxt(os.getcwd()+GMFolder+'NumPointsFile_(%s1).dat'%O.FileName, [len(O.GMDataX)], fmt='%d')
    np.savetxt(os.getcwd()+GMFolder+'NumPointsFile_(%s2).dat'%O.FileName, [len(O.GMDataX)], fmt='%d')

    np.savetxt(os.getcwd()+GMFolder+'DtFile_(%s1).dat'%O.FileName, [O.Dt])
    np.savetxt(os.getcwd()+GMFolder+'DtFile_(%s2).dat'%O.FileName, [O.Dt])

def GetRClosetDistance(SlipFile, LatLongs, SWCornerLatLong=[40.26059706792827, -127.70217428430801], ZoneNumber=10):
    import numpy as np
    import utm

    #Slip File
    # N coord. (m), E coord. (m), depth (m), seismic moment for that source grid cell (Nm), start time (s), rise time (s), etc.

    SlipData = np.loadtxt(SlipFile, skiprows=2)[:,0:3]

    SWCornerUTM = utm.from_latlon(SWCornerLatLong[0], SWCornerLatLong[1], ZoneNumber)

    NorthingEasting = []
    RCD = []
    for LatLong in LatLongs:
        temp_utm = utm.from_latlon(LatLong[0], LatLong[1], ZoneNumber)
        northing = temp_utm[1]-SWCornerUTM[1]
        easting = temp_utm[0]-SWCornerUTM[0]
        NorthingEasting.append([northing, easting])
        RCD.append(np.min(np.sqrt((SlipData[:,0]-northing)**2.+(SlipData[:,1]-easting)**2.+(SlipData[:,2])**2.))/1000.)

    return RCD

def GenerateLatLonListForAllStationCodes(DataArchive='F:/M9/DataArchive/', realization='csz002'):
    import numpy as np
    AllSites = []
    for Map in ['A','B','C','D','E','Y','Z']:
        SiteLocations = np.loadtxt(DataArchive + realization + '/' + Map + '/BroadBandLocations.utm', skiprows=1, dtype=str)
        for i in range(len(SiteLocations)):
            lat, lon = ConvertUTMToLatLon(float(SiteLocations[i][2]), float(SiteLocations[i][1]))
            AllSites.append([SiteLocations[i][0],lat, lon])

    np.savetxt(DataArchive + 'AllLatLon.dat', AllSites, fmt='%s')