M9 Project - Broadband Web Service Documentation
=======
The M9 simulations download tool is a web service that enables users to download simulated broadband ground motions, response spectra, and metadata at locations throughout the Pacific Northwest for multiple realizations of a magnitude-9 earthquake due to a full rupture of the Cascadia subduction zone.

The site locations available for download are documented here.  Broadband ground motions can be downloaded for a particular site name or the closest site to a particular latitude and longitude. The output can be provided in either JSON or CSV formats:

-[Downloads by Site Coordinates (in JSON format)](/service1)

-[Downloads by Site Name (in JSON format)](/service2)

-[Downloads by Site Coordinates (in CSV format)](/service3)

-[Downloads by Site Name (in CSV format)](/service4)

#### Acknowledgments
The simulations were the result of a collaboration between researchers at the University of Washington and United States Geological Survey (USGS) with the financial support from the National Science Foundation ([Award Number 1331412](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1331412)). This web service tool was developed by [Nasser A. Marafi](https://orcid.org/0000-0002-3622-1839) with the support of the USGS ([USGS External Grant G19AP00049](https://earthquake.usgs.gov/cfusion/external_grants/research.cfm)).

#### Disclaimer of Liability
Neither the University of Washington, nor the USGS, nor the National Science Foundation, nor any of their employees, contractors, or subcontractors, make any warranty, express or implied, nor assume any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, data and tools provided. Users of this information, data, and tools are responsible for assessing their accuracy and proper use.

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

#### SensitivityRuns
Download the sensitivity runs from Wirth et al. 2018 instead of the Frankel et al. 2018 (logic tree runs). Example: ```True``` or ```False```

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

