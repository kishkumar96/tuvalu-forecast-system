# Tuvalu Forecast System - Commands Reference

## 🚀 Quick Commands Reference

This document provides a comprehensive reference of all commands and scripts available in the Tuvalu Forecast System.

---

## 🎯 Essential Commands

### Basic Deployment
```bash
# Quick start - Full forecast with conda environment
conda activate Tuvalu_EWS_new && ./deploy.sh

# Simple deployment script
./run-forecast-simple.sh

# Complete forecast workflow
./complete-forecast.sh

# Production deployment
./deploy.sh --production
```

### System Health and Status
```bash
# Comprehensive health check
./health_check.sh

# System status overview
./health_check.sh --summary

# Check specific components
./health_check.sh --component download
./health_check.sh --component models
./health_check.sh --component output
```

---

## 🐳 Docker Commands

### Docker Builds
```bash
# Production build
docker build -f Dockerfile -t tuvalu-forecast-production .
# Alternative using script
./build-production.sh

# Development build  
docker build -f Dockerfile.simple-working -t tuvalu-forecast-dev .

# Ultra-fast build for testing
docker build -f Dockerfile.ultrafast -t tuvalu-forecast-ultrafast .
# Alternative using script
./ultrafast-build.sh

# Build with credentials (secure)
docker build -f Dockerfile.credentials -t tuvalu-forecast-secure .
# Alternative using script
./build-with-credentials.sh

# Smart build (automatically selects best option)
./smart-build.sh
```

### Docker Run Commands
```bash
# Run production container
docker run -v $(pwd)/Regional_Output:/app/output \
           -v /media:/media \
           --rm tuvalu-forecast-production

# Run development container with live code editing
docker run -v $(pwd)/codes:/app/codes \
           -v $(pwd)/tmp:/app/tmp \
           -v $(pwd)/Regional_Output:/app/output \
           -v /media:/media \
           -ti --rm tuvalu-forecast-dev bash

# Run ultra-fast container for testing
docker run -ti --rm tuvalu-forecast-ultrafast

# Run with specific environment file
docker run --env-file .env.production \
           -v $(pwd)/Regional_Output:/app/output \
           --rm tuvalu-forecast-production
```

### Docker Compose
```bash
# Production deployment with compose
docker-compose -f docker-compose.yml up

# Development environment
docker-compose -f docker-compose.working.yml up

# Ultra-fast deployment
docker-compose -f docker-compose.ultrafast-final.yml up

# Background deployment
docker-compose -f docker-compose.yml up -d

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build
```

---

## 📊 Individual Step Execution

### Data Download Steps (1-6)
```bash
# Step 1: Download NCEP atmospheric data
conda activate Tuvalu_EWS_new && python codes/step1_download_NCEP.py

# Step 2: Download CMEMS sea level data  
conda activate Tuvalu_EWS_new && python codes/step2_download_CMEMS_copernicus_marine_client.py

# Step 3: Generate tidal forcing
conda activate Tuvalu_EWS_new && python codes/step3_gen_tide_TPOX9_last_TMD.py

# Step 4: Generate barometric forcing
conda activate Tuvalu_EWS_new && python codes/step4_gen_Inverted_Barometer.py

# Step 5: Create wave forcing
conda activate Tuvalu_EWS_new && python codes/step5_make_wave_forcing.py

# Step 6: Create wind forcing
conda activate Tuvalu_EWS_new && python codes/step6_make_wind_forcing.py
```

### Model Execution Steps (7-11)
```bash
# Step 7: Run SWAN wave model
conda activate Tuvalu_EWS_new && python codes/step7_run_SWAN.py

# Step 8: Process wave output
conda activate Tuvalu_EWS_new && python codes/step8_postprocess_output.py

# Step 9: Generate flood risk assessment
conda activate Tuvalu_EWS_new && python codes/step9_make_flood_risk.py

# Step 10: Run XBeach coastal model
conda activate Tuvalu_EWS_new && python codes/step10_run_XBeach.py

# Step 11: Run SFINCS storm surge model
conda activate Tuvalu_EWS_new && python codes/step11_run_SFINCS.py

# Step 12: Generate final output
conda activate Tuvalu_EWS_new && python codes/step12_postprocess_SFINCS.py
```

### Selective Step Execution
```bash
# Run specific step using deploy script
./deploy.sh --step 1
./deploy.sh --step 7
./deploy.sh --step 12

# Run multiple specific steps
./deploy.sh --steps 1 2 3
./deploy.sh --steps 7 8 9

# Resume from specific step
./deploy.sh --resume-from 7

# Skip specific steps
./deploy.sh --skip-steps 10 11
```

---

## 🔧 System Management

### Build and Setup Scripts
```bash
# Build production image
./build-production.sh

# Build with credentials
./build-with-credentials.sh

# Ultra-fast build for testing
./ultrafast-build.sh

# Simple working build
./build-working-java.sh

# Smart build selection
./smart-build.sh

# Build credentials layer
./build-credentials-layer.sh
```

