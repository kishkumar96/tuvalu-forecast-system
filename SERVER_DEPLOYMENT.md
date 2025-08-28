# Tuvalu Forecast System - Server Deployment Guide

This guide explains how to deploy the Tuvalu Forecast System on a new server from the Git repository.

## Summary: Is the Repo Ready for Server Deployment?

**YES**, but with important caveats about ignored assets that must be handled during deployment.

## What's in Git vs What's Ignored

### ✅ Included in Git Repository:
- All Python source code (main pipeline, processing steps, utilities)
- Docker configuration (Dockerfile, docker-compose.yml)  
- Python dependencies (requirements_working.txt) - now includes scikit-learn
- Shell scripts and management tools
- Configuration templates (.env.example)
- Documentation

### ❌ Excluded from Git (.gitignore):
- **SWAN executables** (`executables/swan.exe`, `executables/swanrun`)
- **Java tools** (`executables/toolsUI-5.4.1.jar`)
- **Data directories** (`runs/`, `archives/`, `logs/`, `tmp/`)
- **Output directories** (`Regional_Output/`, `Regional_tmp/`)
- **NCEP/CMEMS data files** (downloaded during forecast runs)
- **Environment configuration** (`.env` with secrets)
- **Large model files and cached data**

## Deployment Options

### Option 1: Docker Deployment (Recommended)

The Dockerfile already handles most dependencies, but you need to ensure non-git assets are available:

```bash
# Clone the repository
git clone <your-repo-url> tuvalu-forecast
cd tuvalu-forecast

# Copy your SWAN executables to the executables/ directory
# (These must be obtained separately and placed here)
cp /path/to/your/swan.exe executables/
cp /path/to/your/swanrun executables/ 
cp /path/to/your/toolsUI-5.4.1.jar executables/

# Create environment file from template
cp .env.example .env
# Edit .env with your actual configuration values

# Build and run with Docker
docker build -t tuvalu-forecast .
docker-compose up -d
```

### Option 2: Native Installation

For native installation on Ubuntu/Debian:

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential g++ gfortran mpich gcc \
    python3-dev python3-pip python3-venv wget zlib1g-dev \
    libnetcdf-dev libnetcdff-dev default-jre

# Clone repository
git clone <your-repo-url> tuvalu-forecast
cd tuvalu-forecast

# Set up Python environment
python3 -m venv tuvalu_env
source tuvalu_env/bin/activate
pip install --upgrade pip
pip install -r requirements_working.txt

# Copy executables (must be done manually)
# Place SWAN executables in executables/ directory
# Ensure they're executable: chmod +x executables/*

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Create required directories
mkdir -p runs archives logs tmp Regional_Output Regional_tmp

# Run forecast
cd codes
python main_run_operational.py
```

## Critical Dependencies Not in Git

### 1. SWAN Wave Model
- **Files needed**: `swan.exe`, `swanrun`  
- **Source**: Must be compiled from SWAN source code or obtained from SWAN distribution
- **License**: Check SWAN licensing requirements for your use case
- **Installation**: Place in `executables/` directory and ensure executable permissions

### 2. NetCDF Java Tools  
- **File needed**: `toolsUI-5.4.1.jar`
- **Source**: Download from Unidata NetCDF-Java project
- **Installation**: Place in `executables/` directory

### 3. Configuration and Secrets
- **File needed**: `.env`
- **Source**: Create from `.env.example` template
- **Contents**: API keys, database credentials, file paths, etc.
- **Security**: Never commit actual `.env` to git

### 4. Data Directories
The system expects these directories to exist (will be created if missing):
- `runs/` - Forecast run outputs
- `archives/` - Archived forecasts  
- `logs/` - Application logs
- `tmp/` - Temporary processing files
- `Regional_Output/` - Regional forecast outputs
- `Regional_tmp/` - Regional processing temp files

## Automated Deployment Script

Here's a deployment script that handles the common setup:

```bash
#!/bin/bash
# deploy-tuvalu.sh

set -e

echo "Deploying Tuvalu Forecast System..."

# Clone repository
git clone <your-repo-url> tuvalu-forecast
cd tuvalu-forecast

# Check for required executables
if [ ! -f "executables/swan.exe" ]; then
    echo "ERROR: swan.exe not found in executables/"
    echo "Please copy SWAN executables to executables/ directory before running deployment"
    exit 1
fi

# Create required directories
mkdir -p runs archives logs tmp Regional_Output Regional_tmp

# Set up environment file
if [ ! -f ".env" ]; then
    echo "Creating .env from template..."
    cp .env.example .env
    echo "IMPORTANT: Edit .env file with your actual configuration before running forecasts"
fi

# Build Docker image
echo "Building Docker image..."
docker build -t tuvalu-forecast .

echo "Deployment complete!"
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: docker-compose up -d"
```

## Verification Steps

After deployment, verify the system works:

```bash
# Test that all dependencies are available
docker run --rm tuvalu-forecast python -c "
import sklearn
import netCDF4
import xarray
import pandas
import numpy
print('All Python dependencies OK')
"

# Test that SWAN executable is available
docker run --rm tuvalu-forecast which swan.exe

# Run a test forecast (if you have test data)
docker run --rm -v $(pwd)/test_data:/TuvaluForecast/test_data tuvalu-forecast python codes/main_run_operational.py --test
```

## Troubleshooting Common Issues

### Missing scikit-learn
**Error**: `ModuleNotFoundError: No module named 'sklearn'`  
**Solution**: Already fixed in requirements_working.txt - rebuild Docker image

### SWAN not found
**Error**: `FileNotFoundError: swan.exe not found`  
**Solution**: Copy SWAN executables to `executables/` directory before building

### Permission denied on executables
**Error**: `Permission denied: ./swan.exe`  
**Solution**: `chmod +x executables/*` or rebuild Docker image (Dockerfile handles this)

### Missing data directories
**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'runs/'`
**Solution**: Create directories with `mkdir -p runs archives logs tmp Regional_Output Regional_tmp`

## Production Considerations

1. **Resource Requirements**: Ensure adequate CPU, memory, and disk space for forecast processing
2. **Network Access**: System needs internet access to download NCEP/CMEMS data
3. **Scheduling**: Set up cron jobs or systemd timers for automated forecast runs
4. **Monitoring**: Implement logging and alerting for forecast failures
5. **Backup**: Regular backup of forecast outputs and configuration
6. **Updates**: Plan for updating code while preserving data and configuration

## Security Notes

- Never commit `.env` files containing secrets
- Review and validate all external executables (SWAN, etc.) 
- Consider running in containers for isolation
- Implement proper access controls on forecast data
- Monitor network connections for data downloads

## Support

For deployment issues:
1. Check this deployment guide
2. Review DEPLOYMENT_GUIDE.md for technical details
3. Check logs in `logs/` directory
4. Test individual pipeline steps using test scripts

The system is production-ready when all dependencies (including non-git assets) are properly installed and configured.
