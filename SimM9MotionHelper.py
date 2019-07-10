from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import os
from six.moves import range

BroadbandLocation = ''#os.getcwd() + '/Broadbands/Data/%s/A/'%Realization
path = ''#os.getcwd() + '/Broadbands/Data/%s/B/'%Realization
SlipFilePath = ''#os.getcwd()+'/Broadbands/RawData/%s/%s'%(Realization, SourceFile)

############################################# Methods #################################################################

LogicTreeRealizations = [
                    'csz001',  # 30
                    'csz002',  # 31
                    'csz003',  # 32
                    'csz004',  # 37
                    'csz005',  # 34
                    'csz006',  # 38
                    'csz007',  # 39
                    'csz008',  # 40
                    'csz009',  # 41
                    'csz010',  # 42
                    'csz011',  # 43
                    'csz012',  # 44
                    'csz013',  # 46
                    'csz014',  # 47
                    'csz015',  # 49
                    'csz016',  # 50
                    'csz017',  # 51
                    'csz018',  # 52
                    'csz019',  # 53
                    'csz020',  # 54
                    'csz021',  # 57
                    'csz022',  # 58
                    'csz023',  # 59
                    'csz024',  # 60 # Rerun
                    'csz025',  # 61
                    'csz026',  # 62
                    'csz027',  # 63
                    'csz028',  # 64
                    'csz029',  # 65
                    'csz030',  # 66
                    ]

SensitivityRealizations = [
                    'csz002_sd10',  # 33
                    'csz002_sd10_100bar',  # 33
                    'csz002_sd10_300bar',  # 33
                    'csz005_south',  # 35
                    'csz005_trench',  # 36
                    'csz005_zero',  # 45
                    # 'csz002_sd10_revPwave',  # 48
                    '032017',
                    '032217',
                    '032817', #Run again
                    '040617',
                    '042417',
                    '042817',
                    '050117',
                    '051117',
                    '051817',
                    '060317',
                    '061417',
                    '062217',
                    '051117',
                    '051817',
                    '081117',
                    '081817',
                    '081917',
                    '100617',
                    '082517',
]

def GetPath(Realization, Map='A'):
    global path, BroadbandLocation, SlipFilePath

    if os.name == 'nt':
        RawDataPath = '../BroadbandGeneration/RawData/%s/'%Realization
        path = 'F:/M9/DataArchive/%s/%s/' %(Realization, Map)
        BroadbandLocation = path
    else:
        # RawDataPath = '/civil/shared/lehman/marafi/Python/RawData/%s/' % Realization
        # path = '/civil/shared/lehman/marafi/Python/GenerateBroadbands/%s/%s/' % (Realization, Map)
        # BroadbandLocation = path
        RawDataPath = '../RawData/%s/' % Realization
        path = '../M9/%s/%s/' % (Realization, Map)
        BroadbandLocation = path

    FileNames = np.loadtxt(RawDataPath + '/../RealizationSlipFileName.dat', dtype=str, delimiter=',')
    for i in range(len(FileNames)):
        if FileNames[i,0] == Realization:
            SourceFile = FileNames[i,1]

    SlipFilePath = RawDataPath + '%s'%(SourceFile)

