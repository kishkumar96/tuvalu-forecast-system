# Tuvalu Forecast System - Developer Quick Reference

## Essential Commands

```bash
# Build development image with live code editing support
cd /media/judith/Big_Booty1/Tuvalu_Forecast/tailored-report-tv
docker build -f Dockerfile.simple-working -t tuvalu-forecast-dev .

# Run with LIVE CODE EDITING (changes on host reflect immediately in container)
docker run \
  -v $(pwd)/codes:/app/codes \
  -v $(pwd)/tmp:/app/tmp \
  -v $(pwd)/Regional_Output:/app/Regional_Output \
  -v /media:/media \
  -ti --rm \
  tuvalu-forecast-dev

# Alternative: Mount entire workspace  
docker run -v $(pwd):/workspace -v /media:/media -ti --rm tuvalu-forecast-dev

# Run production system with conda environment
conda activate Tuvalu_EWS_new && python codes/step1_download_NCEP.py

# Run with Docker compose for full orchestration
docker-compose -f docker-compose.working.yml up

# Ultra-fast build for quick testing
./ultrafast-build.sh && docker run -ti --rm tuvalu-forecast-ultrafast

# Production build with credentials
./build-with-credentials.sh
docker run -v /media:/media -ti --rm tuvalu-forecast-production
```

## 🔥 Live Development Workflow

1. **Edit files on host** using VS Code, vim, nano, or any editor
2. **Changes sync automatically** to container via volume mounts
3. **Test immediately** in container without rebuilding
4. **When satisfied**, rebuild production image for deployment

## Key Files for Development

### Core Processing Scripts
- `codes/step1_download_NCEP.py` - NCEP atmospheric data download
- `codes/step2_download_CMEMS_copernicus_marine_client.py` - Sea level anomaly data
- `codes/step3_gen_tide_TPOX9_last_TMD.py` - Tidal forcing generation
- `codes/step4_gen_Inverted_Barometer.py` - Barometric pressure forcing
- `codes/step5_make_wave_forcing.py` - Wave boundary conditions
- `codes/step6_make_wind_forcing.py` - Wind forcing fields
- `codes/step7_run_SWAN.py` - SWAN spectral wave model execution
- `codes/step8_postprocess_output.py` - Output post-processing
- `codes/step9_make_flood_risk.py` - Flood risk assessment
- `codes/step10_run_XBeach.py` - XBeach coastal model
- `codes/step11_run_SFINCS.py` - SFINCS storm surge model
- `codes/step12_postprocess_SFINCS.py` - SFINCS post-processing

### Configuration Files
- `.env` - Development environment variables
- `.env.production` - Production configuration
- `.env.ultrafast` - Fast deployment configuration
- `requirements_working.txt` - Python dependencies
- `docker-compose.yml` - Main orchestration
- `docker-compose.working.yml` - Development setup
- `docker-compose.ultrafast-final.yml` - Fast deployment

### Model Configuration
- `extras/tuvalu/swan/` - SWAN model configuration
- `extras/tuvalu/sfincs/` - SFINCS model setup
- `extras/tuvalu/xbeach/` - XBeach model configuration
- `persistent_data/` - Model grids and bathymetry

### Executable Tools
- `executables/toolsUI-5.4.1.jar` - GRIB to NetCDF conversion
- `executables/swan.exe` - SWAN wave model
- `executables/sfincs` - SFINCS storm surge model
- `executables/xbeach` - XBeach coastal model

## Environment Management

### Conda Environment (Recommended)
```bash
# Activate the main environment
conda activate Tuvalu_EWS_new

# Install additional packages
conda install -n Tuvalu_EWS_new package_name

# Export environment
conda env export -n Tuvalu_EWS_new > environment.yml

# Create environment from file
conda env create -f environment.yml
```

### Virtual Environment (Alternative)
```bash
# Activate pip environment
source tuvalu_ews_pip/bin/activate

# Install packages
pip install -r requirements_working.txt

# Add new packages
pip install package_name
pip freeze > requirements_working.txt
```

## Common Development Tasks

### Add New Processing Step
1. Create `codes/stepN_description.py` following the existing pattern
2. Add imports and functions to main orchestration script
3. Update environment files if needed
4. Test with development Docker setup
5. Update production builds

