# 🐳 TUVALU FORECAST SYSTEM - DOCKER DEPLOYMENT

## Method 1: Using the Management Script (Recommended)

The easiest way to run the Tuvalu forecast system in Docker:

```bash
# Build the Docker image (first time only)
./tuvalu-manager.sh build-docker

# Run forecast with Docker
./tuvalu-manager.sh docker

# Or start interactive shell
./tuvalu-manager.sh shell
```

## Method 2: Direct Docker Command

If you prefer to run Docker directly (equivalent to your Niue approach):

### Basic Docker Run Command:
```bash
docker run --rm -it \
  --user $(id -u):$(id -g) \
  --env-file .env \
  -v "$(pwd):/TuvaluForecast" \
  -v "$(pwd)/runs:/TuvaluForecast/runs" \
  -v "$(pwd)/logs:/TuvaluForecast/logs" \
  -v "$(pwd)/tmp:/TuvaluForecast/tmp" \
  -v "$(pwd)/archives:/TuvaluForecast/archives" \
  -v "$(pwd)/Regional_Output:/TuvaluForecast/Regional_Output" \
  -v "$(pwd)/.copernicusmarine:/root/.copernicusmarine" \
  -w /TuvaluForecast/codes \
  tuvalu-forecast:latest \
  python main_run_operational.py
```

### For Your Specific Use Case (Similar to Niue):
If you want to mount external data directories like in your Niue command:

```bash
docker run --rm -it \
  --user $(id -u):$(id -g) \
  --env-file /path/to/tuvalu-forecast-system/.env \
  -v /path/to/tuvalu-forecast-system:/TuvaluForecast \
  -v /data/forecast-model/TUV/runs:/TuvaluForecast/runs \
  -v /data/forecast-model/TUV/archives:/TuvaluForecast/archives \
  -v /data/forecast-model/TUV/logs:/TuvaluForecast/logs \
  -v /data/ocean_portal/datasets/model/country/spc/forecast/hourly/TUV:/data \
  -w /TuvaluForecast/codes \
  tuvalu-forecast:latest \
  python main_run_operational.py
```

## Method 3: Docker Compose (Production Recommended)

Use the provided docker-compose.yml:

```bash
# Simple setup
docker-compose -f docker-compose.simple.yml up

# Full setup  
docker-compose up
```

## Key Differences from Niue System:

1. **Image Name**: `tuvalu-forecast:latest` (not `niue-forecast:latest`)
2. **Working Directory**: `/TuvaluForecast` (not `/NiueForecast`) 
3. **Main Script**: `codes/main_run_operational.py` (same path structure)
4. **Volume Mounts**: More volumes needed for Tuvalu system:
   - `runs/` - For forecast outputs
   - `archives/` - For archived results  
   - `logs/` - For logging
   - `tmp/` - For temporary files
   - `Regional_Output/` - For regional data
   - `.copernicusmarine/` - For marine data credentials

## Environment Variables Required:

Make sure your `.env` file contains:
```bash
# Copernicus Marine credentials
COPERNICUS_MARINE_USERNAME=your_username
COPERNICUS_MARINE_PASSWORD=your_password

# Email configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

## Test the Setup:

```bash
# Test the Docker setup
cd /media/judith/Big_Booty1/Tuvalu_Forecast/tailored-report-tv
./tuvalu-manager.sh status
./tuvalu-manager.sh shell

# Inside the container, test individual steps:
python step1_download_NCEP.py
python step2_download_CMEMS.py
# ... etc
```

## Troubleshooting:

1. **Permission Issues**: Make sure to use `--user $(id -u):$(id -g)`
2. **Missing Data**: Check that all volume mounts point to correct paths
3. **Network Issues**: Ensure firewall allows Docker to access external APIs
4. **Memory Issues**: The SWAN model needs significant RAM (8GB+ recommended)