def GetDeterministicTimeSeries(Lat, Lon, Realization):
    GetPath(Realization)

    SWCornerUTM = [4467300, 100080]
    SWCornerLatLong = [40.26059706792827, -127.70217428430801]

    import utm
    utmcoord = utm.from_latlon(Lat, Lon, 10)[:2]
    Easting, Northing = utmcoord[0 ] - SWCornerUTM[1], utmcoord[1 ] -SWCornerUTM[0]  # these are relative Easting and Northings to the SW corner

    # Rounding Function
    def round_to(n ,precision):
        correction = 0.5 if n >= 0 else -0.5
        return int( n/ precision + correction) * precision

    stationid, northing, easting = np.genfromtxt(path + '/BroadbandLocations.utm', skip_header=1, dtype=str,
                                                 unpack=True)
    northing = np.array(northing, dtype=np.float)
    easting = np.array(easting, dtype=np.float)

    precision = easting[1] - easting[0]
    Easting = round_to(Easting, precision)
    Northing = round_to(Northing, precision)

    # Get File Name
    for i in range(len(northing)):
        y = round_to(northing[i], precision)
        x = round_to(easting[i], precision)
        if Easting == x and Northing == y:
            Name = stationid[i]
            #             print i
            break
        if i == len(northing) - 1:
            print('Syn file not found')

    try:
        Syn = np.loadtxt(path + 'Deterministic/%s' % (Name))
    except:
        print('error, rs or ds file not found')
        return None

    class Output():
        def __init__(self):
            self.time = Syn[:, 0]
            dt = Syn[1, 0] - Syn[0, 0]
            self.dt = dt
            self.ag_X = np.gradient(Syn[:, 2], dt) / 9.80
            self.ag_Y = np.gradient(Syn[:, 1], dt) / 9.80

            self.LatLon = utm.to_latlon(x + SWCornerUTM[1], y + SWCornerUTM[0], 10, 'T')[:2]

    return Output()

def PlotResponseSpectra(Lat, Long, Title, Realization):
    GetPath(Realization)

    Det = GetDeterministicTimeSeries(Lat, Long)
    Syn = GetSyn(Lat, Long)

    import matplotlib.pyplot as plt
    import numpy as np

    periods = np.exp(np.linspace(np.log(0.1), np.log(10), 50))

    import GMHelper
    SaDet = []
    SaSyn = []
    for t in periods:
        u, v, a = GMHelper.FindSa(Det.ag_X, Det.dt, t, 0.05)
        wn = (2. * np.pi) / t
        SaX = u * wn ** 2.0
        u, v, a = GMHelper.FindSa(Det.ag_Y, Det.dt, t, 0.05)
        SaY = u * wn ** 2.0
        SaDet.append(np.sqrt(SaX * SaY))

        u, v, a = GMHelper.FindSa(Syn.ag_X, Syn.dt, t, 0.05)
        wn = (2. * np.pi) / t
        SaX = u * wn ** 2.0
        u, v, a = GMHelper.FindSa(Syn.ag_Y, Syn.dt, t, 0.05)
        SaY = u * wn ** 2.0
        SaSyn.append(np.sqrt(SaX * SaY))

    plt.figure(figsize=(3.5, 3.5))

    plt.title(Title)
    plt.plot(periods, SaDet, color='#b0b0b0', linewidth=1.5, label='Det.')
    plt.plot(periods, SaSyn, color='#000000', linewidth=1.5, label='Syn')
    plt.ylabel('$S_a$, g')
    plt.xlabel('$T_n$, s')

    plt.legend()

    plt.xlim([0, 10])
    plt.ylim([0, 1.0])

    plt.savefig('Figures/ResponseSpectra_%s.png' % Title)
    plt.show()

