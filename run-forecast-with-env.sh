#!/bin/bash

# =============================================================================
# Tuvalu Forecast Runner with Environment Variables
# Automatically loads .env file and runs forecast with proper credentials
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}🔷 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    print_status "Please create a .env file with your credentials"
    exit 1
fi

print_status "Loading environment variables from .env file..."

# Load environment variables from .env file
set -a  # automatically export all variables
source .env
set +a  # disable automatic export

print_status "Environment loaded successfully"
print_status "Copernicus Marine User: ${COPERNICUSMARINE_SERVICE_USERNAME:-'Not set'}"

# Check if Python environment exists
VENV_PATH="/media/judith/Big_Booty1/Tuvalu_Forecast/tuvalu_py39_env"
if [ ! -d "$VENV_PATH" ]; then
    print_error "Python virtual environment not found at $VENV_PATH"
    exit 1
fi

print_status "Activating Python environment..."
source "$VENV_PATH/bin/activate"

# Check if date parameter is provided
FORECAST_DATE="${1:-}"
if [ -n "$FORECAST_DATE" ]; then
    export TV_DATE="$FORECAST_DATE"
    print_status "Using forecast date: $TV_DATE"
else
    print_status "Using current date for forecast"
fi

print_status "🌊 Starting Tuvalu Forecast System..."
cd codes

# Run the forecast
python main_run_operational.py

print_success "🎉 Forecast completed successfully!"
