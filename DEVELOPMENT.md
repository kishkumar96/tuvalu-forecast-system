# Tuvalu Forecast System - Comprehensive Development Guide

## 🎯 Development Overview

The Tuvalu Early Warning System is a production-ready coastal forecasting system that provides automated 7-day forecasts for the Tuvalu islands. This guide covers the complete development environment, architecture, and workflows.

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Data Sources  │    │   Processing     │    │     Models      │
│                 │    │     Pipeline     │    │                 │
│  • NCEP GFS     │───►│  Steps 1-6       │───►│  • SWAN         │
│  • CMEMS        │    │  (Pre-process)   │    │  • SFINCS       │
│  • TPXO10       │    │  • Download      │    │  • XBeach       │
│  • Local Obs    │    │  • Transform     │    │                 │
└─────────────────┘    │  • Validate      │    └─────────────────┘
                       └──────────────────┘              │
                                 │                       │
┌─────────────────┐              │       ┌─────────────────┐
│     Outputs     │◄─────────────┴───────│ Post-Processing │
│                 │                      │                 │
│  • NetCDF       │                      │  Steps 7-12     │
│  • Flood Maps   │                      │  • Model Run    │
│  • Wave Data    │                      │  • Validate     │
│  • Reports      │                      │  • Generate     │
└─────────────────┘                      └─────────────────┘
```

### Component Breakdown

#### Data Pipeline (Steps 1-6)
- **Step 1**: NCEP GFS atmospheric data download
- **Step 2**: CMEMS sea level anomaly data download  
- **Step 3**: TPXO10 tidal forcing generation
- **Step 4**: Inverted barometer pressure forcing
- **Step 5**: Wave boundary condition generation
- **Step 6**: Wind forcing field preparation

#### Model Execution (Steps 7-11)
- **Step 7**: SWAN spectral wave model execution
- **Step 8**: Wave output post-processing
- **Step 9**: Flood risk assessment generation
- **Step 10**: XBeach coastal morphodynamics
- **Step 11**: SFINCS storm surge modeling

#### Output Generation (Step 12)
- **Step 12**: Final NetCDF output and report generation

## 🛠️ Development Environment Setup

### Method 1: Conda Environment (Recommended)

```bash
# Clone and navigate to project
cd /media/judith/Big_Booty1/Tuvalu_Forecast/tailored-report-tv

# Activate existing environment
conda activate Tuvalu_EWS_new

# Or create new environment from scratch
conda env create -f environment.yml
conda activate Tuvalu_EWS_new

# Verify installation
python -c "import netCDF4, requests, numpy; print('Environment ready')"
```

### Method 2: Docker Development Environment

```bash
# Build development container
docker build -f Dockerfile.simple-working -t tuvalu-dev .

# Run with live code mounting
docker run -it --rm \
  -v $(pwd)/codes:/app/codes \
  -v $(pwd)/tmp:/app/tmp \
  -v $(pwd)/Regional_Output:/app/Regional_Output \
  -v /media:/media \
  tuvalu-dev bash

# Alternative: Full workspace mount
docker run -it --rm \
  -v $(pwd):/workspace \
  -v /media:/media \
  tuvalu-dev bash
```

### Method 3: Virtual Environment

```bash
# Create and activate virtual environment
python -m venv tuvalu_ews_pip
source tuvalu_ews_pip/bin/activate

# Install dependencies
pip install -r requirements_working.txt

