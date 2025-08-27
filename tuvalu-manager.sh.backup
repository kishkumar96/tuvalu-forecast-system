#!/bin/bash
# ===========================================================================cmcmd_build() {
    echo -e "${BLUE}🔨 Building Docker image (Niue-style)...${NC}"
    docker build -t tuvalu-forecast:latest .
    echo -e "${GREEN}✅ Docker image built: tuvalu-forecast:latest${NC}"
}

cmd_fix_permissions() {
    echo -e "${BLUE}🔧 Fixing permissions for native Python (like Niue)...${NC}"
    
    # Fix permissions for key directories
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
    
    echo -e "${GREEN}✅ Permissions fixed for user $CURRENT_USER${NC}"
}ll() {
    echo -e "${BLUE}🐚 Starting interactive Docker shell (Niue-style)...${NC}"
    
    if ! docker image inspect tuvalu-forecast:latest &>/dev/null; then
        echo -e "${RED}❌ Docker image not found${NC}"
        echo -e "${YELLOW}💡 Run: $0 build${NC}"
        return 1
    fi
    
    echo -e "${CYAN}🚀 Starting interactive shell (as user $USER_ID:$GROUP_ID)...${NC}"alu Forecast System - Simple Management Script (Niue-style)
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
    echo -e "${PURPLE}"
    echo "============================================================================="
    echo " 🌊 Tuvalu Forecast System - Simple Manager (Niue-style)"
    echo "============================================================================="
    echo -e "${NC}"
    echo "User: $CURRENT_USER (ID: $USER_ID:$GROUP_ID)"
    echo "Forecast Dir: $SCRIPT_DIR"
    echo ""
}

print_usage() {
    echo -e "${CYAN}Usage: $0 <command> [options]${NC}"
    echo ""
    echo -e "${BLUE}🌊 Forecast Commands:${NC}"
    echo "  forecast        Run a forecast"
    echo "    --date=YYYYMMDDHH    Set specific forecast date"
    echo "    --step=N            Run only specific step"  
    echo "    --native            Use native Python environment (recommended)"
    echo "    --docker            Use Docker mode"
    echo ""
    echo -e "${BLUE}🔧 Management Commands:${NC}"
    echo "  build           Build the Docker image"
    echo "  shell           Interactive Docker shell"
    echo "  status          Show system status"
    echo "  logs            Show logs"
    echo "  clean           Clean up Docker resources"
    echo ""
    echo -e "${BLUE}📋 Information Commands:${NC}"
    echo "  help            Show this help message"
    echo "  version         Show version information"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0 forecast --native --date 2025082500   # Run forecast natively (recommended)"
    echo "  $0 forecast --docker --date 2025082500   # Run forecast with Docker"
    echo "  $0 build                                 # Build Docker image"
    echo "  $0 status                                # Show system status"
}

check_prerequisites() {
    # Check Docker (only if Docker mode is used)
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}⚠️ Docker not found - Docker mode will not be available${NC}"
    fi
}

load_environment() {
    # Load environment
    if [[ -f "$ENV_FILE" ]]; then
        source "$ENV_FILE"
    else
        echo -e "${YELLOW}⚠️ No .env file found${NC}"
    fi
}

# === Command Functions ===
cmd_build() {
    echo -e "${BLUE}� Building Docker image...${NC}"
    docker build -t tuvalu-forecast:latest .
    echo -e "${GREEN}✅ Docker image built: tuvalu-forecast:latest${NC}"
}

cmd_shell() {
    echo -e "${BLUE}� Starting interactive Docker shell...${NC}"
    
    if ! docker image inspect tuvalu-forecast:latest &>/dev/null; then
        echo -e "${RED}❌ Docker image not found${NC}"
        echo -e "${YELLOW}� Run: $0 build${NC}"
        return 1
    fi
    
    docker run --rm -it \
        --user $USER_ID:$GROUP_ID \
        --env-file .env \
        -v "$PWD:/TuvaluForecast" \
        -v "$PWD/runs:/TuvaluForecast/runs" \
        -v "$PWD/logs:/TuvaluForecast/logs" \
        -v "$PWD/tmp:/TuvaluForecast/tmp" \
        -v "$PWD/archives:/TuvaluForecast/archives" \
        -v "$PWD/Regional_Output:/TuvaluForecast/Regional_Output" \
        -v "$PWD/.copernicusmarine:/root/.copernicusmarine" \
        -v "$PWD/.env:/TuvaluForecast/.env" \
        -w /TuvaluForecast/codes \
        tuvalu-forecast:latest \
        /bin/bash
}

