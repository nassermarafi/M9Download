RealizationsToProcess = ['csz%03d'%x for x in range(1,34,1)] + ['csz002_sd10']
RealizationsIgnore = ['csz001', 'csz015', 'csz016', 'csz002']
LogicTreeRealizations = [x for x in RealizationsToProcess if not(x in RealizationsIgnore)]

SensitivityRealizations = \
    [
                    'csz002',
                    'csz002_sd10',  # 33
                    'csz002_sd10_100bar',  # 33
                    'csz002_sd10_300bar',  # 33
                    'csz005_south',  # 35
                    'csz005_trench',  # 36
                    'csz005_zero',  # 45
                    'csz002_sd10_revPwave',  # 48
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
                    '050117',
                    '051117',
                    '051817',
                    '081117',
                    '081817',
                    '081917',
                    '100617',
    ]

def FindClosestStationNameToLatLon(Latitude, Longitude):
    import numpy as np
    import geopy.distance
    latlon = np.loadtxt('AllLatLon.dat', dtype=[('StationCode', np.unicode_,16), ('Latitude', '<f8'), ('Longitude', '<f8')])
    Distances = []
    for i in range(len(latlon)):
        Distances.append(geopy.distance.geodesic((latlon[i][1], latlon[i][2]), (Latitude, Longitude)).km)
    return latlon[np.argmin(Distances)][0], Distances[np.argmin(Distances)]

def FindLatLonOfStation(StationName):
    import numpy as np
    import geopy.distance
    latlon = np.loadtxt('AllLatLon.dat', dtype=[('StationCode', np.unicode_,16), ('Latitude', '<f8'), ('Longitude', '<f8')])
    Distances = []
    for i in range(len(latlon)):
        if latlon[i][0] == StationName:
            return latlon[i][1], latlon[i][2]
    return None

def GetM9Motion(StationName, Unprocessed = False, GetDistanceToRupture = False, ResponseSpectra = False,
                DistanceToClosestSite = None, SensitivityRuns = False):
    import numpy as np
    Motions = []
    SigFigures = 5

    if not SensitivityRuns:
        RealizationsToProcess = LogicTreeRealizations
    else:
        RealizationsToProcess = SensitivityRealizations

    for realization in RealizationsToProcess[:]:
        print('Processing Realization %s'%realization)
        MotionInfo = {}
        MotionInfo['Realization'] = realization
        MotionInfo['StationCode'] = StationName
        if DistanceToClosestSite is not None:
            MotionInfo['DistanceToClosestSite'] = np.round(DistanceToClosestSite,SigFigures)

        # Cut Records and Make Original Length
        O = GetSynFileFromGoogleCloudUsingSynFileName(realization, StationName, StationName[:1],)

        Dt = O.dt
        CutOffTime = O.CutOffTime
        RCD = O.RCD
        MotionInfo['TimeStep'] = float(np.round(Dt,SigFigures))
        MotionInfo['CutOffTime'] = float(np.round(O.CutOffTime,SigFigures))

        Ag_X = np.zeros(len(O.ag_X))
        Ag_Y = np.zeros(len(O.ag_Y))
        Ag_Z = np.zeros(len(O.ag_Z))

        if Unprocessed:
            MotionInfo['AccelerationHistory-EW-Unprocessed'] = list(np.round(O.ag_X,SigFigures))
            MotionInfo['AccelerationHistory-NS-Unprocessed'] = list(np.round(O.ag_Y,SigFigures))
            MotionInfo['AccelerationHistory-Vert-Unprocessed'] = list(np.round(O.ag_Z,SigFigures))
            del O
        else:
            Ag_X[:O.CutOffIndex] = O.ag_X[:O.CutOffIndex]
            Ag_Y[:O.CutOffIndex] = O.ag_Y[:O.CutOffIndex]
            Ag_Z[:O.CutOffIndex] = O.ag_Z[:O.CutOffIndex]
            del O

            # Taper Records at Ends
            import SignalHelper
            Ag_X = SignalHelper.FilterSeriesInTimeDomain(Dt, Ag_X, CutOffTime).FilteredSignal
            Ag_Y = SignalHelper.FilterSeriesInTimeDomain(Dt, Ag_Y, CutOffTime).FilteredSignal
            Ag_Z = SignalHelper.FilterSeriesInTimeDomain(Dt, Ag_Z, CutOffTime).FilteredSignal

            # Zeorth Order Base Line Correct
            Ag_X = SignalHelper.RemoveResidualVelocityFromAccelerogram(Dt, Ag_X) * 980.
            Ag_Y = SignalHelper.RemoveResidualVelocityFromAccelerogram(Dt, Ag_Y) * 980.
            Ag_Z = SignalHelper.RemoveResidualVelocityFromAccelerogram(Dt, Ag_Z) * 980.

            MotionInfo['AccelerationHistory-EW'] = list(np.round(Ag_X / 980.,SigFigures))
            MotionInfo['AccelerationHistory-NS'] = list(np.round(Ag_Y / 980.,SigFigures))
            MotionInfo['AccelerationHistory-Vert'] = list(np.round(Ag_Z / 980.,SigFigures))

            if ResponseSpectra:
                import GMHelper
                sa, t = GMHelper.GetResponseSpectra(Ag_X / 980., Dt, 0.05)
                MotionInfo['SpectralAcceleration-EW'], MotionInfo['Period'] =  list(np.round(sa,SigFigures)), list(np.round(t,SigFigures))
                sa, t = GMHelper.GetResponseSpectra(Ag_Y / 980., Dt, 0.05)
                MotionInfo['SpectralAcceleration-NS'], MotionInfo['Period'] =  list(np.round(sa,SigFigures)), list(np.round(t,SigFigures))

        # Use Key File Instead
        if GetDistanceToRupture:
            # Compute RCD
            MotionInfo['ClosestDistanceToRupture'] = float(np.round(RCD,SigFigures))

        Motions.append(MotionInfo)

    return Motions