# Verify installation
python -c "import netCDF4, requests, numpy; print('Environment ready')"
```

## 📁 Project Structure Deep Dive

```
tailored-report-tv/
├── codes/                      # 🐍 Core Python processing scripts
│   ├── step1_download_NCEP.py      # NCEP atmospheric data retrieval
│   ├── step2_download_CMEMS*.py     # Sea level anomaly data
│   ├── step3_gen_tide*.py           # Tidal forcing generation
│   ├── step4_gen_Inverted*.py       # Barometric forcing
│   ├── step5_make_wave_forcing.py   # Wave boundary conditions
│   ├── step6_make_wind_forcing.py   # Wind forcing preparation
│   ├── step7_run_SWAN.py            # SWAN wave model execution
│   ├── step8_postprocess_output.py  # Wave output processing
│   ├── step9_make_flood_risk.py     # Flood risk generation
│   ├── step10_run_XBeach.py         # XBeach coastal model
│   ├── step11_run_SFINCS.py         # SFINCS storm surge model
│   └── step12_postprocess_SFINCS.py # Final output generation
├── extras/                     # 🗺️ Model configurations
│   ├── tuvalu/                     # Tuvalu-specific configurations
│   │   ├── swan/                   # SWAN model setup files
│   │   ├── sfincs/                 # SFINCS configuration
│   │   └── xbeach/                 # XBeach setup
│   └── common/                     # Shared model resources
├── executables/               # 🔧 Model binaries and tools
│   ├── toolsUI-5.4.1.jar         # GRIB to NetCDF converter
│   ├── swan.exe                   # SWAN wave model executable
│   ├── sfincs                     # SFINCS storm surge executable
│   └── xbeach                     # XBeach coastal executable
├── persistent_data/           # 💾 Static model data
│   ├── bathymetry/               # Depth/elevation grids
│   ├── coastlines/               # Shoreline data
│   └── boundaries/               # Model boundary conditions
├── tmp/                       # 📁 Temporary processing files
├── Regional_tmp/              # 🌊 Regional temporary data
├── Regional_Output/           # 📊 Final forecast outputs
├── logs/                      # 📋 System and model logs
├── archives/                  # 🗃️ Historical forecast data
├── runs/                      # 🏃 Current and recent runs
├── tests/                     # 🧪 Test suite and validation
├── Hall_Reports/              # 📑 Archived forecast reports
└── miniconda/                 # 🐍 Conda environment data
```

## 🔧 Development Workflows

### Standard Development Cycle

1. **Setup Environment**
   ```bash
   conda activate Tuvalu_EWS_new
   # or
   source tuvalu_ews_pip/bin/activate
   ```

2. **Make Code Changes**
   - Edit files in `codes/` directory
   - Modify configuration in `extras/` if needed
   - Update dependencies in `requirements_working.txt`

3. **Test Changes**
   ```bash
   # Test individual steps
   python codes/step1_download_NCEP.py
   python codes/step7_run_SWAN.py
   
   # Run specific test suite
   python -m pytest tests/test_download.py
   
   # Full system test
   ./deploy.sh --test
   ```

4. **Validate Output**
   ```bash
   # Check NetCDF output
   ncdump -h Regional_Output/TuvaluForecast_*.nc
   
   # Validate model completion
   grep "NORMAL END" logs/swan.log
   grep "SFINCS finished" logs/sfincs.log
   ```

5. **Build and Deploy**
   ```bash
   # Development build
   docker build -f Dockerfile.simple-working -t tuvalu-dev .
   
   # Production build
   ./build-production.sh
   
   # Deploy to production
   ./deploy.sh
   ```

### Docker Development Workflow

```bash
# 1. Build development image
docker build -f Dockerfile.simple-working -t tuvalu-dev .

# 2. Run with code mounting for live editing
docker run -it --rm \
  -v $(pwd)/codes:/app/codes \
  -v $(pwd)/.env:/app/.env \
  tuvalu-dev

# 3. Inside container - test changes immediately
cd /app
python codes/step1_download_NCEP.py

# 4. Changes on host sync automatically to container
# Edit files with your favorite editor on the host

# 5. When ready, build production image
docker build -f Dockerfile -t tuvalu-prod .
```

### Multi-Environment Development

The system supports multiple deployment environments:

#### Development Environment
```bash
# Use .env for development settings
cp .env.example .env
# Edit .env with development configurations

# Build development container
docker build -f Dockerfile.simple-working -t tuvalu-dev .

# Run development workflow
docker-compose -f docker-compose.working.yml up
```

#### Ultra-Fast Environment
```bash
# Use .env.ultrafast for rapid testing
cp .env.ultrafast .env.ultrafast.local
# Edit for local ultra-fast settings

# Build ultra-fast container
./ultrafast-build.sh

# Run ultra-fast workflow
docker run -ti --rm tuvalu-ultrafast
```

#### Production Environment
```bash
# Use .env.production for production settings
cp .env.production .env.production.local
# Edit for production configurations

# Build production container with credentials
./build-with-credentials.sh