### Automation and Scheduling
```bash
# Setup 6-hour automation
./6h_scheduler.sh

# Manage forecast cycles
./cycle_manager.sh

# Setup scheduling system
./schedule_setup.sh

# Tuvalu system manager
./tuvalu-manager.sh start
./tuvalu-manager.sh stop
./tuvalu-manager.sh restart
./tuvalu-manager.sh status
```

### Cleanup and Maintenance
```bash
# Ultra-fast cleanup of temporary files
./cleanup-ultrafast.sh

# Docker cleanup (remove unused images/containers)
./cleanup-docker-clutter.sh

# Fix SWAN model issues
./fix-swan.sh

# General cleanup
find tmp/ -type f -mtime +7 -delete
find Regional_tmp/ -type f -mtime +7 -delete
```

---

## 🧪 Testing and Validation

### Test Execution
```bash
# Run complete test suite
python -m pytest tests/

# Run specific test categories
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/system/

# Run with coverage report
python -m pytest --cov=codes tests/

# Run tests with verbose output
python -m pytest -v tests/

# Run specific test file
python -m pytest tests/test_download.py
python -m pytest tests/test_models.py
```

### Validation Commands
```bash
# Validate environment setup
./health_check.sh --validate-env

# Validate output files
python codes/validate_output.py Regional_Output/

# Check NetCDF file structure
ncdump -h Regional_Output/TuvaluForecast_*.nc

# Validate model execution logs
grep "NORMAL END" logs/swan.log
grep "SFINCS finished" logs/sfincs.log

# Validate data ranges
python codes/validate_data_ranges.py
```

### Performance Testing
```bash
# Benchmark system performance
./deploy.sh --benchmark

# Monitor resource usage during execution
./deploy.sh --monitor

# Time individual steps
time python codes/step1_download_NCEP.py
time python codes/step7_run_SWAN.py

# Profile Python execution
python -m cProfile -o profile.stats codes/step1_download_NCEP.py
```

---

## 🌐 Environment Management

### Conda Environment
```bash
# Activate environment
conda activate Tuvalu_EWS_new

# List installed packages
conda list

# Update environment
conda env update -f environment.yml

# Export current environment
conda env export > environment_backup.yml

# Create new environment
conda env create -f environment.yml

# Remove environment
conda env remove -n Tuvalu_EWS_new
```

### Virtual Environment (Alternative)
```bash
# Activate virtual environment
source tuvalu_ews_pip/bin/activate

# Install packages
pip install -r requirements_working.txt

# Update packages
pip install --upgrade -r requirements_working.txt

# List installed packages
pip list

# Generate requirements
pip freeze > requirements_current.txt
```

### Environment Configuration
```bash
# Use development environment
cp .env.example .env
# Edit .env with your settings

# Use production environment
cp .env.production .env.production.local
# Edit .env.production.local with production settings

# Use ultra-fast environment
cp .env.ultrafast .env.ultrafast.local
# Edit for ultra-fast testing
```

---

## 📊 Monitoring and Logging

### Log Management
```bash
# View real-time logs
tail -f logs/tuvalu_forecast.log
tail -f logs/swan.log
tail -f logs/sfincs.log

# Search logs for errors
grep -i error logs/*.log
grep -i "failed\|exception" logs/*.log

# View recent log entries
tail -n 100 logs/tuvalu_forecast.log

# Archive old logs
tar -czf logs_$(date +%Y%m%d).tar.gz logs/
```

### System Monitoring
```bash
# Monitor system resources
htop
iotop
watch -n 5 'df -h && free -h'

# Check disk usage
du -sh */
df -h

# Monitor network activity
nethogs
iftop

# Process monitoring
ps aux | grep python
ps aux | grep java
```

### Health Monitoring
```bash
# Comprehensive health check
./health_check.sh

# Component-specific checks
./health_check.sh --check-downloads
./health_check.sh --check-models
./health_check.sh --check-storage

# Docker health check
./docker-healthcheck.sh

# Monitor forecast execution
watch -n 30 './health_check.sh --brief'
```

---

## 🔄 Hybrid and Advanced Operations

### Hybrid Mode (Native + Docker)
```bash
# Hybrid execution script
./hybrid-run.sh

# Run specific steps in Docker while others native
./hybrid-run.sh --docker-steps 1,2,3 --native-steps 7,8,9

# Use Docker for preprocessing, native for models
./hybrid-run.sh --mode preprocess-docker
```

### Advanced Docker Operations
```bash
# Multi-stage build
docker build --target development -t tuvalu-dev .
docker build --target production -t tuvalu-prod .

# Build for specific architecture
docker buildx build --platform linux/amd64,linux/arm64 .

# Export Docker image
docker save tuvalu-forecast-production > tuvalu-forecast.tar

# Import Docker image
docker load < tuvalu-forecast.tar

# Inspect container
docker inspect tuvalu-forecast-production
docker history tuvalu-forecast-production
```

