#!/bin/bash
# =============================================================================
# Tuvalu Forecast System - Niue-style Management Script
# Simple management interface following Niue approach exactly
# =============================================================================

set -euo pipefail

# === Configuration ===
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${SCRIPT_DIR}/.env"

# Get current user info (like Niue)
USER_ID=$(id -u)
GROUP_ID=$(id -g)
CURRENT_USER=$(id -un)

# === Colors ===
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# === Functions ===
print_header() {
    echo "Tuvalu Forecast System - Niue-style Setup"
    echo "=========================================="
    echo "User: $CURRENT_USER (ID: $USER_ID:$GROUP_ID)"
    echo "Forecast Dir: $SCRIPT_DIR"
    echo ""
}

# Function to fix permissions (like Niue)
fix_permissions() {
    echo "Fixing permissions for native Python..."
    local dirs_to_fix=("$SCRIPT_DIR/runs" "$SCRIPT_DIR/logs" "$SCRIPT_DIR/tmp" "$SCRIPT_DIR/archives" "$SCRIPT_DIR/Regional_Output")
    
    for dir in "${dirs_to_fix[@]}"; do
        if [[ -d "$dir" ]]; then
            if [[ $EUID -eq 0 ]]; then
                chown -R $USER_ID:$GROUP_ID "$dir"
                echo "✓ Fixed permissions for $dir"
            else
                echo "Need sudo to fix permissions for $dir:"
                sudo chown -R $USER_ID:$GROUP_ID "$dir"
                echo "✓ Fixed permissions for $dir"
            fi
        else
            mkdir -p "$dir"
            chown $USER_ID:$GROUP_ID "$dir" 2>/dev/null || sudo chown $USER_ID:$GROUP_ID "$dir"
            echo "✓ Created and fixed permissions for $dir"
        fi
    done
    echo "✓ Permissions fixed"
}

# Function to build Docker image
build_docker() {
    echo "Building Docker image..."
    cd "$SCRIPT_DIR"
    docker build -t tuvalu-forecast:latest .
    echo "✓ Docker image built: tuvalu-forecast:latest"
}

# Function to run with Docker (as user)
run_docker() {
    echo "Running forecast with Docker (as user $USER_ID:$GROUP_ID)..."
    
    # Check if image exists
    if ! docker image inspect tuvalu-forecast:latest &>/dev/null; then
        echo "❌ Docker image not found"
        echo "💡 Run: $0 build-docker"
        return 1
    fi
    
    # Load environment file if it exists
    local env_args=""
    if [[ -f ".env" ]]; then
        env_args="--env-file .env"
    fi
    
    docker run --rm -it \
        --user $USER_ID:$GROUP_ID \
        $env_args \
        -v "$SCRIPT_DIR:/TuvaluForecast" \
        -v "$SCRIPT_DIR/runs:/TuvaluForecast/runs" \
        -v "$SCRIPT_DIR/logs:/TuvaluForecast/logs" \
        -v "$SCRIPT_DIR/tmp:/TuvaluForecast/tmp" \
        -v "$SCRIPT_DIR/archives:/TuvaluForecast/archives" \
        -v "$SCRIPT_DIR/Regional_Output:/TuvaluForecast/Regional_Output" \
        -v "$SCRIPT_DIR/.copernicusmarine:/root/.copernicusmarine" \
        -w /TuvaluForecast/codes \
        tuvalu-forecast:latest \
        python main_run_operational.py
}

# Function to run native Python
run_native() {
    echo "Running forecast with native Python..."
    
    # Check if virtual environment exists
    local venv_path="/media/judith/Big_Booty1/Tuvalu_Forecast/tuvalu_py39_env"
    if [[ ! -d "$venv_path" ]]; then
        echo "❌ Python virtual environment not found at $venv_path"
        return 1
    fi
    
    # Load environment variables if file exists
    if [[ -f "$ENV_FILE" ]]; then
        echo "📋 Loading environment variables..."
        set -a
        source "$ENV_FILE"
        set +a
    fi
    
    # Activate virtual environment and run
    echo "🚀 Starting native forecast..."
    (
        source "$venv_path/bin/activate"
        cd "$SCRIPT_DIR/codes"
        python main_run_operational.py
    )
}

# Function to start interactive Docker shell
run_shell() {
    echo "Starting interactive Docker shell (as user $USER_ID:$GROUP_ID)..."
    
    if ! docker image inspect tuvalu-forecast:latest &>/dev/null; then
        echo "❌ Docker image not found"
        echo "💡 Run: $0 build-docker"
        return 1
    fi
    
    local env_args=""
    if [[ -f ".env" ]]; then
        env_args="--env-file .env"
    fi
    
    docker run --rm -it \
        --user $USER_ID:$GROUP_ID \
        $env_args \
        -v "$SCRIPT_DIR:/TuvaluForecast" \
        -v "$SCRIPT_DIR/runs:/TuvaluForecast/runs" \
        -v "$SCRIPT_DIR/logs:/TuvaluForecast/logs" \
        -v "$SCRIPT_DIR/tmp:/TuvaluForecast/tmp" \
        -v "$SCRIPT_DIR/archives:/TuvaluForecast/archives" \
        -v "$SCRIPT_DIR/Regional_Output:/TuvaluForecast/Regional_Output" \
        -v "$SCRIPT_DIR/.copernicusmarine:/root/.copernicusmarine" \
        -w /TuvaluForecast/codes \
        tuvalu-forecast:latest \
        /bin/bash
}

# Function to show status
show_status() {
    echo "System Status:"
    echo "=============="
    
    # Check Docker image
    if docker image inspect tuvalu-forecast:latest &>/dev/null; then
        echo "✓ Docker image exists: tuvalu-forecast:latest"
    else
        echo "❌ Docker image not found. Run '$0 build-docker' first."
    fi
    
    # Check native environment
    local venv_path="/media/judith/Big_Booty1/Tuvalu_Forecast/tuvalu_py39_env"
    if [[ -d "$venv_path" ]]; then
        echo "✓ Native Python environment exists"
    else
        echo "❌ Native Python environment not found"
    fi
    
    # Check environment file
    if [[ -f "$ENV_FILE" ]]; then
        echo "✓ Environment file exists"
    else
        echo "❌ Environment file not found"
    fi
    
    # Check recent runs
    echo ""
    echo "Recent runs:"
    ls -la "$SCRIPT_DIR/runs/" 2>/dev/null | tail -5 || echo "No runs found"
}

# Main menu (like Niue)
print_header

case "${1:-menu}" in
    "fix-permissions")
        fix_permissions
        ;;
    "build-docker")
        build_docker
        ;;
    "docker")
        run_docker
        ;;
    "native")
        run_native
        ;;
    "shell")
        run_shell
        ;;
    "status")
        show_status
        ;;
    "menu"|"help"|*)
        echo "Available commands:"
        echo "  fix-permissions   - Fix permissions for native Python (like Niue)"
        echo "  build-docker      - Build Docker image"
        echo "  docker            - Run forecast with Docker (as current user)"
        echo "  native            - Run forecast with native Python (recommended)"
        echo "  shell             - Start interactive Docker shell"
        echo "  status            - Show system status"
        echo ""
        echo "Examples:"
        echo "  $0 fix-permissions"
        echo "  $0 native"
        echo "  $0 docker"
        echo "  $0 status"
        ;;
esac
