# Tuvalu Forecast System - Portability Guide

## 🌐 Making the System Work Anywhere

This guide explains how to make the Tuvalu Forecast System portable across different environments, operating systems, and deployment scenarios.

---

## 🎯 Portability Overview

The Tuvalu Forecast System is designed with multiple deployment options to ensure it can run in various environments:

1. **Native Python** (Conda/pip) - Direct system installation
2. **Docker Containers** - Fully containerized deployment
3. **Hybrid Mode** - Combined native and containerized components
4. **Cloud Deployment** - AWS, Azure, Google Cloud compatibility

---

## 🐧 Linux Deployment (Primary)

### Ubuntu/Debian Systems

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-dev python3-pip git curl wget
sudo apt install -y build-essential gfortran libnetcdf-dev libhdf5-dev
sudo apt install -y openjdk-11-jdk docker.io docker-compose

# Install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b -p $HOME/miniconda3
source $HOME/miniconda3/bin/activate

# Clone and setup
git clone <repository-url> tuvalu-forecast
cd tuvalu-forecast/tailored-report-tv

# Create environment
conda env create -f environment.yml
conda activate Tuvalu_EWS_new

# Verify installation
./health_check.sh
```

### CentOS/RHEL Systems

```bash
# Install system dependencies
sudo yum update -y
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3-devel netcdf-devel hdf5-devel
sudo yum install -y java-11-openjdk docker docker-compose

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# Continue with Miniconda installation (same as Ubuntu)
```

### Alpine Linux (Minimal)

```bash
# Install minimal dependencies
apk add --no-cache python3 py3-pip git bash curl wget
apk add --no-cache build-base gfortran netcdf-dev hdf5-dev
apk add --no-cache openjdk11 docker docker-compose

# Continue with environment setup
```

---

## 🖥️ Windows Deployment

### Windows 10/11 with WSL2 (Recommended)

```powershell
# Install WSL2
wsl --install -d Ubuntu-20.04

# Enter WSL environment
wsl

# Follow Linux deployment instructions above
```

### Native Windows (Advanced)

```powershell
# Install Chocolatey package manager
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Install dependencies
choco install -y python3 git curl wget
choco install -y openjdk11 docker-desktop

# Install Miniconda
Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile "miniconda.exe"
Start-Process -FilePath "miniconda.exe" -ArgumentList "/S" -Wait

# Continue with environment setup (adapt paths for Windows)
```

---

## 🍎 macOS Deployment

### macOS with Homebrew

```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install python@3.9 git curl wget
brew install netcdf hdf5 openjdk@11
brew install --cask docker

# Install Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh -b -p $HOME/miniconda3
source $HOME/miniconda3/bin/activate

# Continue with environment setup
```

### macOS ARM64 (Apple Silicon)

```bash
# Use ARM64 version of Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
bash Miniconda3-latest-MacOSX-arm64.sh -b -p $HOME/miniconda3

# Some packages may need specific ARM64 builds
conda config --add channels conda-forge
conda config --set channel_priority flexible

# Continue with environment setup
```

---

## 🐳 Docker Deployment (Universal)

### Docker-Only Deployment

```bash
# Clone repository
git clone <repository-url> tuvalu-forecast
cd tuvalu-forecast/tailored-report-tv

# Build production image
docker build -f Dockerfile -t tuvalu-forecast .

# Run complete forecast
docker run -v $(pwd)/Regional_Output:/app/Regional_Output \
           -v /data:/data \
           --rm tuvalu-forecast

# For development
docker build -f Dockerfile.simple-working -t tuvalu-dev .
docker run -v $(pwd)/codes:/app/codes -ti tuvalu-dev bash
```

### Docker Compose Deployment

```bash
# Production deployment
docker-compose -f docker-compose.yml up

# Development deployment
docker-compose -f docker-compose.working.yml up

# Ultra-fast testing
docker-compose -f docker-compose.ultrafast-final.yml up
```

---

## ☁️ Cloud Deployment

### AWS Deployment

```bash
# EC2 Instance Setup
# Launch Ubuntu 20.04 LTS instance (m5.2xlarge recommended)

# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awszip"
unzip awszip && sudo ./aws/install

# Setup S3 for data storage
aws s3 mb s3://tuvalu-forecast-data
aws s3 mb s3://tuvalu-forecast-output

# ECS Deployment (Docker)
# Create task definition with tuvalu-forecast image
# Setup ECS cluster and service
# Configure S3 volume mounts

# Lambda Deployment (for lightweight processing)
# Package specific steps as Lambda functions
# Use EventBridge for scheduling
```

### Azure Deployment

```bash
# Azure Container Instance
az container create \
  --resource-group tuvalu-rg \
  --name tuvalu-forecast \
  --image tuvalu-forecast:latest \
  --cpu 4 --memory 16 \
  --restart-policy OnFailure

# Azure Batch (for large-scale processing)
# Create Batch account and pool
# Submit forecast jobs as Batch tasks

