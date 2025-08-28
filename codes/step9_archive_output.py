# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 14:10:27 2021

@author: judithg
"""

# Archiving the output.mat

import os, shutil
import glob

def archive_output(now):
# function to save the swan output.mat file to the archive folder
    # Get the directory of this script and build absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)  # Parent directory (tailored-report-tv)
    
    dirname = os.path.join(base_dir, 'archives', now.strftime("%Y%m%d%H"))
    if os.path.exists(dirname):
        print('exists')
    else:
        os.makedirs(dirname, 0o775)
        
    inun_dir = os.path.join(base_dir, 'inundation', 'Figures')
    #shutil.copy(inun_dir, dirname)
    if os.path.exists(inun_dir):
        for file in glob.glob(os.path.join(inun_dir,"*.png")):
            shutil.copy2(file,dirname)
    
    flood_risk_dir = os.path.join(base_dir, 'inundation', 'Flood_risk')
    if os.path.exists(flood_risk_dir):
        for file in glob.glob(os.path.join(flood_risk_dir,"*.csv")):
            shutil.copy2(file,dirname)
    
    floutname = os.path.join(dirname, 'output.mat')
    fout_name = os.path.join(base_dir, 'runs', now.strftime("%Y%m%d%H"), 'output.mat')
    try:
        shutil.copy(fout_name, floutname)
    except PermissionError as e:
        print(f"Warning: Could not copy output.mat to archives due to permissions: {e}")
        print(f"Source file exists at: {fout_name}")
    except FileNotFoundError as e:
        print(f"Warning: Source output.mat file not found: {fout_name}")
    print('done')
    #ends
    return()
    