def GetSyn(Lat, Lon, Realization, Map='A'):
    GetPath(Realization, Map)

    SWCornerUTM = [4467300, 100080]
    SWCornerLatLong = [40.26059706792827, -127.70217428430801]

    import utm
    utmcoord = utm.from_latlon(Lat, Lon, 10)[:2]
    Easting, Northing = utmcoord[0] - SWCornerUTM[1], utmcoord[1] - SWCornerUTM[0]  # these are relative Easting and Northings to the SW corner

    # Rounding Function
    def round_to(n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int(n / precision + correction) * precision

    stationid, northing, easting = np.genfromtxt(path + '/BroadBandLocations.utm',
                                                 skip_header=1,
                                                 dtype=str,
                                                 unpack=True)
    northing = np.array(northing, dtype=np.float)
    easting = np.array(easting, dtype=np.float)

    precision = easting[1] - easting[0]
    Easting = round_to(Easting, precision)
    Northing = round_to(Northing, precision)

    # Get File Name
    for i in range(len(northing)):
        y = round_to(northing[i], precision)
        x = round_to(easting[i], precision)
        if Easting == x and Northing == y:
            Name = stationid[i]
            #             print i
            break
        if i == len(northing) - 1:
            print('Syn file not found')

    try:
        Syn = np.loadtxt(path + '%s/%s.syn' % (Name[0:3], Name))
    except:
        print('error, rs or ds file not found')
        return None

    class Output():
        def __init__(self):
            self.time = Syn[:, 0]
            dt = Syn[1, 0] - Syn[0, 0]
            self.dt = dt
            self.ag_X = Syn[:, 3] / 980.
            self.ag_Y = Syn[:, 2] / 980.

            self.Name = Name
            self.LatLon = utm.to_latlon(x + SWCornerUTM[1], y + SWCornerUTM[0], 10, 'T')[:2]

    return Output()

def PlotTimeHistory(Lat, Long, Title, Realization):
    GetPath(Realization)

    Syn = GetSyn(Lat, Long)

    import matplotlib.pyplot as plt
    import numpy as np

    dt = Syn.time[1] - Syn.time[0]

    MaxT = 300 / dt

    time = np.array(list(range(int(MaxT)))) * dt

    padzeros = np.zeros(int(MaxT)).tolist()
    GMData = list(Syn.ag_X[:])

    plt.figure(figsize=(6.5, 3.5))

    ax = plt.axes()
    ax.xaxis.set_visible(False)
    ax = plt.axes()
    ax.yaxis.set_visible(False)
    ax.set_frame_on(False)

    plt.title(Title)
    plt.plot(time, GMData, color='#000000')
    plt.ylabel('$a_g$, g')

    plt.xlim([0, 300])
    plt.ylim([-0.6, 0.6])

    plt.savefig('Figures/M9_TimeHistory_Specto_%s.png' % Title)
    plt.show()

def GetIMs(Easting, Northing, Realization):
    GetPath(Realization)
    #Rounding Function
    def round_to(n,precision):
        correction = 0.5 if n >= 0 else -0.5
        return int( n/precision+correction ) * precision

    f = open(BroadbandLocation+'Locations.utm')
    precision = 1000
    Easting = round_to(Easting,precision)
    Northing = round_to(Northing,precision)

    #Get File Name
    for line in f.readlines():
        line = line.split()
        y = round_to(float(line[1]),precision)
        x = round_to(float(line[2]),precision)
        if Easting == x and Northing == y:
            Name = line[0]

    import numpy as np
    try:
        RS = np.loadtxt(BroadbandLocation+'%s/RS_(%s).dat'%(Name[0:3],Name))
        Ds = np.loadtxt(BroadbandLocation+'%s/Ds_(%s).dat'%(Name[0:3],Name))
    except:
        print('error, rs or ds file not found')
        return None

    class Output():
        def __init__(self):
            self.Periods = RS[:,0]
            self.SaX = RS[:,1]
            self.SaY = RS[:,2]
            self.DsX595 = Ds[0]
            self.DsY595 = Ds[1]
            self.DsX575 = Ds[2]
            self.DsY575 = Ds[3]

    return Output()

def GetPoints(X1, Y1, Radius=2000, GridSpacing=1000):
    # No of points includes the Start and End Point
    # GridSpacing = 1000
    Xs = np.arange(0,Radius*2+1,GridSpacing)-Radius
    Ys = np.arange(0,Radius*2+1,GridSpacing)-Radius
    Coordinates = []
    for i in range(len(Xs)):
        for j in range(len(Ys)):
            if (Xs[i]**2.+Ys[j]**2.)**.5 <= Radius:
                Coordinates.append([X1+Xs[i],Y1+Ys[j]])
    return Coordinates

def GetXrayFile():
    import xarray as xray
    ## Loading Cascadia File NetCDF
    Cascadia = xray.open_dataset(path + 'Xarray.nc')
    return Cascadia

def GetCutOffTime(Name, Realization, MapFolder):
    GetPath(Realization, MapFolder)

    import sys
    sys.path.append('../BroadbandGeneration/')
    import removeInsta_clean

    cutoff = removeInsta_clean.main(path + 'Deterministic/%s' % (Name))
    if cutoff == 0:
        cutoff = 400

    return cutoff

############################################# Main ####################################################################