# Deploy to production
./deploy.sh --production
```

## 🧪 Testing Strategy

### Test Categories

#### Unit Tests
```bash
# Test individual functions and modules
python -m pytest tests/unit/test_download.py
python -m pytest tests/unit/test_models.py
python -m pytest tests/unit/test_processing.py

# Run with coverage
python -m pytest --cov=codes tests/unit/
```

#### Integration Tests
```bash
# Test complete workflows
python -m pytest tests/integration/test_pipeline.py
python -m pytest tests/integration/test_models.py

# Test Docker environments
python -m pytest tests/integration/test_docker.py
```

#### System Tests
```bash
# Test complete forecast execution
./deploy.sh --test

# Benchmark performance
./deploy.sh --benchmark

# Validate output quality
python -m pytest tests/system/test_output_validation.py
```

### Test Data Management

```bash
# Setup test data
mkdir -p tests/data/input
mkdir -p tests/data/expected_output

# Download test datasets
python tests/setup_test_data.py

# Run tests with test data
python -m pytest tests/ --test-data=tests/data/
```

## 🐛 Debugging Guide

### Common Development Issues

#### Java Classpath Errors
```bash
# Issue: toolsUI-5.4.1.jar not found
# Solution: Check path in step1_download_NCEP.py
ls -la executables/toolsUI-5.4.1.jar

# Fix classpath in code
# From: '../executables/toolsUI-5.4.1.jar'
# To: './executables/toolsUI-5.4.1.jar'
```

#### Download Failures
```bash
# Issue: NCEP/CMEMS download failures
# Debug: Check network connectivity
curl -I "https://nomads.ncep.noaa.gov/"

# Debug: Verify server status
python codes/debug_downloads.py

# Solution: Implement retry logic
# Already implemented in download functions
```

#### Model Execution Issues
```bash
# Issue: SWAN/SFINCS/XBeach crashes
# Debug: Check input file formats
ls -la tmp/
ncdump -h tmp/wind_tmp_000.nc

# Debug: Verify coordinate bounds
python codes/debug_coordinates.py

# Check model logs
tail -f logs/swan.log
tail -f logs/sfincs.log
```

#### Docker Build Problems
```bash
# Issue: Docker build failures
# Debug: Check base image availability
docker pull continuumio/miniconda3:latest

# Debug: Verify dependency availability
docker run --rm continuumio/miniconda3 conda list

# Solution: Use specific base image versions
# Edit Dockerfile to use pinned versions
```

### Debugging Tools

#### Log Analysis
```bash
# Real-time log monitoring
tail -f logs/tuvalu_forecast.log

# Search for errors
grep -i error logs/*.log
grep -i "failed\|exception\|traceback" logs/*.log

# Analyze model execution
grep "NORMAL END\|terminated" logs/swan.log
grep "finished\|completed" logs/sfincs.log
```

#### Performance Profiling
```bash
# Profile Python code execution
python -m cProfile -o profile_output codes/step1_download_NCEP.py

# Analyze profile results
python -c "import pstats; pstats.Stats('profile_output').sort_stats('time').print_stats(10)"

# Monitor system resources
./health_check.sh
```

#### Data Validation
```bash
# Validate NetCDF files
ncdump -h Regional_Output/TuvaluForecast_*.nc

# Check data ranges
python codes/validate_data_ranges.py

# Compare with reference data
python codes/compare_with_reference.py
```

## 🚀 Performance Optimization

### Code Optimization

#### Parallel Processing
```python
# Example: Parallel file downloads
from concurrent.futures import ThreadPoolExecutor
import requests

def download_file(url):
    response = requests.get(url)
    return response.content

# Use thread pool for multiple downloads
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(download_file, url) for url in urls]
    results = [future.result() for future in futures]
```

#### Memory Management
```python
# Example: Efficient NetCDF handling
import netCDF4 as nc
import numpy as np

# Use context managers to ensure file closure
with nc.Dataset('large_file.nc', 'r') as dataset:
    # Process data in chunks
    for i in range(0, len(dataset.dimensions['time']), chunk_size):
        chunk = dataset.variables['data'][i:i+chunk_size]
        process_chunk(chunk)
```

### System Optimization

#### Docker Optimization
```dockerfile
# Multi-stage build for smaller images
FROM continuumio/miniconda3:latest AS builder
COPY requirements_working.txt .
RUN conda install --file requirements_working.txt

FROM continuumio/miniconda3:latest AS runtime
COPY --from=builder /opt/conda /opt/conda
COPY codes/ /app/codes/
```

#### Storage Optimization
```bash
# Clean temporary files regularly
./cleanup-ultrafast.sh

# Use compression for archives
tar -czf archive_$(date +%Y%m%d).tar.gz runs/

# Monitor disk usage
df -h
du -sh */
```

## 📊 Monitoring and Metrics

### System Monitoring
```bash
# System health check
./health_check.sh