### Debugging Commands
```bash
# Debug mode execution
./deploy.sh --debug

# Verbose mode
./deploy.sh --verbose

# Dry run (validate without execution)
./deploy.sh --dry-run

# Interactive debugging
docker run -ti --rm tuvalu-forecast-dev bash
# Inside container:
cd /app && python -i codes/step1_download_NCEP.py
```

---

## 📁 File and Data Management

### Data Organization
```bash
# Check data directory structure
tree Regional_Output/
tree Regional_tmp/
tree tmp/

# List recent forecast outputs
ls -lat Regional_Output/

# Check file sizes
du -sh Regional_Output/*
du -sh tmp/*

# Compress old data
tar -czf archive_$(date +%Y%m%d).tar.gz runs/older_runs/

# Clean temporary files
rm -f tmp/*.grib2
rm -f tmp/*.tmp
rm -f Regional_tmp/*.tmp
```

### Output Management
```bash
# Copy latest forecast
cp Regional_Output/TuvaluForecast_latest.nc /path/to/destination/

# Create symlink to latest
ln -sf Regional_Output/TuvaluForecast_$(date +%Y%m%d%H).nc latest_forecast.nc

# Validate NetCDF files
for file in Regional_Output/*.nc; do
    ncdump -h "$file" > /dev/null && echo "✅ $file" || echo "❌ $file"
done

# Convert NetCDF to other formats
python codes/convert_output_formats.py Regional_Output/TuvaluForecast_latest.nc
```

---

## 🔧 Troubleshooting Commands

### Common Issue Resolution
```bash
# Fix Java classpath issues
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$JAVA_HOME/bin:$PATH

# Fix permission issues
sudo chown -R $USER:$USER .
chmod +x *.sh

# Reset environment
conda deactivate
conda activate Tuvalu_EWS_new

# Clear temporary files
./cleanup-ultrafast.sh

# Restart Docker daemon
sudo systemctl restart docker
```

### Network Troubleshooting
```bash
# Test data source connectivity
curl -I https://nomads.ncep.noaa.gov/
ping -c 4 nomads.ncep.noaa.gov

# Test with proxy (if needed)
export https_proxy=http://proxy.server:port
export http_proxy=http://proxy.server:port

# Download test file
wget https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.f000
```

### System Recovery
```bash
# Emergency system recovery
./health_check.sh --fix-issues

# Restore from backup
tar -xzf backup_$(date +%Y%m%d).tar.gz

# Reset to clean state
git checkout -- .
git clean -fd

# Full system reinstall
conda env remove -n Tuvalu_EWS_new
conda env create -f environment.yml
```

---

## 📚 Reference Information

### Command Options and Flags

#### deploy.sh Options
```bash
./deploy.sh [OPTIONS]

Options:
  --step N                Run specific step N (1-12)
  --steps N,M,P          Run multiple steps
  --resume-from N        Resume execution from step N
  --skip-steps N,M       Skip specific steps
  --production          Use production configuration
  --test                Run in test mode
  --benchmark           Run with performance benchmarking
  --monitor             Monitor resource usage
  --debug               Enable debug output
  --verbose             Enable verbose logging
  --dry-run             Validate without execution
  --force               Force execution even if checks fail
```

#### health_check.sh Options
```bash
./health_check.sh [OPTIONS]

Options:
  --summary             Show brief status summary
  --component NAME      Check specific component
  --validate-env        Validate environment setup
  --fix-issues          Attempt to fix common issues
  --brief               Brief output for monitoring
```

### Environment Variables
```bash
# Data directories
DATA_DIR              # Main data directory
TMP_DIR              # Temporary files directory  
OUTPUT_DIR           # Output files directory
LOG_DIR              # Log files directory

# External paths
JAVA_HOME            # Java installation directory
CONDA_PREFIX         # Conda environment path

# Model executables
SWAN_EXE            # SWAN executable path
SFINCS_EXE          # SFINCS executable path
XBEACH_EXE          # XBeach executable path

# API credentials
NCEP_API_KEY        # NCEP API access key
CMEMS_USERNAME      # CMEMS username
CMEMS_PASSWORD      # CMEMS password

# System configuration
OMP_NUM_THREADS     # OpenMP thread count
PROCESSING_MODE     # Processing mode (standard/lightweight)
```

### File Locations
```bash
# Configuration files
.env                    # Development environment variables
.env.production         # Production environment variables
.env.ultrafast         # Ultra-fast deployment settings

# Scripts and executables
codes/                 # Processing scripts (steps 1-12)
executables/          # Model binaries and tools
*.sh                  # Shell scripts for automation

# Data directories
tmp/                  # Temporary processing files
Regional_tmp/         # Regional temporary data
Regional_Output/      # Final forecast outputs
logs/                 # System and model logs
archives/             # Historical data archives
```

This commands reference provides comprehensive coverage of all available operations in the Tuvalu Forecast System. Use it as a quick reference during development, testing, and production operations.