# Azure Functions (serverless)
# Deploy individual processing steps
# Use Timer triggers for scheduling
```

### Google Cloud Deployment

```bash
# Cloud Run (serverless containers)
gcloud run deploy tuvalu-forecast \
  --image gcr.io/project/tuvalu-forecast \
  --platform managed \
  --memory 8Gi \
  --cpu 4

# Compute Engine
# Create VM instance with Container-Optimized OS
# Use persistent disks for data storage

# Cloud Functions
# Deploy lightweight processing functions
# Use Cloud Scheduler for automation
```

---

## 🔧 Environment Adaptation

### Path Configuration

```bash
# Create portable path configuration
cat > config/paths.conf << EOF
# Data directories
DATA_DIR=${DATA_DIR:-/data}
TMP_DIR=${TMP_DIR:-/tmp/tuvalu}
OUTPUT_DIR=${OUTPUT_DIR:-/output}
LOG_DIR=${LOG_DIR:-/logs}

# Executable paths
JAVA_HOME=${JAVA_HOME:-/usr/lib/jvm/java-11-openjdk}
SWAN_EXE=${SWAN_EXE:-./executables/swan.exe}
SFINCS_EXE=${SFINCS_EXE:-./executables/sfincs}
XBEACH_EXE=${XBEACH_EXE:-./executables/xbeach}

# Network configuration
PROXY_HOST=${PROXY_HOST:-}
PROXY_PORT=${PROXY_PORT:-}
NO_PROXY=${NO_PROXY:-localhost,127.0.0.1}
EOF

# Source in all scripts
source config/paths.conf
```

### Dependency Management

```yaml
# environment-portable.yml - Cross-platform environment
name: tuvalu-portable
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - netcdf4
  - numpy
  - scipy
  - matplotlib
  - requests
  - pip
  - pip:
    - copernicus-marine-client
    - # Other pip packages
```

### Resource Configuration

```bash
# Auto-detect system resources
detect_resources() {
    # CPU cores
    CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 2)
    
    # Memory (GB)
    if command -v free >/dev/null; then
        MEM_GB=$(($(free -m | awk '/^Mem:/{print $2}') / 1024))
    elif command -v sysctl >/dev/null; then
        MEM_GB=$(($(sysctl -n hw.memsize) / 1024 / 1024 / 1024))
    else
        MEM_GB=8
    fi
    
    # Disk space (GB)
    DISK_GB=$(df -BG . | tail -1 | awk '{print $4}' | sed 's/G//')
    
    echo "Detected: ${CORES} cores, ${MEM_GB}GB RAM, ${DISK_GB}GB disk"
}

# Configure based on resources
configure_resources() {
    detect_resources
    
    # Set parallel processing
    export OMP_NUM_THREADS=$((CORES / 2))
    export SWAN_THREADS=$CORES
    
    # Set memory limits
    if [ $MEM_GB -lt 16 ]; then
        export PROCESSING_MODE="lightweight"
        export CHUNK_SIZE=100
    else
        export PROCESSING_MODE="standard"
        export CHUNK_SIZE=500
    fi
}
```

---

## 📦 Distribution and Packaging

### Standalone Installer

```bash
#!/bin/bash
# create_installer.sh - Create portable installer

set -e

echo "Creating Tuvalu Forecast System portable installer..."

# Create directory structure
mkdir -p tuvalu-portable/{bin,lib,data,config}

# Copy source code
cp -r codes/ tuvalu-portable/
cp -r extras/ tuvalu-portable/
cp -r executables/ tuvalu-portable/

# Copy dependencies
cp requirements_working.txt tuvalu-portable/
cp environment.yml tuvalu-portable/

# Create installation script
cat > tuvalu-portable/install.sh << 'EOF'
#!/bin/bash
echo "Installing Tuvalu Forecast System..."

# Detect OS
OS=$(uname -s)
case $OS in
    Linux*)  PLATFORM=linux;;
    Darwin*) PLATFORM=mac;;
    CYGWIN*|MINGW*) PLATFORM=windows;;
    *) echo "Unsupported OS: $OS"; exit 1;;
esac

echo "Detected platform: $PLATFORM"

# Install Miniconda if not present
if ! command -v conda &> /dev/null; then
    echo "Installing Miniconda..."
    case $PLATFORM in
        linux)
            wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
            ;;
        mac)
            curl -s -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
            mv Miniconda3-latest-MacOSX-x86_64.sh miniconda.sh
            ;;
    esac
    
    bash miniconda.sh -b -p ./miniconda
    source ./miniconda/bin/activate
else
    echo "Using existing conda installation"
fi

# Create environment
conda env create -f environment.yml -p ./env
conda activate ./env

# Make scripts executable
chmod +x *.sh

echo "Installation complete!"
echo "To run: conda activate ./env && ./deploy.sh"
EOF

chmod +x tuvalu-portable/install.sh

# Create archive
tar -czf tuvalu-forecast-portable.tar.gz tuvalu-portable/