# Monitor forecast execution
./efficiency_monitor.sh

# Check resource usage
htop
iotop
```

### Application Metrics
```python
# Example: Add timing metrics to processing steps
import time
import logging

def timed_step(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        logging.info(f"{func.__name__} completed in {execution_time:.2f} seconds")
        return result
    return wrapper

@timed_step
def download_NCEP(now):
    # Existing download logic
    pass
```

### Quality Metrics
```bash
# Output validation
python codes/validate_output_quality.py

# Compare with observations
python codes/validate_against_observations.py

# Generate quality reports
python codes/generate_quality_report.py
```

## 🔄 Continuous Integration

### Automated Testing
```yaml
# Example GitHub Actions workflow
name: Tuvalu Forecast CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Conda
        uses: conda-incubator/setup-miniconda@v2
      - name: Install dependencies
        run: conda env create -f environment.yml
      - name: Run tests
        run: |
          conda activate Tuvalu_EWS_new
          python -m pytest tests/
      - name: Build Docker image
        run: docker build -f Dockerfile.simple-working .
```

### Deployment Pipeline
```bash
# Automated deployment script
#!/bin/bash
set -e

# Run tests
python -m pytest tests/

# Build production image
./build-production.sh

# Deploy to production
./deploy.sh --production

# Validate deployment
./health_check.sh

# Send notification
echo "Deployment completed successfully" | mail -s "Tuvalu Forecast Deployment" admin@example.com
```

## 🔐 Security Considerations

### Credentials Management
```bash
# Use environment files for sensitive data
echo "NCEP_API_KEY=your_key_here" >> .env.production.local
echo "CMEMS_USERNAME=your_username" >> .env.production.local

# Never commit credentials to version control
echo ".env.production.local" >> .gitignore
echo "*.key" >> .gitignore
```

### Container Security
```dockerfile
# Use non-root user in containers
FROM continuumio/miniconda3:latest
RUN groupadd -r tuvalu && useradd -r -g tuvalu tuvalu
USER tuvalu

# Minimize attack surface
RUN rm -rf /tmp/* /var/tmp/*
```

### Network Security
```bash
# Use secure download protocols
# Replace HTTP with HTTPS where possible
# Implement certificate validation
```

## 📈 Scaling Considerations

### Horizontal Scaling
- Deploy multiple instances for different regions
- Use container orchestration (Kubernetes, Docker Swarm)
- Implement load balancing for API endpoints

### Vertical Scaling
- Optimize memory usage for large datasets
- Use GPU acceleration for model execution where applicable
- Implement efficient data storage strategies

### Data Management
- Implement data lifecycle policies
- Use cloud storage for long-term archival
- Optimize database queries and indexing

## 🤝 Contributing Guidelines

### Code Standards
```python
# Follow PEP 8 style guidelines
# Use type hints where possible
def download_data(start_date: datetime, end_date: datetime) -> List[str]:
    """Download atmospheric data for specified date range.
    
    Args:
        start_date: Start of download period
        end_date: End of download period
        
    Returns:
        List of downloaded file paths
    """
    pass

# Add comprehensive docstrings
# Include error handling
# Write unit tests for new functions
```

### Documentation Standards
- Update relevant documentation when making changes
- Include examples in docstrings
- Maintain changelog for significant changes
- Update API reference for new features

### Testing Requirements
- All new features must include unit tests
- Integration tests for workflow changes
- Performance benchmarks for optimization changes
- Documentation tests for API changes

This development guide provides comprehensive coverage of the Tuvalu Forecast System development environment, workflows, and best practices. Use it as a reference for all development activities and keep it updated as the system evolves.
