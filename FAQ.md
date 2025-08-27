# Frequently Asked Questions (FAQ)

## 🔧 **Installation & Setup**

### **Q: What are the minimum system requirements?**
**A:** 
- **CPU**: 4+ cores (8+ recommended)
- **RAM**: 8GB minimum (16GB+ recommended)  
- **Storage**: 50GB+ available space
- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2

### **Q: How long does initial setup take?**
**A:** 
- **Quick setup**: 5-10 minutes using existing conda environment
- **Full setup**: 30-60 minutes including all dependencies
- **New team member**: 30 minutes with onboarding guide

### **Q: Can I run this on Windows?**
**A:** Yes! Use Windows Subsystem for Linux (WSL2) with Ubuntu. Native Windows support is limited but functional.

## 🌊 **Forecasting Operations**

### **Q: How often should I run forecasts?**
**A:** 
- **Production**: Every 6 hours (00, 06, 12, 18 UTC) - automated via cron
- **Development**: On-demand as needed
- **Emergency**: Any time with custom date/time parameters

### **Q: What if a forecast run fails?**
**A:** 
1. **Resume**: Use `./deploy.sh --resume` to continue from last successful step
2. **Debug**: Enable debug mode with `TV_DEBUG=1 ./deploy.sh --step N`  
3. **Force re-run**: Use `--force` flag to re-run completed steps
4. **Check logs**: Review `logs/forecast_YYYYMMDD.log` for errors

### **Q: How long does a full forecast take?**
**A:**
- **Steps 1-5** (Data download): 10-30 minutes (depends on internet)
- **Step 6** (Model run): 30-90 minutes (depends on CPU)
- **Steps 7-12** (Processing): 10-20 minutes
- **Total**: 1-2.5 hours typically

### **Q: Can I run individual steps?**
**A:** Yes! Use `--step N` for single steps or `--steps 1 2 3` for multiple:
```bash
./deploy.sh --step 1    # Download weather data only
./deploy.sh --steps 8 9 10  # Inundation + archive + regional
```

## 💾 **Data & Storage**

### **Q: How much disk space is used?**
**A:**
- **Per forecast run**: 2-5GB
- **Archived data**: Grows ~10GB/month with 6-hour cycles
- **Persistent data**: ~20GB (reused across runs)
- **Docker cleanup**: Use `docker system prune -a -f --volumes` to reclaim space

### **Q: Where is forecast data stored?**
**A:**
- **Current run**: `runs/YYYYMMDDHH/`
- **Archives**: `archives/YYYYMMDDHH/` (compressed)
- **Reports**: `Hall_Reports/`
- **Persistent**: `persistent_data/` (shared across runs)

### **Q: How do I backup forecast data?**
**A:** Key directories to backup:
```bash
persistent_data/    # Persistent forecast data
archives/          # Historical forecasts  
Hall_Reports/      # Generated reports
config.*.yml       # Configuration files
```

## 🔄 **Automation & Scheduling**

### **Q: How do I setup automated forecasts?**
**A:** Use the provided scheduler:
```bash
chmod +x 6h_scheduler.sh
./6h_scheduler.sh    # Sets up cron for 6-hour cycles
```

### **Q: Can I change the forecast schedule?**
**A:** Yes! Edit cron entries:
```bash
crontab -e
# Change from 6-hour to different schedule
0 */12 * * * cd /path/to/forecast && ./cycle_manager.sh
```

### **Q: How do I monitor automated runs?**
**A:**
- **Health checks**: `./health_check.sh`
- **Efficiency monitoring**: `./efficiency_monitor.sh`
- **Logs**: `logs/forecast_YYYYMMDD.log`
- **Run status**: Check `runs/` directory for latest

## 🐳 **Docker & Containers**

### **Q: Should I use Docker or native installation?**
**A:**
- **Docker**: Better for production, isolation, portability
- **Native**: Better for development, debugging, customization
- **Both**: Docker for production, native for development

### **Q: How do I update the Docker container?**
**A:**
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### **Q: Docker is using too much space, what do I do?**
**A:** Regular cleanup:
```bash
docker system df                    # Check usage
docker system prune -a -f --volumes  # Clean everything
```

## 👥 **Team & Scaling**

