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
        DynamicModel.__init__(self)           # 

        self.input_netcdf = input_netcdf
        self.output_netcdf = output_netcdf 
        self.tmpDir = tmpDir
        self.modelTime = modelTime

        # resampling factor: ratio between output and input resolutions
        self.resample_factor = vos.getMapAttributes(self.output_netcdf["cell_resolution"])/\
                               vos.getMapAttributes(self.input_netcdf["cell_area"],'cellsize')

        # input clone properties
        
        
        
        # clone map 
        if self.resample_factor > 1.0
            # get the unique ids for the output resolution
            pcr.setclone(self.input_netcd["cell_area"])
            
            
            
            # all pcraster calculations are performed at the input resolution
            pcr.setclone(self.input_netcd["cell_area"])
            
            self.resample_factor = round(self.resample_factor)
            
        else:
            # all pcraster calculations are performed at the output resolution
        self.clone_map = pcr.boolean(1)


        
        # cell area (m2)
        self.cell_area = vos.readPCRmapClone(\
                        self.input_files["model_cell_area"],\
                        self.input_files["model_cell_area"],\
                        self.tmpDir)
        
        
        # unique ids for upscaling to one degree resolution (grace resolution)
        self.one_degree_id = pcr.nominal(\
                             vos.readPCRmapClone(\
                            self.input_files["one_degree_id"],\
                            self.input_files["model_cell_area"],\
                            self.tmpDir))
        
        # object for reporting at coarse resolution (i.e. one arc degree - grace resolution)
        self.output = OutputNetcdf(self.input_files["one_degree_id"], self.input_files["model_cell_area"])       
        # preparing the netcdf file at coarse resolution:
        self.output.createNetCDF(self.output_files['one_degree_tws']['model'], "pcrglobwb_tws","m")
        #
        # edit some attributes:
        attributeDictionary = {}
        attributeDictionary['description']      = "One degree resolution total water storage (tws), upscaled from PCR-GLOBWB result. "
        self.output.changeAtrribute(self.output_files['one_degree_tws']['model'],\
                                    attributeDictionary)                       
        
    def initial(self): 
        pass

    def dynamic(self):
        
        # re-calculate model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # processing / calculating only at the last day of the month:
        if self.modelTime.endMonth == True:
        
            #~ # open totalWaterStorageThickness (unit: m, monthly average values) 
            #~ value_at_5min = vos.netcdf2PCRobjClone(\
                            #~ self.input_files["model_total_water_storage"],\
                            #~ "total_thickness_of_water_storage",\
                            #~ str(self.modelTime.fulldate), useDoy = "end-month")
            
            # open totalWaterStorageThickness (unit: m, monthly average values) 
            value_at_5min = vos.netcdf2PCRobjClone(\
                            self.input_files["model_total_water_storage"],\
                            self.input_files["model_total_water_storage_variable_name"],\
                            str(self.modelTime.fulldate), useDoy = "end-month")

            # upscale to one degree resolution
            value_at_1deg_but_5min_cell = \
                            vos.getValDivZero(\
                            pcr.areatotal(self.cell_area*value_at_5min,\
                                                         self.one_degree_id),\
                            pcr.areatotal(self.cell_area,self.one_degree_id),
                            vos.smallNumber)
            
            # resample from 5 arc minute cells to one degree cells
            value_at_1deg = vos.regridToCoarse(\
                            pcr.pcr2numpy(value_at_1deg_but_5min_cell,vos.MV),self.resample_factor,"max",vos.MV)
            #
            # reporting
            timestepPCR = self.modelTime.timeStepPCR
            timeStamp = datetime.datetime(self.modelTime.year,\
                                          self.modelTime.month,\
                                          self.modelTime.day,0)
            # write it to netcdf 
            self.output.data2NetCDF(self.output_files['one_degree_tws']['model'],\
                                    "pcrglobwb_tws",\
                                    value_at_1deg,\
                                    timeStamp)
