# 🌊 Tuvalu Forecast System - Production Docker Deployment

## 📋 Overview

This document describes the world-class Docker setup for the Tuvalu Forecast System, following industry best practices for production deployments.

## 🎯 Key Features

### 🔒 **Security First**
- Non-root user execution (uid/gid 1000)
- Read-only containers where possible
- Minimal attack surface with `no-new-privileges`
- Secure credential management
- Proper capability dropping and adding

### ⚡ **Performance Optimized**
- Multi-stage Docker builds
- Optimal layer caching
- Minimal image size with `.dockerignore`
- Resource limits and reservations
- BuildKit for faster builds

### 🏗️ **Production Ready**
- Comprehensive health checks
- Proper logging and monitoring
- Graceful shutdown handling
- Environment-specific configurations
- Service orchestration with profiles

### 🔄 **Operational Excellence**
- Smart resume functionality
- Automated scheduling
- System monitoring
- Easy backup and recovery
- Comprehensive management interface

## 🚀 Quick Start

### 1. Initial Setup

```bash
# Clone or navigate to the project
cd /path/to/tuvalu-forecast

# Copy environment template
cp tailored-report-tv/.env.production tailored-report-tv/.env

# Edit environment variables (especially credentials)
nano tailored-report-tv/.env
```

### 2. Build the System

```bash
# Build production image
./tailored-report-tv/build-production.sh

# Verify build
docker images | grep tuvalu-forecast
```

### 3. Deploy

```bash
# Start production system
./tailored-report-tv/tuvalu-manager.sh start

# Check status
./tailored-report-tv/tuvalu-manager.sh status

# View logs
./tailored-report-tv/tuvalu-manager.sh logs
```

## 🏗️ Architecture

### Docker Components

```
📦 Production Deployment
├── 🐳 Dockerfile (Multi-stage, optimized)
├── 🔧 docker-compose.yml (Production ready)
├── 📋 .dockerignore (Minimal build context)
├── 🛠️ build-production.sh (Automated build)
├── 👨‍💼 tuvalu-manager.sh (Management interface)
└── 🏥 docker-healthcheck.sh (Health monitoring)
```

### Service Architecture

```
🌐 Tuvalu Forecast System
├── 📊 tuvalu-forecast (Main application)
├── ⏰ tuvalu-scheduler (Automated runs)
├── 👁️ tuvalu-monitor (Health monitoring)
├── 🛠️ tuvalu-dev (Development environment)
└── 🧪 tuvalu-test (Testing environment)
```

## 🔧 Management Interface

The `tuvalu-manager.sh` script provides a comprehensive management interface:

### Deployment Operations
```bash
./tuvalu-manager.sh start          # Start system
./tuvalu-manager.sh stop           # Stop system
./tuvalu-manager.sh restart        # Restart system
./tuvalu-manager.sh status         # Show status
./tuvalu-manager.sh logs           # View logs
```

### Forecast Operations
```bash
./tuvalu-manager.sh forecast                    # Run current forecast
./tuvalu-manager.sh forecast --date=2025082500  # Run specific date
./tuvalu-manager.sh schedule                    # Start scheduler
./tuvalu-manager.sh monitor                     # Start monitoring
```

### Development Operations
```bash
./tuvalu-manager.sh dev            # Start dev environment
./tuvalu-manager.sh test           # Run tests
./tuvalu-manager.sh shell          # Interactive shell
./tuvalu-manager.sh exec python3 --version  # Execute commands
```

### System Operations
```bash
./tuvalu-manager.sh health         # Health check
./tuvalu-manager.sh info           # System information
./tuvalu-manager.sh cleanup        # Clean old data
```

## 📊 Service Profiles

### Production Profile
Full production deployment with scheduler and monitoring:
```bash
docker-compose --profile production up -d
```

### Development Profile
Development environment with debugging tools:
```bash
docker-compose --profile dev up -d tuvalu-dev
```

### Testing Profile
Automated testing environment:
```bash
docker-compose --profile test run --rm tuvalu-test
```

## 🔒 Security Features

### Container Security
- **Non-root execution**: All processes run as user `tuvalu` (uid 1000)
- **Capability management**: Minimal capabilities with proper dropping/adding
- **Read-only containers**: Where data persistence isn't required
- **Security options**: `no-new-privileges` enabled

### Credential Management
- **Environment files**: Secure credential storage in `.env`
- **Volume mounts**: Credential files mounted read-only
- **Secret management**: Support for Docker secrets in production

### Network Security
- **Isolated networks**: Custom bridge network for container communication
- **Minimal exposure**: Only necessary ports exposed
- **Health checks**: Continuous security monitoring

## 📈 Monitoring & Health Checks

### Built-in Health Checks
The system includes comprehensive health monitoring:

```bash
# Container-level health check
docker inspect --format='{{.State.Health.Status}}' tuvalu-forecast

# Application health check
./tuvalu-manager.sh health

# Detailed health monitoring
docker exec tuvalu-forecast /app/docker-healthcheck.sh
```

