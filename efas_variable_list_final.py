#!/usr/bin/python
# -*- coding: utf-8 -*-

# dictionary for netcdf file names, variable names and units: 
netcdf_short_name = {}
netcdf_unit       = {}
netcdf_long_name  = {}
description       = {}

# pr Daily precipitation (mm) between 6 UTC on the day specified and 6 UTC on the next day 
efas_variable_name = "pr"
netcdf_short_name[efas_variable_name] = 'precipitation'
netcdf_unit[efas_variable_name]       = 'mm.day-1'
netcdf_long_name[efas_variable_name]  = 'daily_precipitation'
description[efas_variable_name]       = 'Daily precipitation between 6 UTC on the day specified and 6 UTC on the next day.'

# tn Daily minimum temperature (°C) between 18 UTC and 6 UTC (i.e. during the preceding night) at 2m 
efas_variable_name = "tn"
netcdf_short_name[efas_variable_name] = 'minimum_temperature'
netcdf_unit[efas_variable_name]       = 'degrees Celcius'
netcdf_long_name[efas_variable_name]  = 'daily_minimum_temperature'
description[efas_variable_name]       = 'Daily minimum temperature between 18 UTC and 6 UTC (i.e. during the preceding night) at 2m.'

# tx Daily maximum temperature (°C) between 6 UTC and 18 UTC (i.e. during daytime) at 2m 
efas_variable_name = "tx"
netcdf_short_name[efas_variable_name] = 'maximum_temperature'
netcdf_unit[efas_variable_name]       = 'degrees Celcius'
netcdf_long_name[efas_variable_name]  = 'daily_maximum_remperature'
description[efas_variable_name]       = 'Daily maximum temperature between 6 UTC and 18 UTC (i.e. during daytime) at 2m.'

# ta Daily mean temperature (°C) is calculated using ta=(tx+tn)/2 
efas_variable_name = "ta"
netcdf_short_name[efas_variable_name] = 'temperature'
netcdf_unit[efas_variable_name]       = 'degrees Celcius'
netcdf_long_name[efas_variable_name]  = 'daily_mean_precipitation'
description[efas_variable_name]       = 'Daily mean temperature (ta) ; calculated using ta = (tx+tn)/2 ; with tx and ta are the maximum and minimum temperature values.'

# ws Mean daily wind speed at 10 metres (m/s) calculated from 3-hourly observations (0-24 UTC) 
efas_variable_name = "ws"
netcdf_short_name[efas_variable_name] = 'wind_speed'
netcdf_unit[efas_variable_name]       = 'm.s-1'
netcdf_long_name[efas_variable_name]  = 'daily_mean_wind_speed'
description[efas_variable_name]       = 'Mean daily wind speed at 10 metres (m/s) calculated from 3-hourly observations (0-24 UTC).'

# pd Mean daily vapour pressure (hPa) 
efas_variable_name = "pd"
netcdf_short_name[efas_variable_name] = 'vapour_pressure'
netcdf_unit[efas_variable_name]       = 'hPa'
netcdf_long_name[efas_variable_name]  = 'daily_mean_vapour_pressure'
description[efas_variable_name]       = 'Mean daily vapour pressure (hPa).'

# cr or rg Calculated radiation (KJ/m2/day) 
#~ efas_variable_name = "cr"
efas_variable_name = "rg"
netcdf_short_name[efas_variable_name] = 'calculated_radiation'
netcdf_unit[efas_variable_name]       = 'KJ/m2/day'
netcdf_long_name[efas_variable_name]  = 'calculated_radiation'
description[efas_variable_name]       = 'Calculated radiation (KJ/m2/day), see the reference about its method.'

# e0 Penman potential evaporation from a free water surface (mm/day) 
efas_variable_name = "e0"
netcdf_short_name[efas_variable_name] = 'water_potential_evaporation'
netcdf_unit[efas_variable_name]       = 'mm.day-1'
netcdf_long_name[efas_variable_name]  = 'potential_evaporation_from_a_free_water_surface'
description[efas_variable_name]       = 'Penman potential evaporation from a free water surface (mm/day).'

# et Penman potential transpiration from a crop canopy (mm/day) 
efas_variable_name = "et"
netcdf_short_name[efas_variable_name] = 'crop_potential_transpiration'
netcdf_unit[efas_variable_name]       = 'mm.day-1'
netcdf_long_name[efas_variable_name]  = 'potential_transpiration_from_a_crop_canopy'
description[efas_variable_name]       = 'Penman potential transpiration from a crop canopy (mm/day).'

# es Penman potential evaporation from a moist bare soil surface (mm/day)
efas_variable_name = "es"
netcdf_short_name[efas_variable_name] = 'bare_soil_potential_evaporation'
netcdf_unit[efas_variable_name]       = 'mm.day-1'
netcdf_long_name[efas_variable_name]  = 'potential_evaporation_from_a_moist_bare_soil_surface'
description[efas_variable_name]       = 'Penman potential evaporation from a moist bare soil surface (mm/day).'
