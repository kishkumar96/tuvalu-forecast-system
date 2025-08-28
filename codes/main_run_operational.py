# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 18:16:18 2021

@author: moritzw
This is the main script to run the forecast (step-configurable)
"""

import datetime as dt
from datetime import timedelta
import os
import shutil
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import logging
import sys
import time
import json
import platform

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
except ImportError:
    # If python-dotenv is not available, continue without it
    pass

# Import inundation forecast runner
from run_inundation_forecasts import run_inundation_forecasts
import sys
import argparse
import step1_download_NCEP as step1
import step2_download_CMEMS as step2
import step3_gen_tide_TPOX8 as step3
import step4_make_wave_forcing as step4
import step5_make_wind_forcing as step5
import step6_parallelize_run as step6
import step10_download_all_regional_data as step_10
import step10_ingest2GUI as step_10_gui
import step11_read_and_plot_all_regional_data as step_11
import step12_forecast_pts as step_12
import step13_GUIsetup as step_13
import step7_postprocess_output as step_7
import step9_archive_output as step9
import re

# Production configuration
PLATFORM = platform.system().lower()
EMAIL_ENABLED = os.environ.get("TV_EMAIL", "0") == "1"
GUI_ENABLED = os.environ.get("TV_GUI", "0") == "1"
DEBUG_MODE = os.environ.get("TV_DEBUG", "0") == "1"

# If you need to disable SSL verification (not recommended for production), set this environment variable:
os.environ['PYTHONHTTPSVERIFY'] = '0'

# The ROOT_DIR should point to the project's root directory.
# Handle both Docker (/app) and native environments
if os.path.exists('/app') and os.path.exists('/app/codes'):
    # Docker environment
    ROOT_DIR = os.environ.get("TV_ROOT", "/app")
else:
    # Native environment - use script location
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.environ.get("TV_ROOT") or default_root
    # Ensure ROOT_DIR is never empty
    if not ROOT_DIR or ROOT_DIR.strip() == "":
        ROOT_DIR = default_root

def setup_logging():
    """Setup structured logging for production"""
    log_level = logging.DEBUG if DEBUG_MODE else logging.INFO
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(ROOT_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Setup logging to both file and console
    handlers = [
        logging.FileHandler(os.path.join(log_dir, 'forecast.log')),
        logging.StreamHandler(sys.stdout)
    ]
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )
    
    # Also log to a daily rotating file
    from logging.handlers import TimedRotatingFileHandler
    daily_handler = TimedRotatingFileHandler(
        os.path.join(log_dir, 'daily.log'),
        when='midnight',
        interval=1,
        backupCount=7
    )
    daily_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(daily_handler)

logging.info(f"ROOT_DIR set to: {ROOT_DIR}")  # Debug print

def parse_arguments():
    parser = argparse.ArgumentParser(description='Tuvalu Forecast System - Production Ready')
    parser.add_argument('--step', type=int, choices=range(1, 16),
                        help='Run only a specific step (1-15)')
    parser.add_argument('--steps', nargs='+', type=int, choices=range(1, 16),
                        help='Run multiple specific steps (e.g., --steps 1 2 3)')
    parser.add_argument('--all', action='store_true',
                        help='Run all core steps (1-12). Convenience flag equivalent to default behavior when no specific step options are provided.')
    parser.add_argument('--date', type=str, 
                        help='Override forecast date (YYYYMMDDHH or YYYYMMDD)')
    parser.add_argument('--hour', type=int, choices=[0, 6, 12, 18],
                        help='Override forecast hour (if --date is YYYYMMDD)')
    parser.add_argument('--force', action='store_true',
                        help='Force re-run steps even if markers exist')
    parser.add_argument('--no-email', action='store_true',
                        help='Disable email sending (override TV_EMAIL)')
    parser.add_argument('--resume', action='store_true',
                        help='Resume from last successful step')
    parser.add_argument('--validate-only', action='store_true',
                        help='Only validate dependencies, don\'t run steps')
    parser.add_argument('--config', type=str, default="tailored_report_config.json",
                        help='Configuration file path')
    return parser.parse_args()

def list_available_runs(url):
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        connect=5, 
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount(url, adapter)
    
    try:
        logging.info(f"Fetching available runs from: {url}")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        x = soup.find_all('a')
        run_numbers = []
        for i in x:
            try:
                file_name = i.extract().get_text()
                # The run number from the website has a trailing '/', which needs to be removed.
                run_numbers.append(int(file_name.strip('/')))
            except (ValueError, AttributeError):
                continue
                
        logging.info(f"Found {len(run_numbers)} available runs: {sorted(run_numbers)}")
        return run_numbers
        
    except (requests.RequestException, AttributeError) as e:
        logging.error(f'Error downloading run list: {e}')
        return []
    finally:
        session.close()

def delete_ndaysbefore(current_time, ndays):
    folder_name = ROOT_DIR + '/runs/'
    if not os.path.exists(folder_name):
        logging.warning(f"Runs directory does not exist: {folder_name}")
        return
        
    flist = os.listdir(folder_name)
    date_pattern = re.compile(r'^\d{10}$')  # e.g., 2025081706
    deleted_count = 0
    
    for d in flist:
        if not date_pattern.match(d):
            continue  # Skip non-date directories
        try:
            rundate = dt.datetime.strptime(d + '0000', "%Y%m%d%H%M%S")
            if rundate < current_time - timedelta(days=ndays):
                run_dir = os.path.join(folder_name, d)
                shutil.rmtree(run_dir)
                logging.info(f"Deleted old run: {d}")
                deleted_count += 1
        except ValueError as ve:
            logging.error(f"Error parsing date for directory {d}: {ve}")
        except OSError as oe:
            logging.error(f"Error deleting directory {d}: {oe}")
    
    logging.info(f"Cleaned up {deleted_count} old run directories")
    return deleted_count

def step_marker_path(run_time, step_num):
    """Get the path to a step completion marker file"""
    run_dir = os.path.join(ROOT_DIR, 'runs', run_time.strftime('%Y%m%d%H'))
    return os.path.join(run_dir, f'.step{step_num:02d}.done')

def mark_step_complete(run_time, step_num):
    """Mark a step as completed"""
    marker_path = step_marker_path(run_time, step_num)
    os.makedirs(os.path.dirname(marker_path), exist_ok=True)
    
    with open(marker_path, 'w') as f:
        completion_info = {
            'completed_at': dt.datetime.utcnow().isoformat(),
            'step': step_num,
            'run_time': run_time.strftime('%Y%m%d%H'),
            'hostname': platform.node()
        }
        json.dump(completion_info, f, indent=2)
    
    logging.debug(f"Marked step {step_num} as complete: {marker_path}")

def is_step_complete(run_time, step_num):
    """Check if a step has been completed"""
    marker_path = step_marker_path(run_time, step_num)
    return os.path.exists(marker_path)

def get_last_completed_step(run_time):
    """Get the highest numbered completed step"""
    for step_num in range(15, 0, -1):  # Check from highest to lowest
        if is_step_complete(run_time, step_num):
            return step_num
    return 0

def validate_output_mat(run_time):
    """Validate the SWAN output.mat file"""
    run_dir = os.path.join(ROOT_DIR, 'runs', run_time.strftime('%Y%m%d%H'))
    output_mat = os.path.join(run_dir, 'output.mat')
    
    if not os.path.exists(output_mat):
        return False, "output.mat file does not exist"
    
    file_size = os.path.getsize(output_mat)
    min_size = 50 * 1024 * 1024  # 50MB minimum (reduced from 200MB for successful SWAN runs)
    
    if file_size < min_size:
        return False, f"output.mat too small: {file_size} bytes (minimum {min_size})"
    
    # Check file is not truncated by trying to read the header
    try:
        import scipy.io as sio
        info = sio.whosmat(output_mat)
        if not info:
            return False, "output.mat appears to be empty or corrupted"
    except Exception as e:
        return False, f"output.mat validation failed: {e}"
    
    logging.info(f"output.mat validation passed: {file_size} bytes")
    return True, "valid"

def validate_environment():
    """Validate the runtime environment"""
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python version too old: {sys.version}")
    
    # Check required directories
    for dir_name in ['runs', 'tmp', 'archives']:
        dir_path = os.path.join(ROOT_DIR, dir_name)
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path, exist_ok=True)
                logging.info(f"Created missing directory: {dir_path}")
            except OSError as e:
                issues.append(f"Cannot create directory {dir_path}: {e}")
    
    # Check disk space
    try:
        statvfs = os.statvfs(ROOT_DIR)
        free_space = statvfs.f_frsize * statvfs.f_bavail
        min_space = 10 * 1024 * 1024 * 1024  # 10GB
        
        if free_space < min_space:
            issues.append(f"Low disk space: {free_space / (1024**3):.1f}GB available")
        else:
            logging.info(f"Disk space OK: {free_space / (1024**3):.1f}GB available")
    except (OSError, AttributeError):
        logging.warning("Could not check disk space")
    
    # Check executables
    swan_exe = os.path.join(ROOT_DIR, 'executables', 'swan.exe')
    if not os.path.exists(swan_exe):
        issues.append(f"SWAN executable not found: {swan_exe}")
    
    return issues

def check_step_dependencies(step_num, run_time):
    """Check if required files exist for each step"""
    run_dir = f"{ROOT_DIR}/runs/{run_time.strftime('%Y%m%d%H')}"
    
    # Define step dependencies
    step_deps = {
        7: ['fort.14'],  # Post-process SWAN
        8: ['output.mat'],  # Inundation forecasts
        9: ['output.mat'],  # Archive output
        12: ['output.mat'],  # Hall's tailored forecast
    }
    
    if step_num in step_deps:
        for required_file in step_deps[step_num]:
            file_path = os.path.join(run_dir, required_file)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Step {step_num} requires {file_path}. Run previous steps first.")
            
            # Special validation for output.mat
            if required_file == 'output.mat':
                valid, msg = validate_output_mat(run_time)
                if not valid:
                    raise RuntimeError(f"Step {step_num} requires valid output.mat: {msg}")
    
    logging.debug(f"Dependencies check passed for step {step_num}")

if __name__ == "__main__":
    # Setup logging first
    setup_logging()
    
    start_time = time.time()
    logging.info("="*60)
    logging.info("Tuvalu Forecast System - Production Ready")
    logging.info("="*60)
    logging.info(f"ROOT_DIR: {ROOT_DIR}")
    logging.info(f"Platform: {PLATFORM}")
    logging.info(f"Email enabled: {EMAIL_ENABLED}")
    logging.info(f"GUI enabled: {GUI_ENABLED}")
    
    args = parse_arguments()
    
    # Validate environment
    env_issues = validate_environment()
    if env_issues:
        logging.error("Environment validation failed:")
        for issue in env_issues:
            logging.error(f"  - {issue}")
        if not args.validate_only:
            sys.exit(1)
    
    if args.validate_only:
        logging.info("Environment validation complete")
        sys.exit(0)
    
    # Override email settings if requested
    email_enabled = EMAIL_ENABLED and not args.no_email
    
    # Parse date override
    now = None
    runs = []
    
    if args.date:
        try:
            if len(args.date) == 10:  # YYYYMMDDHH
                now = dt.datetime.strptime(args.date, "%Y%m%d%H")
            elif len(args.date) == 8:  # YYYYMMDD
                hour = args.hour if args.hour is not None else 0
                now = dt.datetime.strptime(args.date, "%Y%m%d").replace(hour=hour)
            else:
                raise ValueError("Date must be YYYYMMDDHH or YYYYMMDD format")
            
            logging.info(f"🔧 Using override date: {now}")
            runs = [0, 6, 12, 18]  # Dummy runs for override mode
            
        except ValueError as e:
            logging.error(f"Invalid date format: {e}")
            sys.exit(1)
    else:
        # Normal mode - discover available runs
        try:
            now = dt.datetime.utcnow()
            runs_url = f'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfswave.pl?dir=%2Fgfs.{now.strftime("%Y%m%d")}'
            runs = list_available_runs(runs_url)
            
            if len(runs) == 0:
                logging.warning("No runs found for today, checking yesterday...")
                now = dt.datetime.utcnow() - timedelta(1)
                runs_url = f'https://nomads.ncep.noaa.gov/cgi-bin/filter_gfswave.pl?dir=%2Fgfs.{now.strftime("%Y%m%d")}'
                runs = list_available_runs(runs_url)
                
                if len(runs) == 0:
                    logging.error("ERROR: No runs available!")
                    sys.exit(1)
            
            runs = sorted(runs)
            now = now.replace(hour=runs[-1], minute=0, second=0, microsecond=0)
            logging.info(f"Using forecast run: {now} (hour: {runs[-1]:02d})")
            logging.info(f"Available runs: {runs}")
            
        except Exception as e:
            logging.error(f"Error discovering forecast runs: {e}")
            sys.exit(1)
    
    # Cleanup old runs
    try:
        deleted = delete_ndaysbefore(now, 14)
        logging.info(f"Cleanup completed, deleted {deleted} old runs")
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")
    
    # Determine steps to run
    steps_to_run = []
    
    if args.all and (args.step or args.steps):
        logging.warning("--all flag provided along with --step/--steps; ignoring --all and using explicit selection")

    if args.all:
        steps_to_run = list(range(1, 15))  # Updated to include all steps 1-14
    elif args.resume:
        last_step = get_last_completed_step(now)
        if last_step > 0:
            logging.info(f"Resuming from step {last_step + 1}")
            steps_to_run = list(range(last_step + 1, 15))  # Resume from next step
        else:
            logging.info("No completed steps found, starting from step 1")
            steps_to_run = list(range(1, 15))  # Updated to include all steps 1-14
    elif args.step:
        steps_to_run = [args.step]
    elif args.steps:
        steps_to_run = sorted(args.steps)  # Ensure proper ordering
    else:
        # Default: run all core steps (1-12), optionally including GUI steps on Windows
        if PLATFORM == "windows" and GUI_ENABLED:
            steps_to_run = list(range(1, 15))  # Include GUI steps on Windows
        else:
            steps_to_run = list(range(1, 13))   # Core steps only on Linux/Docker
    
    if not steps_to_run:
        logging.warning("No steps to run")
        sys.exit(0)
    
    logging.info(f"Steps to run: {steps_to_run}")
    
    # Validate step prerequisites
    for step_num in steps_to_run:
        if not args.force and is_step_complete(now, step_num):
            logging.info(f"Step {step_num} already completed (use --force to re-run)")
            continue
    
    success_count = 0
    failed_steps = []

    for step_num in steps_to_run:
        step_start_time = time.time()
        
        try:
            # Check if step already completed (unless forced)
            if not args.force and is_step_complete(now, step_num):
                logging.info(f"⏭️  Step {step_num} already completed, skipping (use --force to re-run)")
                success_count += 1
                continue
            
            # Check dependencies before running each step
            check_step_dependencies(step_num, now)
            
            logging.info(f"🚀 Starting Step {step_num}...")
            
            if step_num == 1:
                logging.info("Step 1: Downloading NCEP data...")
                step1.download_NCEP(now)
                logging.info("✅ Step 1 completed")
            elif step_num == 2:
                logging.info("Step 2: Downloading CMEMS data...")
                step2.download_CMEMS(now)
                logging.info("✅ Step 2 completed")
            elif step_num == 3:
                logging.info("Step 3: Generating tides...")
                step3.gen_tide(now, args.config)
                logging.info("✅ Step 3 completed")
            elif step_num == 4:
                logging.info("Step 4: Making wave forcing...")
                step4.make_waves(now)
                logging.info("✅ Step 4 completed")
            elif step_num == 5:
                logging.info("Step 5: Making wind forcing...")
                step5.make_winds(now)
                logging.info("✅ Step 5 completed")
            elif step_num == 6:
                logging.info("Step 6: Running SWAN wave model...")
                step6.par_run(now)
                logging.info("✅ Step 6 completed")
            elif step_num == 7:
                logging.info("Step 7: Post processing SWAN output...")
                step_7.postprocess_SWAN(now, 1)
                logging.info("✅ Step 7 completed")
            elif step_num == 8:
                logging.info("Step 8: Running inundation forecasts...")
                run_inundation_forecasts(now)
                logging.info("✅ Step 8 completed")
            elif step_num == 9:
                logging.info("Step 9: Archiving output...")
                step9.archive_output(now)
                logging.info("✅ Step 9 completed")
            elif step_num == 10:
                logging.info("Step 10: Downloading regional meteorological data...")
                step_10.download_NCEP(now)
                logging.info("✅ Step 10 completed")
            elif step_num == 11:
                logging.info("Step 11: Plotting winds and MSLP...")
                step_11.plot_winds_and_MSLP(now)
                logging.info("✅ Step 11 completed")
            elif step_num == 12:
                logging.info("Step 12: Hall's tailored forecast...")
                if email_enabled:
                    step_12.hallsTailoredForecast(now, args.config)
                else:
                    logging.info("Email disabled, running without email sending...")
                    # TODO: Add email-disabled version of step 12
                    step_12.hallsTailoredForecast(now, args.config)
                logging.info("✅ Step 12 completed")
            elif step_num == 13:
                if PLATFORM == "windows" and GUI_ENABLED:
                    logging.info("Step 13: Ingesting results to GUI...")
                    step_10_gui.ingest2GUI(now)
                    logging.info("✅ Step 13 completed")
                else:
                    logging.info("⚠️  Step 13 skipped (Windows GUI not available)")
            elif step_num == 14:
                if PLATFORM == "windows" and GUI_ENABLED:
                    logging.info("Step 14: GUI setup...")
                    step_13.ingest2GUI2(now)
                    logging.info("✅ Step 14 completed")
                else:
                    logging.info("⚠️  Step 14 skipped (Windows GUI not available)")
            else:
                logging.warning(f"Step {step_num} not implemented yet")
                continue
            
            # Mark step as completed
            mark_step_complete(now, step_num)
            success_count += 1
            
            step_duration = time.time() - step_start_time
            logging.info(f"⏱️  Step {step_num} completed in {step_duration:.1f} seconds")
            
        except Exception as e:
            step_duration = time.time() - step_start_time
            logging.error(f"❌ Step {step_num} failed after {step_duration:.1f} seconds: {e}")
            failed_steps.append(step_num)
            
            # If running a single step, exit immediately
            if args.step:
                logging.error("Single step execution failed, exiting")
                sys.exit(1)
            
            # For multi-step runs, log and continue
            logging.error(f"Continuing with remaining steps...")
    
    # Final summary
    total_duration = time.time() - start_time
    def log_execution_summary(total_duration, steps_to_run, success_count, failed_steps):
        logging.info("="*60)
        logging.info("EXECUTION SUMMARY")
        logging.info("="*60)
        logging.info(f"Total runtime: {total_duration:.1f} seconds")
        logging.info(f"Steps attempted: {len(steps_to_run)}")
        logging.info(f"Steps successful: {success_count}")
        logging.info(f"Steps failed: {len(failed_steps)}")
        if failed_steps:
            logging.error(f"Failed steps: {failed_steps}")
            logging.info("✅ Tuvalu Forecast completed with errors!")
        else:
            logging.info("🎉 Tuvalu Forecast completed successfully!")
            logging.info("="*60)

    log_execution_summary(total_duration, steps_to_run, success_count, failed_steps)
    if failed_steps:
        sys.exit(1)
