#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import calendar

import pcraster as pcr
from pcraster.framework import DynamicModel

from outputNetcdf import OutputNetcdf
import virtualOS as vos

class ResampleFramework(DynamicModel):

    def __init__(self, input_netcdf,\
                       output_netcdf,\
                       modelTime,\
                       tmpDir = "/dev/shm/"):
        DynamicModel.__init__(self) 

        self.input_netcdf = input_netcdf
        self.output_netcdf = output_netcdf 
        self.tmpDir = tmpDir
        self.modelTime = modelTime

        # a dictionary contains input clone properties (based on the input netcdf file)
        self.input_clone = vos.netcdfCloneAttributes(self.input_netcdf['file_name'],\
                                                     round(self.input_netcdf['cell_resolution']*60.),\
                                                     True)

        # resampling factor: ratio between output and input resolutions
        self.resample_factor = self.output_netcdf["cell_resolution"]/\
                                self.input_netcdf['cell_resolution']
        
        print self.resample_factor
        
        # clone map 
        if self.resample_factor > 1.0: # upscaling

            # the resample factor must be a rounded value without decimal
            self.resample_factor = round(self.resample_factor)
            
            # output clone properties
            self.output_netcdf['rows'    ] = int(round(float(self.input_clone['rows'])/float(self.resample_factor))) 
            self.output_netcdf['cols'    ] = int(round(float(self.input_clone['cols'])/float(self.resample_factor)))
            self.output_netcdf['cellsize'] = self.output_netcdf["cell_resolution"]
            self.output_netcdf['xUL'     ] = self.input_clone['xUL']
            self.output_netcdf['yUL'     ] = self.input_clone['yUL']

            # get the unique ids for the output resolution
            # - use the clone for the output resolution (only for a temporary purpose)
            pcr.setclone(self.output_netcdf['rows'    ],
                         self.output_netcdf['cols'    ],
                         self.output_netcdf['cellsize'],
                         self.output_netcdf['xUL'     ],
                         self.output_netcdf['yUL'     ])
            # - unique_ids in a numpy object
            cell_unique_ids = pcr.pcr2numpy(pcr.scalar(pcr.uniqueid(pcr.boolean(1.))),vos.MV)

            # the remaining pcraster calculations are performed at the input resolution
            pcr.setclone(self.input_clone['rows'    ],
                         self.input_clone['cols'    ],
                         self.input_clone['cellsize'],
                         self.input_clone['xUL'     ],
                         self.input_clone['yUL'     ])
            
            # clone map file 
            self.clone_map_file = self.input_netcdf['clone_file']
            
            # cell unique ids in a pcraster object
            self.unique_ids = pcr.nominal(pcr.numpy2pcr(pcr.Scalar,
                              vos.regridData2FinerGrid(self.resample_factor,cell_unique_ids, vos.MV), vos.MV))

            # cell area (m2)
            self.cell_area = vos.readPCRmapClone(\
                             self.input_netcdf["cell_area"],\
                             self.clone_map_file,\
                             self.tmpDir)
            
        else: # downscaling / resampling to smaller cell length

            # all pcraster calculations are performed at the output resolution
            pcr.setclone(self.output_netcdf['rows'    ],
                         self.output_netcdf['cols'    ],
                         self.output_netcdf['cellsize'],
                         self.output_netcdf['xUL'     ],
                         self.output_netcdf['yUL'     ])

            # clone map file
            self.clone_map_file = self.output_netcdf['clone_file']
        
        # an object for netcdf reporting
        self.output = OutputNetcdf(self.output_netcdf)       
        
        # preparing the netcdf file at coarse resolution:
        self.output.createNetCDF(self.output_netcdf['file_name'],
                                 self.output_netcdf['variable_name'],
                                 self.output_netcdf['variable_unit'])
        
    def initial(self): 
        pass

    def dynamic(self):
        
        # update model time using the current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # reading
        data_available = True
        if data_available:
            input_value = vos.netcdf2PCRobjClone(ncFile  = self.input_netcdf['file_name'],
                                                 varName = self.input_netcdf['variable_name'],
                                                 dateInput = str(self.modelTime.fulldate),
                                                 useDoy = None,
                                                 cloneMapFileName = self.clone_map_file)
            data_available = True  
        
        else:
            print "No values are available for this date: "+str(self.modelTime)
            data_available = False 
        
        if data_available: output_value = input_value

        # upscaling
        if data_available and self.resample_factor > 1.0:
        
            # upscaling using cell area
            output_value_in_pcraster = \
                            vos.getValDivZero(\
                            pcr.areatotal(output_value*self.cell_area, self.unique_ids),\
                            pcr.areatotal(self.cell_area, self.unique_ids), vos.smallNumber)
            
            # resample to the output clone resolution 
            output_value = vos.regridToCoarse(pcr.pcr2numpy(output_value_in_pcraster, vos.MV),
                                              self.resample_factor, "max", vos.MV)

        # reporting
        if data_available:

            # time stamp 
            timestepPCR = self.modelTime.timeStepPCR
            timeStamp = datetime.datetime(self.modelTime.year,\
                                          self.modelTime.month,\
                                          self.modelTime.day,0)
            # write to netcdf 
            self.output.data2NetCDF(self.output_netcdf['file_name'],\
                                    self.output_netcdf['variable_name'],\
                                    output_value,\
                                    timeStamp)

        # closing the file at the end of
        if self.modelTime.isLastTimeStep(): self.output.close(self.output_netcdf['file_name'])

