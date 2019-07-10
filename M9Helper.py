# This includes functions which help with the m9 motions
from __future__ import absolute_import
from __future__ import print_function
import os
import numpy as np
import GMHelper
import SimM9MotionHelper


from requests_toolbelt.adapters import appengine
appengine.monkeypatch()

CLOUD_STORAGE_BUCKET = 'm9-project-bucket-west'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'M9ProjectBroadbands-412691040693.json'


def GetSynFileFromM9Folder(Realization, Latitude, Longitude, Folder='A', M9Folder='F:/M9/DataArchive/'):
    import numpy as np

    path = M9Folder + '/' + Realization + '/' + Folder + '/'

    SWCornerUTM = [4467300, 100080]
    SWCornerLatLong = [40.26059706792827, -127.70217428430801]

    import utm
    utmcoord = utm.from_latlon(Latitude, Longitude, 10)[:2]
    Easting, Northing = utmcoord[0] - SWCornerUTM[1], utmcoord[1] - SWCornerUTM[
        0]  # these are relative Easting and Northings to the SW corner

    # Rounding Function
    def round_to(n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int(n / precision + correction) * precision

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
        Syn = np.loadtxt(path + '%s/%s.syn' % (Name[0:3], Name))
    except:
        print('error, rs or ds file not found')
        return None

    # Find CutOff
    cutoffTime = SimM9MotionHelper.GetCutOffTime(Name, Realization, Folder)
    cutoffIndex = int(cutoffTime / (Syn[1, 0] - Syn[0, 0]))

    class Output():
        def __init__(self):
            self.FileName = Name
            self.time = Syn[:, 0]
            self.dt = self.time[1] - self.time[0]
            self.ag_Z = Syn[:, 1] / 980.  # convert to G
            self.ag_X = Syn[:, 3] / 980. #convert to G
            self.ag_Y = Syn[:, 2] / 980. #convert to G
            self.CutOffIndex = cutoffIndex
            self.CutOffTime = cutoffTime

            self.LatLon = utm.to_latlon(x + SWCornerUTM[1], y + SWCornerUTM[0], 10, 'T')[:2]

    return Output()

def GetSynFileFromM9FolderUsingSynFileName(Realization, SynFileName, Folder='A', M9Folder='F:/M9/DataArchive/'):
    import numpy as np

    path = M9Folder + '/' + Realization + '/' + Folder + '/'

    Name = SynFileName

    try:
        Syn = np.loadtxt(path + '%s/%s.syn' % (Name[0:3], Name))
    except:
        print('error, rs or ds file not found')
        return None

    # Find CutOff
    cutoffTime = SimM9MotionHelper.GetCutOffTime(Name, Realization, Folder)
    cutoffIndex = int(cutoffTime / (Syn[1, 0] - Syn[0, 0]))

    class Output():
        def __init__(self):
            self.FileName = Name
            self.time = Syn[:, 0]
            self.dt = self.time[1] - self.time[0]
            self.ag_Z = Syn[:, 1] / 980.  # convert to G
            self.ag_X = Syn[:, 3] / 980. #convert to G
            self.ag_Y = Syn[:, 2] / 980. #convert to G
            self.CutOffIndex = cutoffIndex
            self.CutOffTime = cutoffTime

    return Output()

def GetSynFile(SynFileName, Folder):
    import numpy as np

    if not SynFileName.endswith('.syn'):
        SynFileName += '.syn'

    try:
        Syn = np.loadtxt(Folder + SynFileName)
    except:
        print('error, file not found')
        return None

    class Output():
        def __init__(self):
            self.FileName = SynFileName
            self.time = Syn[:, 0]
            self.ag_X = Syn[:, 3] / 980. #convert to G
            self.ag_Y = Syn[:, 2] / 980. #convert to G
            self.ag_Z = Syn[:, 1] / 980.  # convert to G
            self.Dt = Syn[1,0] - Syn[0,0]

    return Output()

def GetIMs(Easting, Northing, BroadbandLocation):
    # Rounding Function
    def round_to(n, precision):
        correction = 0.5 if n >= 0 else -0.5
        return int(n / precision + correction) * precision

    f = open(BroadbandLocation[:-2] + 'A/BroadBandLocations.utm')
    precision = 1000
    Easting = round_to(Easting, precision)
    Northing = round_to(Northing, precision)

    # Get File Name
    for line in f.readlines():
        line = line.split()
        y = round_to(float(line[1]), precision)
        x = round_to(float(line[2]), precision)
        if Easting == x and Northing == y:
            Name = line[0]

    import numpy as np
    try:
        print(Name)
        RS = np.loadtxt(BroadbandLocation[:-2] + 'A/%s/RS_(%s).dat' % (Name[0:3], Name))
        Ds = np.loadtxt(BroadbandLocation[:-2] + 'A/%s/Ds_(%s).dat' % (Name[0:3], Name))
    except:
        print('error, rs or ds file not found')
        return None

    class Output():
        def __init__(self):
            self.Periods = RS[:, 0]
            self.SaX = RS[:, 1]
            self.SaY = RS[:, 2]
            self.DsX595 = Ds[0]
            self.DsY595 = Ds[1]
            self.DsX575 = Ds[2]
            self.DsY575 = Ds[3]

    return Output()

def GetIMsFromSynName(SynName, Realization, M9Folder='F:/M9/DataArchive/'):
    import numpy as np
    try:
        RS = np.loadtxt(M9Folder + '%s/%s/%s/RS_(%s).dat' % (Realization, SynName[:1], SynName[0:3], SynName))
        Ds = np.loadtxt(M9Folder + '%s/%s/%s/Ds_(%s).dat' % (Realization, SynName[:1], SynName[0:3], SynName))
    except:
        print('error, rs or ds file not found')
        return None

    class Output():
        def __init__(self):
            self.Periods = RS[:, 0]
            self.SaX = RS[:, 1]
            self.SaY = RS[:, 2]
            self.DsX595 = Ds[0]
            self.DsY595 = Ds[1]
            self.DsX575 = Ds[2]
            self.DsY575 = Ds[3]

    return Output()

def GetRotD(Periods, Realization, Latitude, Longitude,  Folder='A', M9Folder='F:/M9/DataArchive/'):
    Syn = GetSynFileFromM9Folder(Realization, Latitude, Longitude,  Folder=Folder, M9Folder=M9Folder)
    SaRotD0 = []
    SaRotD50 = []
    SaRotD100 = []
    RotD0 = []
    RotD50 = []
    RotD100 = []
    IM = GetIMsFromSynName(Syn.FileName, Realization, M9Folder)
    SaX = np.interp(Periods, IM.Periods, IM.SaX)
    SaY = np.interp(Periods, IM.Periods, IM.SaY)
    for t in Periods:
        cutoffTime = SimM9MotionHelper.GetCutOffTime(Syn.FileName, Realization, Folder)
        cutoffIndex = int(cutoffTime / Syn.dt)

        Rot = GMHelper.GetSaRotD(Syn.ag_X[:cutoffIndex], Syn.ag_Y[:cutoffIndex], Syn.dt, t, 0.05)
        SaRotD0.append(Rot.SaRotD0)
        SaRotD50.append(Rot.SaRotD50)
        SaRotD100.append(Rot.SaRotD100)
        RotD0.append(Rot.RotD0)
        RotD50.append(Rot.RotD50)
        RotD100.append(Rot.RotD100)
    class Output():
        def __init__(self):
            self.SaRotD0 = SaRotD0
            self.SaRotD50 = SaRotD50
            self.SaRotD100 = SaRotD100
            self.RotD0 = RotD0
            self.RotD50 = RotD50
            self.RotD100 = RotD100
            self.SaX = SaX
            self.SaY = SaY
            self.Periods = Periods

    return Output()

def GetRotDAtSinglePeriod(Periods, PeriodOfInterest, Realization, Latitude, Longitude,  Folder='A', M9Folder='F:/M9/DataArchive/'):
    Syn = GetSynFileFromM9Folder(Realization, Latitude, Longitude,  Folder=Folder, M9Folder=M9Folder)
    SaRotD0 = []
    SaRotD50 = []
    SaRotD100 = []
    IM = GetIMsFromSynName(Syn.FileName, Realization, M9Folder)
    SaX = np.interp(Periods, IM.Periods, IM.SaX)
    SaY = np.interp(Periods, IM.Periods, IM.SaY)

    cutoffTime = SimM9MotionHelper.GetCutOffTime(Syn.FileName, Realization, Folder)
    cutoffIndex = int(cutoffTime / Syn.dt)

    Rot = GMHelper.GetSaRotD(Syn.ag_X[:cutoffIndex], Syn.ag_Y[:cutoffIndex], Syn.dt, PeriodOfInterest, 0.05)

    for t in Periods:
        u, v, a = GMHelper.FindSa(Rot.DataRotD0, Syn.dt, t, 0.05)
        SaRotD0.append(a)
        u, v, a = GMHelper.FindSa(Rot.DataRotD50, Syn.dt, t, 0.05)
        SaRotD50.append(a)
        u, v, a = GMHelper.FindSa(Rot.DataRotD100, Syn.dt, t, 0.05)
        SaRotD100.append(a)

    class Output():
        def __init__(self):
            self.SaRotD0 = SaRotD0
            self.SaRotD50 = SaRotD50
            self.SaRotD100 = SaRotD100
            self.SaX = SaX
            self.SaY = SaY
            self.Periods = Periods

    return Output()

def GetDetFile(StationName, Realization, M9Folder = 'F:/M9/DataArchive'):
    import numpy as np

    try:
        Det = np.loadtxt(M9Folder + '/' + Realization + '/' + StationName[:1] + '/Deterministic/' + StationName)
    except:
        print('error, file not found')
        return None

    Dt = Det[1,0]-Det[0,0]
    GMDataY = np.gradient(Det[:,1],Dt)/9.81
    GMDataX = np.gradient(Det[:,2],Dt)/9.81
    GMDataZ = np.gradient(Det[:,3],Dt)/9.81

    class Output():
        def __init__(self):
            self.FileName = StationName
            self.time = Det[:, 0]
            self.ag_X = GMDataX
            self.ag_Y = GMDataY
            self.ag_Z = GMDataZ
            self.Dt = Dt

    return Output()
