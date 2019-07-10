M9 Project - Broadband Web Service Documentation
=======
####Disclaimer of Liability
_Neither the University of Washington, nor the USGS, nor the National Science Foundation, nor any of their employees, contractors, or subcontractors, make any warranty, express or implied, nor assume any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, data and tools provided.  Users of this information, data and tools are responsible for assessing their accuracy and proper use_.

This web service enables users to download simulated broadband ground motions across the Pacific Northwest for multiple realizations of an magnitude-9 earthquake due to the Cascadia Subduction Zone. More information on the simulations can be [here](https://doi.org/10.1785/0120180034). Broadband ground motions can be downlodeded using:

- [Site latitude and longitude (in JSON format)](/service1)

- [Site Name (in JSON format)](/service2)

- [Site latitude and longitude (in CSV format)](/service3)

## Get broadbands for a site latitude and longitude (in JSON format).

### Requested Parameters
_Required Parameters:_

#### Latitude
Specify the latitude of the site location. Example: ```47.6```

#### Longitude
Specify the longitude of the site location. Example: ```-122.3```

_Optional Parameters:_

#### Unprocessed
Specify whether or not the broadbands should be unprocessed. Note that you can not specify Response Spectra calculations with unprocessed broadbands. Example: ```True``` or ```False```

#### ResponseSpectra
Specify whether or not the spectral accelerations should be calculated and return. Example: ```True``` or ```False```

#### GetDistanceToRupture
Specify whether or not the closest distance to rupture should be calculated and return. Example: ```True``` or ```False```

### Output
*Web service response*
JSON is organized by realization where each record contains the following fields:

#### Realization
    realization id

#### StationCode
    Unique station identifier

#### DistanceToClosestSite
    Closest distance from the specified latitude and longitude to the station latitude and longitude

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
    
#### SpetralAcceleration-EW
    Spectral accelerations in the east-west direction (in units of g)

#### SpetralAcceleration-NS
    Spectral accelerations in the north-south direction (in units of g)

#### SpetralAcceleration-NS
    Spectral accelerations in the north-south direction (in units of g)
    
#### Period
    Periods of spectral accelerations (in seconds)

#### CloestDistanceToRupture
    Closest distance to fault rupture plane (in km)
    
### Example 
#### Request
To get acceleration history for a particular location:

```
https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionFromLatLon?Latitude=47.6062&Longitude=-122.3321
```

To get unprocessed acceleration history for a particular location:

```
https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionFromLatLon?Latitude=47.6062&Longitude=-122.3321&Unprocessed=True
```

To get acceleration history and response spectra for a particular location:

```
https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionFromLatLon?Latitude=47.6062&Longitude=-122.3321&ResponseSpectra=True
```

To download the JSON script as *.json* file:

```
curl "https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionFromLatLon?Latitude=47.6062&Longitude=-122.3321" --output broadband.json
```

#### Response

```
[
    {
        "Realization": "csz003",
        "StationCode": "A11923",
        "DistanceToClosestSite": 0.464591,
        "TimeStep": 0.02,
        "CutOffTime": 305.60001,
        "AccelerationHistory-EW": [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            ...,
            ],
        "AccelerationHistory-NS": [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            ...,
            ],
        "AccelerationHistory-Vert": [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0,
            ...,
            ],
    },
    {
        "Realization": "csz004",
        ...
    },
    ...
]  
```
