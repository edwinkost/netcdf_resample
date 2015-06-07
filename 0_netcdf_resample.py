#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

import numpy as np

# pcraster dynamic framework is used:
from pcraster.framework import DynamicFramework

# classes used in this script
from dynamic_resample_framework import ResampleFramework

# time object
from currTimeStep import ModelTime

# utility module:
import virtualOS as vos

# starting and end dates
startDate = "2008-01-01" # "1990-01-01" #YYYY-MM-DD
endDate   = "2013-12-31" # "2014-10-31" #YYYY-MM-DD

# input netcdf file:
input_netcdf = {}
input_netcdf['folder']           = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/netcdf_latlon/2.5min/temperature/"
input_netcdf['file_name']        = "temperature_efas_rhine-meuse.nc"
input_netcdf['file_name']        = input_netcdf['folder']+"/"+input_netcdf['file_name']
input_netcdf['variable_name']    = "temperature"
input_netcdf['clone_file']       = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/cell_area_maps/RhineMeuseCellsize2.5min.map"
input_netcdf['cell_resolution']  = 2.5/60.
# cell area (m2) for the input netcdf file:
input_netcdf['cell_area']        = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/cell_area_maps/RhineMeuseCellsize2.5min.map"

# output netcdf file:
output_netcdf = {}
# cell size/length/resolution (arc-degree) for the output netcdf file 
output_netcdf['cell_resolution'] = 5./60.
output_netcdf['folder']          = "/scratch/edwin/input/forcing/hyperhydro_wg1/EFAS/netcdf_latlon/5min/temperature/"
output_netcdf['file_name']       = "temperature_efas_rhine-meuse_2008to2013.nc"
output_netcdf['file_name']       = output_netcdf['folder']+"/"+output_netcdf['file_name']
output_netcdf['variable_name']   = input_netcdf['variable_name']
output_netcdf['variable_unit']   = "m.day-1"
#
# input and output resolutions at arc minute unit rounded to one value behind the decimal
input_cell_size_in_arc_minutes  = np.round(input_netcdf['cell_resolution']  * 60.0, 1) 
output_cell_size_in_arc_minutes = np.round(output_netcdf['cell_resolution'] * 60.0, 1) 
important_information  = "The dataset was first resampled to "+str(input_cell_size_in_arc_minutes)+" arc minute resolution "
important_information += "and then aggregated to "+str(input_cell_size_in_arc_minutes)+" arc minute resolution."  
#
output_netcdf['format']    = "NETCDF3_CLASSIC"
output_netcdf['zlib']      = False
output_netcdf['netcdf_attribute'] = {}
output_netcdf['netcdf_attribute']['institution'] = "European Commission - JRC and Department of Physical Geography, Utrecht University"
output_netcdf['netcdf_attribute']['title'      ] = "EFAS-Meteo 5km for Rhine-Meuse - resampled to "+str(output_cell_size_in_arc_minutes)+" arc minute resolution. "
output_netcdf['netcdf_attribute']['source'     ] = "5km Gridded Meteo Database (C) European Commission - JRDC, 2014"
output_netcdf['netcdf_attribute']['history'    ] = "The data were provided by Ad de Roo (ad.de-roo@jrc.ec.europa.eu) on 19 November 2014 and then converted by Edwin H. Sutanudjaja (E.H.Sutanudjaja@uu.nl) to netcdf. "
output_netcdf['netcdf_attribute']['history'    ] += important_information 
output_netcdf['netcdf_attribute']['references' ] = "Ntegeka et al., 2013. EFAS-Meteo: A European daily high-resolution gridded meteorological data set. JRC Technical Reports. doi: 10.2788/51262"
output_netcdf['netcdf_attribute']['comment'    ] = "Please use this dataset only for Hyper-Hydro test bed experiments. " 
output_netcdf['netcdf_attribute']['comment'    ] += "For using it and publishing it, please acknowledge its source: 5km Gridded Meteo Database (C) European Commission - JRDC, 2014 and its reference: Ntegeka et al., 2013 (doi: 10.2788/51262). "
output_netcdf['netcdf_attribute']['comment'    ] += "The original data provided by JRC are in European ETRS projection, 5km grid; http://en.wikipedia.org/wiki/European_grid. "
output_netcdf['netcdf_attribute']['comment'    ] += important_information
output_netcdf['netcdf_attribute']['description'] = "None"

# make an output folder
cleanOutputFolder = False
try:
    os.makedirs(output_netcdf['folder'])
except:
    if cleanOutputFolder: os.system('rm -r '+str(output_netcdf['folder'])+"/*")

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
