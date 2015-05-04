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
startDate = "2003-01-01" #YYYY-MM-DD
endDate   = "2010-12-31" #YYYY-MM-DD

# input netcdf file:
input_netcdf = {}
input_netcdf['file_name']        = ""
input_netcdf['variable_name']    = ""
input_netcdf['clone_file']       = ""
input_netcdf['cell_resolution']  = 5./60.
# cell area (m2) for the input netcdf file
input_netcdf['cell_area']        = ""

# output netcdf file:
output_netcdf = {}
output_netcdf['folder']          = ""
output_netcdf['file_name']       = ""
output_netcdf['variable_name']   = ""
# cell size/length/resolution (arc-degree) for the output netcdf file 
output_netcdf['cell_resolution'] = ""

output_netcdf['format']    = ""
output_netcdf['format']    = ""
output_netcdf['attribute'] = ""


# output netcdf attributes
startDate = "2003-01-01" #YYYY-MM-DD
endDate   = "2010-12-31" #YYYY-MM-DD


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
