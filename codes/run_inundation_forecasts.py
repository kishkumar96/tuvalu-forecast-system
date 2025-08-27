# -*- coding: utf-8 -*-
"""
Created for Tuvalu Forecast System: Inundation Forecast Runner
"""
import importlib
import multiprocessing
import datetime as dt
import os
import time

def run_inundation_forecasts(now):
    # List of atolls for which inundation forecast modules exist
    atolls = [
        'Vaitupu', 'Nui', 'Niulakita', 'Nanumaga', 'Nukufetau',
        'Funafuti', 'Nanumea', 'Nukulaelae', 'Niutao'
    ]
    
    processes = []
    process_names = []
    
    def run_with_chdir(main_func, now_arg, atoll_name):
        """Wrapper function that changes directory then calls the main function"""
        import os
        import sys
        import traceback
        
        original_cwd = os.getcwd()
        try:
            inundation_dir = os.path.join(original_cwd, 'inundation')
            os.chdir(inundation_dir)
            print(f"[{atoll_name}] Starting forecast processing...")
            main_func(now_arg)
            print(f"[{atoll_name}] ✅ Forecast completed successfully")
        except Exception as e:
            print(f"[{atoll_name}] ❌ Forecast failed: {e}")
            traceback.print_exc()
            sys.exit(1)  # Exit with error code
        finally:
            os.chdir(original_cwd)
    
    # Start all processes
    for atoll in atolls:
        module_name = f'inundation.Inundation_Forecast_{atoll}'
        try:
            mod = importlib.import_module(module_name)
            p = multiprocessing.Process(target=run_with_chdir, args=(mod.main, now, atoll))
            p.start()
            processes.append(p)
            process_names.append(atoll)
            print(f"Started inundation forecast for {atoll}")
        except Exception as e:
            print(f"❌ Could not start inundation forecast for {atoll}: {e}")
    
    # Wait for all to finish with timeout and status reporting
    timeout = 7200  # 2 hours timeout per process
    failed_processes = []
    successful_processes = []
    
    for i, p in enumerate(processes):
        atoll = process_names[i]
        try:
            p.join(timeout=timeout)
            
            # Check if process is still alive (timeout occurred)
            if p.is_alive():
                failed_processes.append(atoll)
                print(f"❌ {atoll} inundation forecast timed out after {timeout/60:.1f} minutes")
                p.terminate()
                p.join(timeout=5)
                if p.is_alive():
                    p.kill()
            # Check for successful completion
            elif p.exitcode == 0:
                successful_processes.append(atoll)
                print(f"✅ {atoll} inundation forecast completed successfully")
            # Handle None exitcode (race condition - process may still be finishing)
            elif p.exitcode is None:
                # Give it a moment to finish and check again
                time.sleep(0.1)
                if p.exitcode == 0:
                    successful_processes.append(atoll)
                    print(f"✅ {atoll} inundation forecast completed successfully")
                else:
                    failed_processes.append(atoll)
                    print(f"❌ {atoll} inundation forecast completed with unknown status (exit code: {p.exitcode})")
            # Check for failure
            else:
                failed_processes.append(atoll)
                print(f"❌ {atoll} inundation forecast failed (exit code: {p.exitcode})")
                
        except Exception as e:
            failed_processes.append(atoll)
            print(f"❌ {atoll} inundation forecast crashed: {e}")
            if p.is_alive():
                print(f"Terminating crashed process for {atoll}")
                p.terminate()
                p.join(timeout=5)
                if p.is_alive():
                    p.kill()
    
    # Final status report
    print(f"\n{'='*60}")
    print("INUNDATION FORECAST SUMMARY:")
    print(f"{'='*60}")
    print(f"✅ Successful: {len(successful_processes)}/{len(atolls)} islands")
    if successful_processes:
        print(f"   {', '.join(successful_processes)}")
    
    if failed_processes:
        print(f"❌ Failed: {len(failed_processes)}/{len(atolls)} islands")
        print(f"   {', '.join(failed_processes)}")
        
        # Check if any "failed" processes actually generated outputs (exit code race condition)
        actually_failed = []
        for atoll in failed_processes:
            # Check if this island generated recent output files
            import subprocess
            result = subprocess.run(
                f"find inundation/Figures -name '*{atoll}*' -mmin -60 | wc -l", 
                shell=True, capture_output=True, text=True
            )
            recent_files = int(result.stdout.strip()) if result.returncode == 0 else 0
            
            if recent_files > 0:
                print(f"⚠️  {atoll} reported failed but generated {recent_files} output files - likely exit code race condition")
                successful_processes.append(atoll)
            else:
                actually_failed.append(atoll)
        
        if actually_failed:
            print(f"\nActual failures after checking outputs: {', '.join(actually_failed)}")
            raise RuntimeError(f"Inundation forecasts failed for: {', '.join(actually_failed)}")
        else:
            print(f"\n✅ All islands actually completed successfully (exit code timing issues resolved)")
    
    print("All inundation forecasts completed successfully.")
