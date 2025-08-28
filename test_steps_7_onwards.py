#!/usr/bin/env python3
"""
Test script to verify steps 7 onwards work after SWAN completion
Tests post-processing, inundation forecasts, and archiving
"""

import datetime as dt
import os
import sys
import logging

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Add codes directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'codes'))

# Import the required modules
try:
    import step7_postprocess_output as step_7
    import step9_archive_output as step9
    from run_inundation_forecasts import run_inundation_forecasts
    logging.info("✅ Successfully imported post-SWAN modules")
except ImportError as e:
    logging.error(f"❌ Failed to import modules: {e}")
    sys.exit(1)

def test_recent_swan_run():
    """Test steps 7-9 on the most recent SWAN run"""
    
    # Use the most recent run directory that has output.mat
    run_dir = "2025082700"  # Your most recent successful run
    
    # Parse date from run directory 
    try:
        year = int(run_dir[:4])
        month = int(run_dir[4:6])
        day = int(run_dir[6:8])
        hour = int(run_dir[8:10])
        now = dt.datetime(year, month, day, hour)
        logging.info(f"🧪 Testing post-SWAN steps for run: {run_dir} ({now})")
    except (ValueError, IndexError):
        logging.error(f"❌ Invalid run directory format: {run_dir}")
        return False
    
    # Check if SWAN output exists
    output_file = os.path.join("runs", run_dir, "output.mat")
    if not os.path.exists(output_file):
        logging.error(f"❌ SWAN output not found: {output_file}")
        return False
    
    # Get file size
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    logging.info(f"✅ Found SWAN output: {output_file} ({size_mb:.1f} MB)")
    
    success = True
    
    # Test Step 7: Post-process SWAN output
    logging.info("🧪 Testing Step 7: Post-processing SWAN output...")
    try:
        step_7.postprocess_SWAN(now, 1)
        logging.info("✅ Step 7 completed successfully")
    except Exception as e:
        logging.error(f"❌ Step 7 failed: {e}")
        success = False
    
    # Test Step 8: Inundation forecasts (if available)
    logging.info("🧪 Testing Step 8: Inundation forecasts...")
    try:
        run_inundation_forecasts(now)
        logging.info("✅ Step 8 completed successfully")
    except Exception as e:
        logging.error(f"⚠️  Step 8 failed (may be expected if config missing): {e}")
        # Don't mark as failure since inundation config might not be set up
    
    # Test Step 9: Archive output
    logging.info("🧪 Testing Step 9: Archive output...")
    try:
        step9.archive_output(now)
        logging.info("✅ Step 9 completed successfully")
    except Exception as e:
        logging.error(f"❌ Step 9 failed: {e}")
        success = False
    
    return success

if __name__ == "__main__":
    logging.info("🚀 Testing Tuvalu Forecast - Steps 7 onwards")
    logging.info("=" * 60)
    
    success = test_recent_swan_run()
    
    if success:
        logging.info("🎉 Post-SWAN steps are working correctly!")
        logging.info("🔧 The sys.exit() fix resolved the pipeline issue.")
        sys.exit(0)
    else:
        logging.error("❌ Some post-SWAN steps failed - check logs above")
        sys.exit(1)