echo "Portable installer created: tuvalu-forecast-portable.tar.gz"
```

### Container Images

```bash
# Multi-architecture Docker builds
docker buildx create --use
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t tuvalu-forecast:latest \
  --push .

# Singularity container (HPC systems)
sudo singularity build tuvalu-forecast.sif docker://tuvalu-forecast:latest

# AppImage (Linux desktop)
# Create AppDir structure and use appimagetool
```

---

## 🔄 Migration Scripts

### From Legacy Systems

```bash
#!/bin/bash
# migrate_from_legacy.sh

echo "Migrating from legacy Tuvalu system..."

# Backup existing data
if [ -d "/old/tuvalu/data" ]; then
    echo "Backing up legacy data..."
    cp -r /old/tuvalu/data/ ./legacy_backup/
fi

# Convert configuration files
if [ -f "/old/tuvalu/config.ini" ]; then
    echo "Converting configuration..."
    python scripts/convert_config.py /old/tuvalu/config.ini .env
fi

# Migrate model grids
if [ -d "/old/tuvalu/grids" ]; then
    echo "Migrating model grids..."
    cp -r /old/tuvalu/grids/ ./persistent_data/
fi

echo "Migration complete. Please review .env file and test system."
```

### Between Environments

```bash
#!/bin/bash
# export_environment.sh

echo "Exporting current environment for migration..."

# Export conda environment
conda env export > environment_$(date +%Y%m%d).yml

# Package model data
tar -czf model_data_$(date +%Y%m%d).tar.gz persistent_data/

# Export configuration
cp .env .env_$(date +%Y%m%d).backup
cp .env.production .env.production_$(date +%Y%m%d).backup

# Create migration package
mkdir migration_package
cp environment_*.yml migration_package/
cp model_data_*.tar.gz migration_package/
cp .env_*.backup migration_package/
cp -r scripts/ migration_package/

tar -czf tuvalu_migration_$(date +%Y%m%d).tar.gz migration_package/

echo "Migration package created: tuvalu_migration_$(date +%Y%m%d).tar.gz"
```

---

## 🧪 Validation and Testing

### Cross-Platform Testing

```bash
#!/bin/bash
# test_portability.sh

echo "Testing system portability..."

# Test environment detection
./scripts/detect_environment.sh

# Test dependencies
python -c "
import sys, platform
print(f'Python: {sys.version}')
print(f'Platform: {platform.system()} {platform.machine()}')

# Test imports
try:
    import netCDF4, numpy, scipy, matplotlib, requests
    print('✅ All Python dependencies available')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    sys.exit(1)
"

# Test Java
if command -v java &> /dev/null; then
    java_version=$(java -version 2>&1 | head -1)
    echo "✅ Java available: $java_version"
else
    echo "❌ Java not found"
fi

# Test model executables
for exe in executables/swan.exe executables/sfincs executables/xbeach; do
    if [ -x "$exe" ]; then
        echo "✅ $exe is executable"
    else
        echo "❌ $exe not found or not executable"
    fi
done

# Test data access
if curl -s --head https://nomads.ncep.noaa.gov/ | head -1 | grep -q "200 OK"; then
    echo "✅ NCEP data access OK"
else
    echo "⚠️  NCEP data access may be limited"
fi

echo "Portability test complete"
```

---

## 📚 Platform-Specific Notes

### High-Performance Computing (HPC)

```bash
# SLURM job submission
cat > submit_forecast.slurm << EOF
#!/bin/bash
#SBATCH --job-name=tuvalu-forecast
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G
#SBATCH --time=02:00:00
#SBATCH --partition=compute

module load singularity
singularity exec tuvalu-forecast.sif python codes/step1_download_NCEP.py
EOF

sbatch submit_forecast.slurm
```

### Embedded Systems (ARM)

```bash
# Raspberry Pi optimization
echo "gpu_mem=16" >> /boot/config.txt  # Minimize GPU memory
echo "arm_freq=1500" >> /boot/config.txt  # Boost CPU

# Use lighter dependencies
pip install --no-binary=scipy,numpy scipy numpy
```

### Air-Gapped Environments

```bash
# Create offline package bundle
pip download -r requirements_working.txt -d offline_packages/
conda env export > environment_offline.yml

# Transfer and install offline
pip install --no-index --find-links offline_packages/ -r requirements_working.txt
```

---

## 🎯 Summary

The Tuvalu Forecast System has been designed with portability as a core principle:

- **Multi-platform support**: Linux, Windows, macOS
- **Multiple deployment options**: Native, Docker, Cloud
- **Resource adaptation**: Automatic resource detection and configuration
- **Dependency management**: Isolated environments and clear requirements
- **Migration tools**: Scripts for moving between environments
- **Validation**: Comprehensive testing across platforms

Choose the deployment method that best fits your target environment and requirements. The Docker-based deployment offers the highest portability, while native installations provide maximum performance on dedicated systems.
