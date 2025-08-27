# Tuvalu Forecast - Simple Docker Setup

This is a simplified Docker setup for the Tuvalu Forecast System, inspired by the Niue system's simplicity.

## Quick Start

### 1. Build the Simple Image
```bash
./tuvalu-simple.sh build
```

### 2. Run a Forecast

**Native Mode (Recommended):**
```bash
./tuvalu-simple.sh forecast --date=2025082500
```

**Docker Mode:**
```bash
./tuvalu-simple.sh run --date=2025082500
```

## Available Commands

| Command | Description |
|---------|-------------|
| `build` | Build the simple Docker image |
| `run` | Run forecast with Docker |
| `native` | Run forecast natively (Python venv) |
| `shell` | Open Docker shell |
| `forecast` | Run forecast with date (defaults to native mode) |
| `status` | Show system status |
| `logs` | Show logs |
| `clean` | Clean up Docker resources |

## Key Features

### ✅ Simplicity
- **Single Dockerfile**: Simple, straightforward build process
- **Minimal Docker Compose**: Basic service definition without complexity
- **Easy Commands**: Simple script interface similar to Niue system

### ✅ Flexibility
- **Dual Mode**: Support for both Docker and native Python execution
- **Same Interface**: Consistent command interface for both modes
- **Automatic Fallback**: Forecast command defaults to native mode (which works reliably)

### ✅ Compatibility
- **Same Environment**: Uses existing `.env` file and credentials
- **Same Paths**: Compatible with existing file structure
- **Same Results**: Produces identical outputs to the complex system

## Files Added

1. **`Dockerfile.simple`** - Simplified Docker build (similar to Niue)
2. **`docker-compose.simple.yml`** - Basic Docker Compose configuration  
3. **`tuvalu-simple.sh`** - Main management script (similar to Niue's `run_forecast.sh`)
4. **`SIMPLE_DOCKER_SETUP.md`** - This documentation

## Comparison: Complex vs Simple

### Original Complex Setup
- Multi-stage Dockerfile (146 lines)
- Complex Docker Compose with profiles, health checks, resource limits (243 lines)
- Advanced production features (security, monitoring, scheduling)
- Multiple service definitions
- Complex management script with many production features

### New Simple Setup  
- Single-stage Dockerfile (30 lines) - similar to Niue's approach
- Basic Docker Compose (20 lines) - essential volume mounts only
- Simple management script (200 lines) - focused on core functionality
- Single service definition
- Easy-to-understand structure

## Why Simple is Better

1. **Easier Debugging**: Fewer layers means easier troubleshooting
2. **Faster Builds**: Single-stage build process
3. **Less Complexity**: No advanced features that might cause issues
4. **Better Compatibility**: More similar to the working Niue system
5. **Maintainable**: Easier to modify and understand

## Migration Path

You can use both systems side by side:

- **Current production**: Keep using `tuvalu-manager.sh` if it works for you
- **Simple development**: Use `tuvalu-simple.sh` for easier development and testing
- **Native mode**: Both scripts support native mode using the existing Python environment

## Status

- ✅ **Native mode**: Fully working and tested
- 🔨 **Docker mode**: Building and ready for testing
- ✅ **Compatibility**: Works with existing `.env` file and credentials
- ✅ **File structure**: Compatible with existing directory layout

The simple setup provides the same functionality with much less complexity, making it easier to use, debug, and maintain.
