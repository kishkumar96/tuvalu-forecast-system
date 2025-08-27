# Tuvalu Forecast System - API Reference

## 📋 **Command Line Interface**

### **Main Script: `main_run_operational.py`**

```bash
python codes/main_run_operational.py [OPTIONS]
```

#### **Core Options**
| Option | Type | Description | Example |
|--------|------|-------------|---------|
| `--step N` | int | Run single step (1-15) | `--step 8` |
| `--steps N1 N2 N3` | int[] | Run multiple steps | `--steps 1 2 3 4` |
| `--date YYYYMMDDHH` | str | Override forecast date | `--date 2025081800` |
| `--hour H` | int | Override forecast hour (0,6,12,18) | `--hour 12` |

#### **Control Options**
| Option | Description | Example |
|--------|-------------|---------|
| `--force` | Force re-run completed steps | `--force --step 1` |
| `--resume` | Resume from last completed step | `--resume` |
| `--validate-only` | Only validate environment | `--validate-only` |
| `--no-email` | Disable email sending | `--no-email` |

#### **Configuration**
| Option | Default | Description |
|--------|---------|-------------|
| `--config FILE` | `tailored_report_config.json` | Custom config file |

### **Environment Variables**

| Variable | Default | Description |
|----------|---------|-------------|
| `TV_EMAIL` | `0` | Enable email sending (1=on, 0=off) |
| `TV_GUI` | `0` | Enable GUI features (1=on, 0=off) |
| `TV_DEBUG` | `0` | Enable debug logging (1=on, 0=off) |
| `TV_PRODUCTION` | `0` | Production mode (1=on, 0=off) |

## 🔧 **Deployment Scripts**

### **`deploy.sh` - Production Deployment**
```bash
./deploy.sh [OPTIONS]
```
- Wrapper around main script with environment setup
- Same options as `main_run_operational.py`
- Automatic environment validation

### **`health_check.sh` - System Validation**
```bash
./health_check.sh
```
- Comprehensive system health validation
- Environment dependency checking
- File permissions verification

### **`test_framework.sh` - Automated Testing**
```bash
./test_framework.sh [--unit|--integration|--system|--performance|--functional]
```

## 📊 **Forecast Steps Reference**

| Step | Name | Description | Dependencies |
|------|------|-------------|--------------|
| 1 | Download NCEP | GFS weather data | Internet |
| 2 | Download CMEMS | Ocean data | CMEMS credentials |
| 3 | Generate Tides | TPXO8 tidal predictions | TPXO8 data |
| 4 | Wave Forcing | Process wave data | Step 1,2 |
| 5 | Wind Forcing | Process wind data | Step 1 |
| 6 | Parallelize Run | Execute SWAN model | Steps 1-5 |
| 7 | Postprocess | Process model outputs | Step 6 |
| 8 | Inundation | Inundation forecasts | Step 7 |
| 9 | Archive | Archive outputs | Step 7 |
| 10 | Regional Data | Download regional data | Internet |
| 11 | Regional Analysis | Analyze regional data | Step 10 |
| 12 | Generate Reports | Create forecast reports | Steps 7,11 |
| 13 | GUI Setup | Setup GUI components | Step 12 |
| 14-15 | Extended | Future extensions | - |

## 🏗️ **System Architecture**

### **Directory Structure**
```
tailored-report-tv/
├── codes/                  # Python source code
├── common/                 # SWAN model files
├── executables/           # Binary executables
├── persistent_data/       # Persistent forecast data
├── logs/                  # System logs
├── runs/                  # Forecast run outputs
├── archives/              # Archived forecasts
└── Hall_Reports/          # Generated reports
```

### **Configuration Files**
- `config.production.yml` - Main production config
- `config.multi-env.yml` - Multi-environment config
- `tailored_report_config.json` - Forecast step config

## 🚀 **Quick Examples**

### **Basic Usage**
```bash
# Full forecast run
conda activate Tuvalu_EWS_new && ./deploy.sh

# Single step
./deploy.sh --step 8

# Multiple steps
./deploy.sh --steps 1 2 3 4

# Specific date
./deploy.sh --date 2025081800 --hour 12
```

### **Development**
```bash
# Debug mode
TV_DEBUG=1 ./deploy.sh --step 1

# Validate only
./deploy.sh --validate-only

# Resume from failure
./deploy.sh --resume
```

### **Testing**
```bash
# All tests
./test_framework.sh

# Specific test types
./test_framework.sh --unit
./test_framework.sh --integration
```

## 📚 **Exit Codes**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid arguments |
| 3 | Environment error |
| 4 | Data download error |
| 5 | Model execution error |

## 🔗 **Related Documentation**

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide  
- [TEAM_ONBOARDING.md](TEAM_ONBOARDING.md) - Team onboarding
- [SCALABILITY_ASSESSMENT.md](SCALABILITY_ASSESSMENT.md) - Scaling guide
- [ENTERPRISE_READINESS.md](ENTERPRISE_READINESS.md) - Enterprise features