def GetLatLonFromStationID(StationID, M9Folder = 'F:/M9/DataArchive', Realization = 'csz020' ):
    import numpy as np
    dat = np.genfromtxt( M9Folder + '/' + Realization + '/' + StationID[:1] + '/BroadbandLocations.utm', skip_header=1,
                        dtype="S8,f8,f8")
    import CSZM9Helper
    for i in range(len(dat)):
        if dat[i][0].decode('ascii') == StationID:
            latlon = CSZM9Helper.ConvertUTMToLatLon(dat[i][2], dat[i][1])
            return [latlon[0], latlon[1]]

def GetFileFromGoogleCloudAsString(src):
    # if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    # # Production
    # else:
    # # Local development server

    import urllib
    url = 'https://storage.googleapis.com/m9-project-bucket-west/' + src

    import os
    if os.name == 'nt':
        import tempfile
        temp = tempfile.TemporaryFile()
        temp.close()
        urllib.request.urlretrieve(url, temp.name)
        return temp.name
    else:
        urllib.request.urlretrieve(url, '/tmp/tmp')
        return '/tmp/tmp'  # temp.name

def GetSynFileFromGoogleCloudUsingSynFileName(Realization, SynFileName, Folder='A'):
    import numpy as np
    Name = SynFileName
    def GetFileName():
        # Load Key
        KeyStr = GetFileFromGoogleCloudAsString(Realization + '/' + Folder + '/Key.npy')
        Key = np.load(KeyStr)

        # SynFileName, ModelEasting, ModelNorthing, Lat, Lon, RCD, CutOffTime, SeismogramDataFile, RowStartingSynFile, ResponseSpectraFile, RowStartingRSFile
        for i in range(len(Key)):
            if Key[i][0] == SynFileName:
                Index = Key[i][8]
                FileName = Key[i][7].replace('.dat', '.npy')
                cutoffTime = float(Key[i][6])
                RCD = float(Key[i][5])
                break
        del Key
        return Index, FileName, cutoffTime, RCD

    Index, FileName, cutoffTime, RCD = GetFileName()

    CombinedFileNameStr = GetFileFromGoogleCloudAsString(Realization + '/' + Folder + '/' + FileName)
    CombinedFileName = np.array(np.load(CombinedFileNameStr).tolist(), dtype=float)
    Syn = CombinedFileName[Index:Index + int(400 / 0.02), :]
    del CombinedFileName

    # Find CutOff
    cutoffIndex = int(cutoffTime / (Syn[1, 0] - Syn[0, 0]))

    class Output():
        def __init__(self):
            self.FileName = Name
            self.dt = Syn[1,0] - Syn[0,0]
            self.ag_Z = Syn[:, 3] / 980.  # convert to G
            self.ag_X = Syn[:, 1] / 980.  # convert to G
            self.ag_Y = Syn[:, 2] / 980.  # convert to G
            self.CutOffIndex = cutoffIndex
            self.CutOffTime = cutoffTime
            self.RCD = RCD

    return Output()
