M9 Project - Broadband Web Service Documentation
=======
####Disclaimer of Liability
_Neither the University of Washington, nor the USGS, nor the National Science Foundation, nor any of their employees, contractors, or subcontractors, make any warranty, express or implied, nor assume any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, data and tools provided.  Users of this information, data and tools are responsible for assessing their accuracy and proper use_.


This web service enables users to download simulated broadband ground motions across the Pacific Northwest for multiple realizations of an magnitude-9 earthquake due to the Cascadia Subduction Zone. More information on the simulations can be [here](https://doi.org/10.1785/0120180034). Broadband ground motions can be downlodeded using:

- [Site latitude and longitude (in JSON format)](/service1)

- [Site Name (in JSON format)](/service2)

- [Site latitude and longitude (in CSV format)](/service3)

## Get broadbands using site name (in JSON format).

### Requested Parameters
_Required Parameters:_
 
#### StationName
Specify the Station Name. Example: ```A11923```

_Optional Parameters:_

#### Unprocessed
Specify whether or not the broadbands should be unprocessed. Note that you can not specify Response Spectra calculations with unprocessed broadbands. Example: ```True``` or ```False```

#### ResponseSpectra
Specify whether or not the spectral accelerations should be calculated and return. Example: ```True``` or ```False```

#### ClosestDistanceToRupture
Specify whether or not the closest distance to rupture should be calculated and return. Example: ```True``` or ```False```

### Output
*Web service response*
JSON is organized by realization where each record contains the following fields:

#### Realization
    realization id

#### StationCode
    Unique station identifier

#### Timestep
    Time step of acceleration history in seconds

#### CutOffTime
    Time where the numerical instability occurs. If motions are processed then the acceleration history is ...
    
#### AccelerationHistory-EW
    Acceleration history in the east-west direction (in units of g)
    
#### AccelerationHistory-NS
    Acceleration history in the north-south direction (in units of g)
    
#### AccelerationHistory-Vert
    Acceleration history in the down-up direction (in units of g)
    
#### SpectralAcceleration-NS
    Spectral accelerations in the north-south direction (in units of g)

#### SpectralAcceleration-NS
    Spectral accelerations in the north-south direction (in units of g)
    
#### Period
    Periods of spectral accelerations (in seconds)

#### ClosestDistanceToRupture
    Closest distance to fault rupture plane (in km)
    
    
### Example 
#### Request
```
https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionFromStationName?StationName=A11923
```

To download the JSON script as *.json* file:

```
curl "https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionFromStationName?StationName=A11923" --output broadband.json
```

