#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import time
import re
import subprocess
import netCDF4 as nc
import numpy as np
import virtualOS as vos

# the following dictionary is needed to avoid open and closing files
filecache = dict()

class OutputNetcdf():
    
    def __init__(self, output_netcdf):
        		
        # latitudes and longitudes
        cellLength = output_netcdf['cellsize']
        deltaLat = cellLength
        latMax = output_netcdf['yUL'] - deltaLat/2.
        latMin = output_netcdf['yUL'] - deltaLat*output_netcdf['rows'] + deltaLat/2.
        deltaLon = cellLength
        lonMin = output_netcdf['xUL'] + deltaLon/2.
        lonMax = output_netcdf['xUL'] + deltaLon*output_netcdf['cols'] - deltaLon/2.
        self.latitudes  = np.arange(latMax,latMin-deltaLat,-deltaLat)
        self.longitudes = np.arange(lonMin,lonMax+deltaLon,deltaLon)

        # netcdf format and zlib setup
        self.format = output_netcdf['format']
        self.zlib   = output_netcdf['zlib'] 
        
        # netcdf attributes
        self.attributeDictionary = {}
        self.attributeDictionary['institution'] = output_netcdf['netcdf_attribute']['institution']
        self.attributeDictionary['title'      ] = output_netcdf['netcdf_attribute']['title'      ]
        self.attributeDictionary['source'     ] = output_netcdf['netcdf_attribute']['source'     ]
        self.attributeDictionary['history'    ] = output_netcdf['netcdf_attribute']['history'    ]
        self.attributeDictionary['references' ] = output_netcdf['netcdf_attribute']['references' ]
        self.attributeDictionary['description'] = output_netcdf['netcdf_attribute']['description']
        self.attributeDictionary['comment'    ] = output_netcdf['netcdf_attribute']['comment'    ]
        
    def createNetCDF(self, ncFileName, varName, varUnits, longName=None):

        rootgrp = nc.Dataset(ncFileName,'w',format= self.format)

        #-create dimensions - time is unlimited, others are fixed
        rootgrp.createDimension('time',None)
        rootgrp.createDimension('lat',len(self.latitudes))
        rootgrp.createDimension('lon',len(self.longitudes))

        date_time = rootgrp.createVariable('time','f4',('time',))
        date_time.standard_name = 'time'
        date_time.long_name = 'Days since 1901-01-01'

        date_time.units = 'Days since 1901-01-01' 
        date_time.calendar = 'standard'

        lat= rootgrp.createVariable('lat','f4',('lat',))
        lat.long_name = 'latitude'
        lat.units = 'degrees_north'
        lat.standard_name = 'latitude'

        lon= rootgrp.createVariable('lon','f4',('lon',))
        lon.standard_name = 'longitude'
        lon.long_name = 'longitude'
        lon.units = 'degrees_east'

        lat[:]= self.latitudes
        lon[:]= self.longitudes

        shortVarName = varName
        longVarName  = varName
        if longName != None: longVarName = longName

        var = rootgrp.createVariable(shortVarName,'f4',('time','lat','lon',),fill_value=vos.MV,zlib=self.zlib)
        var.standard_name = varName
        var.long_name = longVarName
        var.units = varUnits

        attributeDictionary = self.attributeDictionary
        for k, v in attributeDictionary.items(): setattr(rootgrp,k,v)

        rootgrp.sync()
        rootgrp.close()

    def changeAtrribute(self, ncFileName, attributeDictionary, closeFile = False):

        if ncFileName in filecache.keys():
            #~ print "Cached: ", ncFileName
            rootgrp = filecache[ncFileName]
        else:
            #~ print "New: ", ncFileName
            rootgrp = nc.Dataset(ncFileName,'a')
            filecache[ncFileName] = rootgrp

        for k, v in attributeDictionary.items(): setattr(rootgrp,k,v)

        rootgrp.sync()
        if closeFile == True: rootgrp.close()

    def addNewVariable(self, ncFileName, varName, varUnits, longName=None, closeFile = False):

        if ncFileName in filecache.keys():
            #~ print "Cached: ", ncFileName
            rootgrp = filecache[ncFileName]
        else:
            #~ print "New: ", ncFileName
            rootgrp = nc.Dataset(ncFileName,'a')
            filecache[ncFileName] = rootgrp

        shortVarName = varName

        var = rootgrp.createVariable(shortVarName,'f4',('time','lat','lon',) ,fill_value=vos.MV,zlib=self.zlib)
        var.standard_name = varName
        var.long_name = varName
        var.units = varUnits

        rootgrp.sync()
        if closeFile == True: rootgrp.close()

    def data2NetCDF(self, ncFileName, shortVarName, varField, timeStamp, posCnt = None, closeFile = False):

        if ncFileName in filecache.keys():
            #~ print "Cached: ", ncFileName
            rootgrp = filecache[ncFileName]
        else:
            #~ print "New: ", ncFileName
            rootgrp = nc.Dataset(ncFileName,'a')
            filecache[ncFileName] = rootgrp

        date_time = rootgrp.variables['time']
        if posCnt == None: posCnt = len(date_time)
        date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)

        rootgrp.variables[shortVarName][posCnt,:,:] = varField

        rootgrp.sync()
        if closeFile == True: rootgrp.close()

    def dataList2NetCDF(self, ncFileName, shortVarNameList, varFieldList, timeStamp, posCnt = None, closeFile = False):

        if ncFileName in filecache.keys():
            #~ print "Cached: ", ncFileName
            rootgrp = filecache[ncFileName]
        else:
            #~ print "New: ", ncFileName
            rootgrp = nc.Dataset(ncFileName,'a')
            filecache[ncFileName] = rootgrp

        date_time = rootgrp.variables['time']
        if posCnt == None: posCnt = len(date_time)

        for shortVarName in shortVarNameList:
            date_time[posCnt] = nc.date2num(timeStamp,date_time.units,date_time.calendar)
            rootgrp.variables[shortVarName][posCnt,:,:] = varFieldList[shortVarName]

        rootgrp.sync()
        if closeFile == True: rootgrp.close()

    def close(self, ncFileName):

        if ncFileName in filecache.keys():
            #~ print "Cached: ", ncFileName
            rootgrp = filecache[ncFileName]
        else:
            #~ print "New: ", ncFileName
            rootgrp = nc.Dataset(ncFileName,'a')
            filecache[ncFileName] = rootgrp

        # closing the file 
        rootgrp.close()

        # remove ncFilename from filecache
        if ncFileName in filecache.keys(): filecache.pop(ncFileName, None)