### Add New Region/Location
1. Create `extras/new_location/` directory structure
2. Add model configuration files (swan/, sfincs/, xbeach/)
3. Update coordinate bounds in step1_download_NCEP.py
4. Modify model execution scripts for new location
5. Test full workflow

### Debug Processing Issues
```bash
# Check logs in real-time
tail -f logs/tuvalu_forecast.log

# Validate conda environment
conda list -n Tuvalu_EWS_new

# Check Docker container logs
docker logs container_name

# Verify data files exist
ls -la tmp/
ls -la Regional_tmp/
ls -la Regional_Output/

# Check model execution
grep "NORMAL END" logs/swan.log
grep "SFINCS finished" logs/sfincs.log
```

### Performance Monitoring
```bash
# Monitor system resources
./health_check.sh

# Check forecast timing
./efficiency_monitor.sh

# Validate output files
ncdump -h Regional_Output/latest_forecast.nc

# Test specific steps
./deploy.sh --step 1 --debug
./deploy.sh --steps 7 8 9 --verbose
```

## Docker Development Patterns

### Multi-Stage Development
```bash
# Development build (includes dev tools)
docker build -f Dockerfile.simple-working -t tuvalu-dev .

# Production build (optimized)
docker build -f Dockerfile -t tuvalu-prod .

# Ultra-fast build (minimal for testing)
docker build -f Dockerfile.ultrafast -t tuvalu-fast .

# Credentials build (with secure access)
docker build -f Dockerfile.credentials -t tuvalu-secure .
```

### Volume Mounting Strategies
```bash
# Mount code for live editing
-v $(pwd)/codes:/app/codes

# Mount data directories
-v $(pwd)/tmp:/app/tmp
-v $(pwd)/Regional_Output:/app/Regional_Output

# Mount external data sources
-v /media:/media

# Mount persistent model data
-v $(pwd)/persistent_data:/app/persistent_data
```

## Testing & Validation

### Unit Testing
```bash
# Run test suite
python -m pytest tests/

# Test specific components
python -m pytest tests/test_download.py
python -m pytest tests/test_models.py

# Coverage report
python -m pytest --cov=codes tests/
```

### Integration Testing
```bash
# Test complete workflow
./run-forecast.sh --test

# Test individual steps
./deploy.sh --step 1 --dry-run
./deploy.sh --step 7 --validate

# Performance testing
./deploy.sh --benchmark
```

### Output Validation
```bash
# Check NetCDF structure
ncdump -h Regional_Output/TuvaluForecast_YYYYMMDDHH.nc

# Verify SWAN completion
grep "SWAN terminated" logs/swan.log

# Validate SFINCS output
python codes/validate_sfincs_output.py

# Check flood risk maps
python codes/validate_flood_risk.py
```

## System Architecture Overview

```
Input Data → Pre-processing → Models → Post-processing → Output
    ↓             ↓             ↓          ↓              ↓
  NCEP GFS     Steps 1-6       SWAN    Steps 8-9      NetCDF
  CMEMS        (Python)       SFINCS   (Python)      Regional
  TPXO10       Scripts        XBeach   Scripts        Reports
  Copernicus                                          Flood Maps
```

## File Organization

```
tailored-report-tv/
├── codes/                  # Processing scripts (Steps 1-12)
├── tmp/                   # Temporary processing files
├── Regional_tmp/          # Regional temporary data
├── Regional_Output/       # Final forecast outputs  
├── logs/                  # System and model logs
├── extras/               # Model configurations
├── persistent_data/      # Static model data
├── executables/         # Model binaries and tools
├── tests/               # Test suite
├── Hall_Reports/        # Archive of forecast reports
└── archives/            # Historical forecast data
```

## Quick Debugging Reference

### Common Issues
1. **Java classpath error**: Check `executables/toolsUI-5.4.1.jar` path
2. **Download failures**: Verify internet connectivity and NCEP server status
3. **Model crashes**: Check input file formats and coordinate bounds
4. **Docker build fails**: Verify base image and dependency availability
5. **Permission errors**: Ensure proper volume mounting and user permissions

### Useful Commands
```bash
# Quick health check
./health_check.sh

# Rebuild everything
./smart-build.sh

# Emergency cleanup
./cleanup-ultrafast.sh

# Monitor in real-time
watch -n 5 'ls -la tmp/ && df -h'
```
