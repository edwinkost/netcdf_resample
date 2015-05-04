#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# pcraster dynamic framework is used:
from pcraster.framework import DynamicFramework

# classes used in this script
from dynamic_resample_framework import ResampleFramework

# time object
from currTimeStep import ModelTime

# utility module:
import virtualOS as vos

# starting and end dates
startDate = "1958-01-01" #YYYY-MM-DD
endDate   = "2010-12-31" #YYYY-MM-DD

# input netcdf file:
input_netcdf = {}
input_netcdf['folder']           = "/scratch/edwin/05min_runs_results/2015_04_27/non_natural_2015_04_27/global/netcdf/"
input_netcdf['file_name']        = "totalEvaporation_monthAvg_output.nc"
input_netcdf['file_name']        = input_netcdf['folder']+"/"+input_netcdf['file_name']
input_netcdf['variable_name']    = "total_evaporation"
input_netcdf['clone_file']       = "/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
input_netcdf['cell_resolution']  = 5./60.
# cell area (m2) for the input netcdf file:
input_netcdf['cell_area']        = "/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"

# output netcdf file:
output_netcdf = {}
# cell size/length/resolution (arc-degree) for the output netcdf file 
output_netcdf['cell_resolution'] = 30./60.
output_netcdf['folder']          = "/scratch/edwin/05min_runs_results/2015_04_27/non_natural_2015_04_27/global/analysis/30min_upscaled"
output_netcdf['file_name']       = "totalEvaporation_monthAvg_output_30min_upscaled_from_5min.nc"
output_netcdf['file_name']       = output_netcdf['folder']+"/"+output_netcdf['file_name']
output_netcdf['variable_name']   = "total_evaporation"
output_netcdf['variable_unit']   = "m.day-1"
#
output_netcdf['format']    = "NETCDF4"
output_netcdf['zlib']      = True
output_netcdf['netcdf_attribute'] = {}
output_netcdf['netcdf_attribute']['institution'] = "Department of Physical Geography, Utrecht University" 
output_netcdf['netcdf_attribute']['title'      ] = "PCR-GLOBWB output"
output_netcdf['netcdf_attribute']['source'     ] = "test version (by Edwin H. Sutanudjaja)" 
output_netcdf['netcdf_attribute']['history'    ] = "None"
output_netcdf['netcdf_attribute']['references' ] = "None"
output_netcdf['netcdf_attribute']['description'] = "None"
output_netcdf['netcdf_attribute']['comment'    ] = "Note that this 30 arc-min field is upscaled from 5 arc-min field."

# make an output folder
try:
    os.makedirs(output_netcdf['folder'])
except:
    os.system('rm -r '+str(output_netcdf['folder'])+"/*")

# make a temporary folder 
tmpDir = output_netcdf['folder']+"/"+"tmp/"
try:
    os.makedirs(tmpDir)
except:
    os.system('rm -r '+str(output_netcdf['folder'])+"/tmp/*")

def main():
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate)
    
    # resample netcdf
    resampleModel = ResampleFramework(input_netcdf,\
                                      output_netcdf,\
                                      modelTime,\
                                      tmpDir)
    dynamic_framework = DynamicFramework(resampleModel, modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()
                                      

if __name__ == '__main__':
    sys.exit(main())
