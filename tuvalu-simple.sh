#!/bin/bash

# Tuvalu Forecast System - Simple Docker Setup
# This script provides a simple way to run the forecast system

set -e

# Get current user info
USER_ID=$(id -u)
GROUP_ID=$(id -g)
CURRENT_USER=$(id -un)

# Base paths
FORECAST_DIR="/media/judith/Big_Booty1/Tuvalu_Forecast/tailored-report-tv"

echo "Tuvalu Forecast System - Simple Setup"
echo "====================================="
echo "User: $CURRENT_USER (ID: $USER_ID:$GROUP_ID)"
echo "Forecast Dir: $FORECAST_DIR"
echo ""

# Function to show usage
usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  build       Build the simple Docker image"
    echo "  run         Run forecast with Docker"
    echo "  native      Run forecast natively (Python venv)"
    echo "  shell       Open Docker shell"
    echo "  forecast    Run forecast with date (--date=YYYYMMDDHH)"
    echo "  status      Show system status"
    echo "  logs        Show logs"
    echo "  clean       Clean up Docker resources"
    echo ""
    echo "Examples:"
    echo "  $0 build                         # Build Docker image"
    echo "  $0 forecast --date=2025082500    # Run forecast for specific date"
    echo "  $0 native --date=2025082500      # Run natively"
    echo "  $0 shell                         # Open interactive shell"
}

# Function to build simple Docker image
build_simple() {
    echo "Building simple Docker image..."
    cd "$FORECAST_DIR"
    docker build -f Dockerfile.simple -t tuvalu-forecast-simple:latest .
    echo "✓ Simple Docker image built: tuvalu-forecast-simple:latest"
}

# Function to run with simple Docker
run_docker_simple() {
    local date_arg=""
    
    # Parse arguments
    for arg in "$@"; do
        case $arg in
            --date=*)
                date_arg="${arg#*=}"
                ;;
        esac
    done
    
    echo "Running forecast with simple Docker..."
    cd "$FORECAST_DIR"
    
    # Set environment variables
    local env_args=""
    if [[ -n "$date_arg" ]]; then
        env_args="-e TV_DATE=$date_arg"
        echo "Using forecast date: $date_arg"
    fi
    
    # Load environment file if it exists
    if [[ -f ".env" ]]; then
        env_args="$env_args --env-file .env"
    fi
    
    docker run --rm -it \
        $env_args \
        -v "$PWD/runs:/TuvaluForecast/runs" \
        -v "$PWD/logs:/TuvaluForecast/logs" \
        -v "$PWD/tmp:/TuvaluForecast/tmp" \
        -v "$PWD/archives:/TuvaluForecast/archives" \
        -v "$PWD/Regional_Output:/TuvaluForecast/Regional_Output" \
        -v "$PWD/.copernicusmarine:/root/.copernicusmarine" \
        -v "$PWD/.env:/TuvaluForecast/.env" \
        tuvalu-forecast-simple:latest \
        python main_run_operational.py
}

# Function to run natively
run_native() {
    local date_arg=""
    
    # Parse arguments
    for arg in "$@"; do
        case $arg in
            --date=*)
                date_arg="${arg#*=}"
                ;;
        esac
    done
    
    echo "Running forecast natively..."
    
    # Check virtual environment
    local venv_path="/media/judith/Big_Booty1/Tuvalu_Forecast/tuvalu_py39_env"
    if [[ ! -d "$venv_path" ]]; then
        echo "❌ Python virtual environment not found at $venv_path"
        exit 1
    fi
    
    # Load environment variables
    if [[ -f "$FORECAST_DIR/.env" ]]; then
        echo "Loading environment variables..."
        set -a
        source "$FORECAST_DIR/.env"
        set +a
    fi
    
    # Set forecast date if provided
    if [[ -n "$date_arg" ]]; then
        export TV_DATE="$date_arg"
        echo "Using forecast date: $TV_DATE"
    fi
    
    # Run forecast
    (
        source "$venv_path/bin/activate"
        cd "$FORECAST_DIR/codes"
        python main_run_operational.py
    )
}

# Function to open Docker shell
run_shell() {
    echo "Opening Docker shell..."
    cd "$FORECAST_DIR"
    
    docker run --rm -it \
        --env-file .env \
        -v "$PWD/runs:/TuvaluForecast/runs" \
        -v "$PWD/logs:/TuvaluForecast/logs" \
        -v "$PWD/tmp:/TuvaluForecast/tmp" \
        -v "$PWD/archives:/TuvaluForecast/archives" \
        -v "$PWD/Regional_Output:/TuvaluForecast/Regional_Output" \
        -v "$PWD/.copernicusmarine:/root/.copernicusmarine" \
        -v "$PWD/.env:/TuvaluForecast/.env" \
        tuvalu-forecast-simple:latest \
        /bin/bash
}

# Function to show status
show_status() {
    echo "System Status:"
    echo "=============="
    
    # Check Docker image
    if docker image inspect tuvalu-forecast-simple:latest &>/dev/null; then
        echo "✓ Docker image exists: tuvalu-forecast-simple:latest"
    else
        echo "❌ Docker image not found. Run '$0 build' first."
    fi
    
    # Check native environment
    local venv_path="/media/judith/Big_Booty1/Tuvalu_Forecast/tuvalu_py39_env"
    if [[ -d "$venv_path" ]]; then
        echo "✓ Native Python environment exists"
    else
        echo "❌ Native Python environment not found"
    fi
    
    # Check environment file
    if [[ -f "$FORECAST_DIR/.env" ]]; then
        echo "✓ Environment file exists"
    else
        echo "❌ Environment file not found"
    fi
    
    # Check recent runs
    echo ""
    echo "Recent runs:"
    ls -la "$FORECAST_DIR/runs/" 2>/dev/null | tail -5 || echo "No runs found"
}

# Function to show logs
show_logs() {
    echo "Recent logs:"
    echo "============"
    
    if [[ -d "$FORECAST_DIR/logs" ]]; then
        ls -la "$FORECAST_DIR/logs/" | head -10
        echo ""
        echo "Latest log entries:"
        tail -20 "$FORECAST_DIR/logs"/*.log 2>/dev/null || echo "No log files found"
    else
        echo "No logs directory found"
    fi
}

# Function to clean up
clean_docker() {
    echo "Cleaning up Docker resources..."
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove unused images (with confirmation)
    echo "Remove unused Docker images? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        docker image prune -f
    fi
    
    echo "✓ Cleanup completed"
}

# Main execution
case "${1:-}" in
    build)
        build_simple
        ;;
    run)
        shift
        run_docker_simple "$@"
        ;;
    native)
        shift
        run_native "$@"
        ;;
    forecast)
        shift
        # Default to native mode (which we know works)
        run_native "$@"
        ;;
    shell)
        run_shell
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_docker
        ;;
    help|--help|-h|"")
        usage
        ;;
    *)
        echo "Unknown command: $1"
        echo ""
        usage
        exit 1
        ;;
esac
