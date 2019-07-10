M9 Project - Broadband Web Service Documentation
=======
####Disclaimer of Liability
_Neither the University of Washington, nor the USGS, nor the National Science Foundation, nor any of their employees, contractors, or subcontractors, make any warranty, express or implied, nor assume any legal liability or responsibility for the accuracy, completeness, or usefulness of any information, data and tools provided.  Users of this information, data and tools are responsible for assessing their accuracy and proper use_.


This web service enables users to download simulated broadband ground motions across the Pacific Northwest for multiple realizations of an magnitude-9 earthquake due to the Cascadia Subduction Zone. More information on the simulations can be [here](https://doi.org/10.1785/0120180034). Broadband ground motions can be downlodeded using:

- [Site latitude and longitude (in JSON format)](/service1)

- [Site Name (in JSON format)](/service2)

- [Site latitude and longitude (in CSV format)](/service3)

## Get broadbands using site latitude and longitude(in CSV format).

### Requested Parameters
_Required Parameters:_

#### Latitude
Specify the latitude of the site location. Example: ```47.6```

#### Longitude
Specify the longitude of the site location. Example: ```-122.3```

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

