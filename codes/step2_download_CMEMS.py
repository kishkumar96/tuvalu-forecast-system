# -*- coding: utf-8 -*-
"""
Created on Thu May  6 17:47:05 2021

@author: anujd
"""
import os
import datetime as dt
import netCDF4 as nc
from netCDF4 import date2num, Dataset, num2date
import numpy as np
import pandas as pd
import copernicusmarine

def read_sla_csv(fpath):
    df = pd.read_csv(fpath)
    atoll = df['atoll'].tolist()
    sla_lon = df['lon'].tolist()
    sla_lat = df['lat'].tolist()
    sla = df['sla_offset'].tolist()
    return(atoll,sla_lon,sla_lat,sla)



###############################################################################
def download_CMEMS(now):  
    print(now)
    
    # Ensure Copernicus Marine credentials are available
    username = os.environ.get('COPERNICUSMARINE_SERVICE_USERNAME')
    password = os.environ.get('COPERNICUSMARINE_SERVICE_PASSWORD')
    
    if not username or not password:
        raise ValueError("Copernicus Marine credentials not found in environment variables. "
                        "Please set COPERNICUSMARINE_SERVICE_USERNAME and COPERNICUSMARINE_SERVICE_PASSWORD")
    
    print(f"Using Copernicus Marine credentials for user: {username}")
    
    DATASET_ID = "cmems_mod_glo_phy_anfc_0.083deg_PT1H-m"
    print('Downloading Sea Level Anomaly data from http://nrt.cmems-du.eu')
    folder_tmp ='../tmp/' 
    now = now - dt.timedelta(2)# NCEP needs at least 3 hours to upload their forecast from UTC00
    # now = now.replace(hour=0,minute=0,second=0,microsecond=0)
    then = now+dt.timedelta(days=9.5,hours=1)
    
    sla_fpath = '../extras/Tuvalu_island_gauge_locations.csv'
    atoll_list, sla_lon_list, sla_lat_list,sla_offset_list = read_sla_csv(sla_fpath)

    for atoll,sla_lon,sla_lat,sla_off in zip(atoll_list,sla_lon_list,sla_lat_list,sla_offset_list):
        print('anuj')
        import time
        time.sleep(60)
        copernicusmarine.subset(
            dataset_id=DATASET_ID,
            username=username,
            password=password,
            service = 'timeseries',
            variables=['zos'],
            minimum_longitude=sla_lon-0.0005,
            maximum_longitude=sla_lon+0.0005,
            minimum_latitude=sla_lat-0.001,
            maximum_latitude=sla_lat+0.001,
            start_datetime= now.strftime('%Y-%m-%dT%H:%M:%S'),
            end_datetime= then.strftime('%Y-%m-%d %H:%M:%S'),
            minimum_depth=0.49402499198913574,
            maximum_depth=.49402499198913574,
            #force_download= True,
            #overwrite_output_data =True,
            output_filename = 'sla_'+atoll+'.nc',
            output_directory = folder_tmp
        )
        output_directory = folder_tmp
        # The following block is intentionally commented out and has no effect:
        # os.system('python -m motuclient --motu http://nrt.cmems-du.eu/motu-web/Motu\
        #                       --service-id GLOBAL_ANALYSISFORECAST_PHY_001_024-TDS --product-id cmems_mod_glo_phy_anfc_0.083deg_PT1H-m\
        #                       --longitude-min %(lon_min)s --longitude-max %(lon_max)s --latitude-min %(lat_min)s --latitude-max %(lat_max)s\
        #                       --date-min '"'%(ini)s'"' --date-max '"'%(end)s'"'\
        #                       --depth-min 0.493 --depth-max 0.4942 --variable thetao --variable uo --variable vo --variable zos\
        #                       --out-dir %(folder)s --out-name sla_%(island)s.nc\
        #                       --user mwandres --pwd nZp9d@zwPVi73hn' %{"lon_min":(sla_lon-0.001),"lon_max":(sla_lon+0.001),"lat_min":(sla_lat-0.001),"lat_max":(sla_lat+0.001),"ini":now.strftime('%Y-%m-%d %H:%M:%S') ,"end":then.strftime('%Y-%m-%d %H:%M:%S'),"folder":folder_tmp,"island":atoll})
                              
        nc_fname = folder_tmp  + ('sla_%s.nc' % atoll)
        ncc = Dataset(nc_fname)    
        time_var_nc = ncc.variables['time']  
        time_or = num2date(time_var_nc[:], time_var_nc.units, time_var_nc.calendar)
        time_str=[time_or[i].strftime('%Y-%b-%d %H:%M') for i in range(0,len(time_or))]
        Time=[dt.datetime.strptime(time_str[i],'%Y-%b-%d %H:%M') for i in range(0,len(time_str))]
        sla = (np.array(ncc['zos'])- sla_off)*100# This offset comes from comparing DUACS altimetry with the model, it has been aplied to transform Sea Surface Height to Sea Level Anomaly (height from the MSL) [1993-2019 monthly mean]
        #sla = (np.array(ncc['zos'][:,0,0])- sla_off)*100
        sla=sla.squeeze()
                
        fn = folder_tmp  + ('sla_hourly_%s.nc' % atoll)
        try:
            os.remove(fn)
        except FileNotFoundError:
            pass
        ds = Dataset(fn, 'w', format='NETCDF4')
        time_dim = ds.createDimension('time', None)
        times = ds.createVariable('time', 'f8', ('time',))
        times.units = 'hours since 1950-01-01 00:00:00'
        times.calendar = 'gregorian'
        SLA = ds.createVariable('SLA', 'f4', dimensions=('time',))
        SLA.units = 'cm'
        times[:] = [date2num(x, units=times.units, calendar=times.calendar) - 0.5 for x in Time]
        ds.close()
        
        print('sea level anomaly stored as ' + fn)