### **Q: How do I onboard new team members?**
**A:** Follow the [TEAM_ONBOARDING.md](TEAM_ONBOARDING.md) guide:
1. System prerequisites check
2. Quick start (5 minutes)
3. Development setup (15 minutes) 
4. Role-specific training

### **Q: Can multiple people work on this simultaneously?**
**A:** Yes! The system supports:
- **Shared environment**: Common conda environment
- **Individual development**: Personal branches/configs
- **Production isolation**: Dedicated production environment

### **Q: How do I scale to multiple regions?**
**A:** Use multi-environment configuration:
```bash
# Copy and modify config
cp config.multi-env.yml config.region2.yml
# Deploy with custom config
./deploy.sh --config config.region2.yml
```

## ⚠️ **Common Issues & Solutions**

### **Q: "ModuleNotFoundError" when running forecast**
**A:**
1. **Activate environment**: `conda activate Tuvalu_EWS_new`
2. **Check installation**: `conda list`
3. **Reinstall dependencies**: `conda env update -f environment.yml`

### **Q: Download steps fail with network errors**
**A:**
1. **Check internet connection**: `ping google.com`
2. **Check credentials**: Verify CMEMS login for Step 2
3. **Retry**: Use `--force --step N` to retry specific step
4. **Proxy**: Configure HTTP_PROXY if behind firewall

### **Q: SWAN model fails to run (Step 6)**
**A:**
1. **Check executables**: Ensure `executables/swan.exe` exists and is executable
2. **Check inputs**: Verify steps 1-5 completed successfully
3. **Check resources**: Ensure sufficient CPU/memory
4. **Debug mode**: `TV_DEBUG=1 ./deploy.sh --step 6`

### **Q: Email notifications not working**
**A:**
1. **Enable email**: `TV_EMAIL=1 ./deploy.sh`
2. **Check config**: Verify email settings in `tcap_mailer.py`
3. **Test connection**: Check SMTP server accessibility

### **Q: GUI features not working**
**A:**
- **Linux**: GUI features are limited on Linux systems
- **Enable**: Use `TV_GUI=1` environment variable
- **Alternative**: Use web interface or command line tools

## 🚀 **Performance & Optimization**

### **Q: How can I make forecasts run faster?**
**A:**
1. **More CPU cores**: SWAN model benefits from parallel processing
2. **Faster storage**: SSD storage significantly helps
3. **Better internet**: Speeds up data download steps
4. **Selective steps**: Run only necessary steps with `--steps`

### **Q: System is using too much memory**
**A:**
1. **Check processes**: `htop` or `ps aux`
2. **Increase swap**: If system has insufficient RAM
3. **Cleanup**: Remove old run directories
4. **Docker limits**: Set memory limits in docker-compose.yml

### **Q: How do I optimize for production?**
**A:** Follow [ENTERPRISE_READINESS.md](ENTERPRISE_READINESS.md):
1. **6-hour cycles**: Optimal efficiency balance
2. **Persistent storage**: Reuse data across runs  
3. **Resource monitoring**: Use efficiency monitoring
4. **Automated cleanup**: Regular Docker and file cleanup

## 📞 **Getting Help**

### **Q: Where can I get more detailed help?**
**A:** Documentation hierarchy:
1. **Quick issues**: This FAQ
2. **Getting started**: [QUICKSTART.md](QUICKSTART.md)
3. **Full deployment**: [DEPLOYMENT.md](DEPLOYMENT.md) 
4. **Team onboarding**: [TEAM_ONBOARDING.md](TEAM_ONBOARDING.md)
5. **Troubleshooting**: Check logs in `logs/` directory

### **Q: How do I report bugs or request features?**
**A:**
1. **Check logs**: Review error logs first
2. **Test framework**: Run `./test_framework.sh` to identify issues
3. **Debug mode**: Enable with `TV_DEBUG=1`
4. **Document issue**: Include logs, config, and reproduction steps

### **Q: Is there a support community?**
**A:** The system includes comprehensive documentation and troubleshooting guides. For complex issues:
1. **Test framework**: Automated issue detection
2. **Health checks**: System validation tools
3. **Monitoring**: Built-in efficiency and performance monitoring
