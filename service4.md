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

## Get broadbands using site latitude and longitude(in CSV format).

### Requested Parameters
_Required Parameters:_

#### Latitude
Specify the latitude of the site location. Example: ```47.6```

#### Longitude
Specify the longitude of the site location. Example: ```-122.3```

#### SensitivityRuns
Download the sensitivity runs from Wirth et al. 2018 instead of the Frankel et al. 2018 (logic tree runs). Example: ```True``` or ```False```

### Output
*Web service response*
The csv file is comma delimited. The first column corresponds to the time (in seconds), remaining columns are organized by realization. Each realization set consists of three columns that correspond to the east-west acceleration history, north-south acceleration history, and vertical acceleration history. All acceleration units are in g.
    
### Example 
#### Request
```
https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionInCSVFromLatLon?Latitude=47.6062&Longitude=-122.3321
```

To download CSV with acceleration history for a particular location:

```
curl "https://m9-broadband-download-rwqks6gbba-uc.a.run.app/getMotionInCSVFromLatLon?Latitude=47.6062&Longitude=-122.3321" --output broadband.csv
```