### Health Check Categories
- **Python Environment**: Package availability and versions
- **Directory Structure**: Required directories and permissions
- **Executables**: SWAN and other tool availability
- **Network Connectivity**: External service reachability
- **Credentials**: Authentication configuration
- **System Resources**: Memory, CPU, and disk space

## 📋 Environment Configuration

### Core Variables
```bash
# Container settings
TV_VERSION=latest
TV_CONTAINER_NAME=tuvalu-forecast-prod
TV_LOG_LEVEL=INFO

# Resource limits
TV_MEMORY_LIMIT=8G
TV_CPU_LIMIT=4
TV_MAX_PROCESSES=4

# Application settings
TV_EMAIL=0
TV_GUI=0
TV_DEBUG=0
```

### Data Paths
```bash
# Volume mount paths
TV_DATA_PATH=./runs
TV_ARCHIVES_PATH=./archives
TV_LOGS_PATH=./logs
# ... (see .env.production for complete list)
```

### Credentials
```bash
# Copernicus Marine Service
COPERNICUSMARINE_SERVICE_USERNAME=your_username
COPERNICUSMARINE_SERVICE_PASSWORD=your_password

# Email configuration
TV_SMTP_SERVER=smtp.example.com
TV_SMTP_USER=your_smtp_user
# ... (see .env.production for complete list)
```

## 🔄 Data Management

### Volume Strategy
The system uses named volumes with bind mounts for optimal performance:

- **Persistent Data**: `runs/`, `archives/`, `logs/`
- **Temporary Data**: `tmp/`, `Regional_tmp/`
- **Configuration**: `config/` (read-only mount)
- **Results**: `Regional_Output/`, `Hall_Reports/`

### Backup Strategy
```bash
# Manual backup
docker run --rm -v tuvalu_runs_data:/data -v $(pwd)/backup:/backup alpine \
  tar czf /backup/runs-$(date +%Y%m%d).tar.gz -C /data .

# Automated backup (configure in cron)
./tuvalu-manager.sh cleanup  # Includes optional backup
```

## 🚀 Deployment Scenarios

### Single Server Deployment
```bash
# Standard production deployment
./tuvalu-manager.sh start
./tuvalu-manager.sh schedule  # Enable automatic runs
```

### High Availability Deployment
```bash
# Multi-instance with load balancing
docker-compose up --scale tuvalu-forecast=3
```

### Development Deployment
```bash
# Development environment
./tuvalu-manager.sh dev
./tuvalu-manager.sh shell  # Interactive development
```

## 🔍 Troubleshooting

### Common Issues

#### Build Failures
```bash
# Check build context size
du -sh . --exclude=runs --exclude=archives

# Clean Docker cache
docker builder prune -a

# Rebuild from scratch
./tuvalu-manager.sh build
```

#### Runtime Issues
```bash
# Check container status
./tuvalu-manager.sh status

# View detailed logs
./tuvalu-manager.sh logs --tail 100

# Run health check
./tuvalu-manager.sh health
```

#### Performance Issues
```bash
# Check resource usage
docker stats

# Adjust resource limits in .env
TV_MEMORY_LIMIT=16G
TV_CPU_LIMIT=8
```

### Log Locations
- **Container logs**: `docker logs tuvalu-forecast`
- **Application logs**: `./logs/`
- **Health check logs**: `./logs/health.log`
- **Build logs**: Docker build output

## 📚 Best Practices

### Development Workflow
1. Use `tuvalu-manager.sh dev` for development
2. Test changes with `tuvalu-manager.sh test`
3. Build production image with `build-production.sh`
4. Deploy with `tuvalu-manager.sh start`

### Production Deployment
1. Use environment-specific `.env` files
2. Enable resource limits and health checks
3. Configure proper logging and monitoring
4. Implement backup strategies
5. Use `--profile production` for full deployment

### Security Practices
1. Never run containers as root
2. Use read-only containers where possible
3. Regularly update base images
4. Monitor security advisories
5. Implement proper secret management

## 📞 Support

For issues or questions:
1. Check the health status: `./tuvalu-manager.sh health`
2. Review logs: `./tuvalu-manager.sh logs`
3. Verify configuration: `./tuvalu-manager.sh info`
4. Test basic functionality: `./tuvalu-manager.sh test`

## 🔄 Updates

To update the system:
```bash
# Pull latest code
git pull

# Rebuild image
./tuvalu-manager.sh build

# Update deployment
./tuvalu-manager.sh restart
```

## 📈 Monitoring Integration

The system is designed to integrate with monitoring solutions:
- **Prometheus**: Health check endpoints
- **Grafana**: Dashboard templates
- **ELK Stack**: Structured logging
- **Nagios**: Service monitoring

For production deployments, consider implementing these monitoring solutions for comprehensive system oversight.