cmd_status() {
    echo -e "${BLUE}📊 System Status:${NC}"
    echo "=============="
    
    # Check Docker image
    if docker image inspect tuvalu-forecast:latest &>/dev/null; then
        echo "✓ Docker image exists: tuvalu-forecast:latest"
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

cmd_logs() {
    echo -e "${BLUE}� Recent logs:${NC}"
    
    if [[ -d "$SCRIPT_DIR/logs" ]]; then
        ls -la "$SCRIPT_DIR/logs/" | head -10
        echo ""
        echo "Latest log entries:"
        tail -20 "$SCRIPT_DIR/logs"/*.log 2>/dev/null || echo "No log files found"
    else
        echo "No logs directory found"
    fi
}

cmd_clean() {
    echo -e "${BLUE}🧹 Cleaning up Docker resources...${NC}"
    
    # Remove stopped containers
    docker container prune -f
    
    # Remove unused images (with confirmation)
    echo "Remove unused Docker images? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        docker image prune -f
    fi
    
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

cmd_forecast() {
    local args=("$@")
    echo -e "${BLUE}🌊 Running forecast...${NC}"
    
    # Parse arguments
    local date_arg=""
    local step_arg=""
    local native_mode=true  # Default to native mode
    local docker_mode=false
    
    for arg in "${args[@]}"; do
        case $arg in
            --date=*)
                date_arg="${arg#*=}"
                ;;
            --step=*)
                step_arg="${arg#*=}"
                ;;
            --native)
                native_mode=true
                docker_mode=false
                ;;
            --docker)
                native_mode=false
                docker_mode=true
                ;;
        esac
    done
    
    # Docker mode
    if [[ "$docker_mode" == true ]]; then
        echo -e "${CYAN}🐳 Using Docker mode (Niue-style)...${NC}"
        
        # Check if image exists
        if ! docker image inspect tuvalu-forecast:latest &>/dev/null; then
            echo -e "${RED}❌ Docker image not found${NC}"
            echo -e "${YELLOW}💡 Run: $0 build${NC}"
            return 1
        fi
        
        # Set environment variables
        local env_args=""
        if [[ -n "$date_arg" ]]; then
            env_args="-e TV_DATE=$date_arg"
            echo -e "${CYAN}📅 Using forecast date: $date_arg${NC}"
        fi
        if [[ -n "$step_arg" ]]; then
            env_args="$env_args -e TV_STEP=$step_arg"
            echo -e "${CYAN}🔢 Running specific step: $step_arg${NC}"
        fi
        
        # Load environment file if it exists
        if [[ -f ".env" ]]; then
            env_args="$env_args --env-file .env"
        fi
        
        # Run Docker directly like Niue (no compose)
        echo -e "${CYAN}🚀 Starting Docker forecast (as user $USER_ID:$GROUP_ID)...${NC}"
        docker run --rm -it \
            --user $USER_ID:$GROUP_ID \
            $env_args \
            -v "$PWD:/TuvaluForecast" \
            -v "$PWD/runs:/TuvaluForecast/runs" \
            -v "$PWD/logs:/TuvaluForecast/logs" \
            -v "$PWD/tmp:/TuvaluForecast/tmp" \
            -v "$PWD/archives:/TuvaluForecast/archives" \
            -v "$PWD/Regional_Output:/TuvaluForecast/Regional_Output" \
            -v "$PWD/.copernicusmarine:/root/.copernicusmarine" \
            -v "$PWD/.env:/TuvaluForecast/.env" \
            -w /TuvaluForecast/codes \
            tuvalu-forecast:latest \
            python main_run_operational.py
        return
    fi
    
    # Native mode (default)
    echo -e "${CYAN}🐍 Running in native Python environment...${NC}"
    
    # Check if virtual environment exists
    local venv_path="/media/judith/Big_Booty1/Tuvalu_Forecast/tuvalu_py39_env"
    if [[ ! -d "$venv_path" ]]; then
        echo -e "${RED}❌ Python virtual environment not found at $venv_path${NC}"
        return 1
    fi
    
    # Load environment variables
    if [[ -f "$ENV_FILE" ]]; then
        echo -e "${CYAN}📋 Loading environment variables...${NC}"
        set -a
        source "$ENV_FILE"
        set +a
    fi
    
    # Set forecast date if provided
    if [[ -n "$date_arg" ]]; then
        export TV_DATE="$date_arg"
        echo -e "${CYAN}📅 Using forecast date: $TV_DATE${NC}"
    fi
    
    if [[ -n "$step_arg" ]]; then
        export TV_STEP="$step_arg"
        echo -e "${CYAN}🔢 Running specific step: $TV_STEP${NC}"
    fi
    
    # Activate virtual environment and run forecast
    echo -e "${CYAN}🚀 Starting forecast...${NC}"
    (
        source "$venv_path/bin/activate"
        cd "$SCRIPT_DIR/codes"
        python main_run_operational.py
    )
}

cmd_help() {
    echo -e "${BLUE}📖 Tuvalu Forecast System - Niue-style Management${NC}"
    echo ""
    echo -e "${CYAN}Basic Commands:${NC}"
    echo "  build             Build Docker image"
    echo "  forecast          Run forecast (--native or --docker, --date=YYYYMMDDHH, --step=N)"
    echo "  shell             Start interactive Docker shell (as current user)"
    echo "  status            Show system status"
    echo "  logs              Show recent logs" 
    echo "  fix-permissions   Fix permissions for native Python (like Niue)"
    echo "  clean             Clean up Docker resources"
    echo "  version           Show version information"
    echo "  help              Show this help message"
    echo ""
    echo -e "${CYAN}Examples:${NC}"
    echo "  $0 build                           # Build Docker image"
    echo "  $0 fix-permissions                 # Fix permissions for native mode"
    echo "  $0 forecast                        # Run forecast (native mode, recommended)"
    echo "  $0 forecast --docker               # Run forecast in Docker (as current user)"
    echo "  $0 forecast --date=2025082100      # Run forecast for specific date"
    echo "  $0 shell                           # Interactive Docker shell"
    echo "  $0 status                          # Check system status"
}

# === Main Execution ===
main() {
    print_header
    
    check_prerequisites
    load_environment
    
    local command="${1:-}"
    shift || true
    
    case "$command" in
        build)              cmd_build "$@" ;;
        forecast)           cmd_forecast "$@" ;;
        shell)              cmd_shell "$@" ;;
        status)             cmd_status "$@" ;;
        logs)               cmd_logs "$@" ;;
        fix-permissions)    cmd_fix_permissions "$@" ;;
        clean)              cmd_clean "$@" ;;
        version)            echo "Tuvalu Forecast System - Niue-style v1.0" ;;
        help|--help|-h)     cmd_help ;;
        "")                 cmd_help ;;
        *)              
            echo -e "${RED}❌ Unknown command: $command${NC}"
            echo ""
            cmd_help
            exit 1
            ;;
    esac
}

# Execute main function
main "$@"
