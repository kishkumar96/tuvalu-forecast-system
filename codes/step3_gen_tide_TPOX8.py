# -*- coding: utf-8 -*-
"""
Created on Fri May 28 15:41:44 2021

@author: antonioh
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import netCDF4 as nc
from scipy.interpolate import interp1d
from pyTMD import io
from pyTMD import predict
import datetime as dt

def read_tpo_csv(fpath):
    """Read atoll, longitude, and latitude from a CSV file."""
    df = pd.read_csv(fpath)
    atoll = df['atoll'].tolist()
    tpo_lon = df['lon'].tolist()
    tpo_lat = df['lat'].tolist()
    return atoll, tpo_lon, tpo_lat

def gen_tide(now, configfile):
    """Generate tide forecast using TPXO8 Global Tidal Model."""
    print(
        'Generating tide from TPOX8 Global Tidal Model '
        'https://www.tpxo.net/global'
    )

    with open(configfile, encoding="utf-8") as f:
        data = json.load(f)
    location_pts_csv = data[0]['Tailored_Forecast']['forecast_locations_path']

    folder_tmp = '../tmp/'
    otis_version = 'TPXO8-atlas'
    otis_path = '../extras/TPXO8/DATA'

    tpo_fpath = location_pts_csv
    atoll_list, tpo_lon_list, tpo_lat_list = read_tpo_csv(tpo_fpath)

    for atoll, tpo_lon, tpo_lat in zip(atoll_list, tpo_lon_list, tpo_lat_list):
        print("\n", atoll, tpo_lon, tpo_lat)

        lon = tpo_lon
        lat = tpo_lat

        # NCEP needs at least 3 hours to upload their forecast from UTC00
        now1 = now - dt.timedelta(days=2)
        then = now1 + dt.timedelta(days=9.5, minutes=1)
        time_tide = mdates.drange(
            now1,
            then,
            dt.timedelta(minutes=1)
        )
        time_tide_hourly = mdates.drange(
            now1,
            then,
            dt.timedelta(hours=1)
        )
        date_time = pd.to_datetime(mdates.num2date(time_tide))
        date_time_hourly = pd.to_datetime(mdates.num2date(time_tide_hourly))

        # convert time from MJD to days relative to Jan 1, 1992 (48622 MJD)
        time_tmd = (
            time_tide
            - mdates.date2num(np.datetime64('1992-01-01T00:00:00'))
        )

        model = io.model(otis_path).elevation(otis_version)
        deltat = np.zeros_like(time_tmd)

        amp, ph, _, c = io.OTIS.extract_constants(
            np.atleast_1d([lon]),
            np.atleast_1d([lat]),
            model.grid_file,
            model.model_file,
            model.projection,
            type=model.type,
            method='spline',
            grid='OTIS'
        )

        # calculate complex phase in radians for Euler's
        cph = -1j * ph * np.pi / 180.0
        # calculate constituent oscillation
        hc = amp * np.exp(cph)

        # predict tidal elevations at time 1 and infer minor corrections
        tide = predict.time_series(
            time_tmd,
            hc,
            c,
            deltat=deltat,
            corrections=model.format
        )
        minor = predict.infer_minor(
            time_tmd,
            hc,
            c,
            deltat=deltat,
            corrections=model.format
        )
        tide.data[:] += minor.data[:]
        # convert to centimeters
        tide.data[:] *= 100.0
        f = interp1d(time_tide, tide)
        tide_hourly = f(time_tide_hourly)

        # Save netcdf with the 10 days tide forecast hourly
        fn = f"{folder_tmp}tide_hourly_{atoll}.nc"
        try:
            os.remove(fn)
        except FileNotFoundError:
            print(
                'The system cannot find the file specified, creating netcdf file'
            )
        with nc.Dataset(fn, 'w', format='NETCDF4') as ds:
            ds.createDimension('time', None)
            times = ds.createVariable('time', 'f8', ('time',))
            times.units = 'hours since 1950-01-01 00:00:00'
            times.calendar = 'gregorian'
            tide_var = ds.createVariable('tide', 'f4', ('time',))
            tide_var.units = 'cm'
            times[:] = [
                nc.date2num(
                    x,
                    units=times.units,
                    calendar=times.calendar
                )
                for x in date_time_hourly
            ]
            tide_var[:] = tide_hourly
        print(f'1 hour tides stored as {fn}')

        # Save tide forecast in netcdf in 1 minute resolution
        fn = f"{folder_tmp}tide_minute_{atoll}.nc"
        try:
            os.remove(fn)
        except FileNotFoundError:
            print(
                'The system cannot find the file specified, creating netcdf file'
            )
        with nc.Dataset(fn, 'w', format='NETCDF4') as ds:
            ds.createDimension('time', None)
            times = ds.createVariable('time', 'f8', ('time',))
            times.units = 'hours since 1950-01-01 00:00:00'
            times.calendar = 'gregorian'
            tide_var = ds.createVariable('tide', 'f4', ('time',))
            tide_var.units = 'cm'
            times[:] = [
                nc.date2num(
                    x,
                    units=times.units,
                    calendar=times.calendar
                )
                for x in date_time
            ]
            tide_var[:] = tide.data
        print(f'1 minute tides stored as {fn}')