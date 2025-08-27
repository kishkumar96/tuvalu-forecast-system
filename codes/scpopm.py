import subprocess

# Running a simple Linux command (e.g., 'ls')
result = subprocess.run("scp -r /home/divesha/data/TUV/tailored-report-tv/Hall_Reports/2024073018 divesha@opmdata.gem.spc.int:/var/www/html/file",shell=True, capture_output=True, text=True)
