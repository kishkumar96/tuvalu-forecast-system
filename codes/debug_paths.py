#!/usr/bin/env python3
import os
import sys

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load .env like the main script does  
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
    print("✅ Loaded .env file")
except Exception as e:
    print(f"❌ Could not load .env: {e}")

# Test ROOT_DIR calculation
if os.path.exists('/app') and os.path.exists('/app/codes'):
    ROOT_DIR = os.environ.get('TV_ROOT', '/app')
    print("🐳 Using Docker paths")
else:
    # Native environment - use script location
    default_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ROOT_DIR = os.environ.get("TV_ROOT") or default_root
    # Ensure ROOT_DIR is never empty
    if not ROOT_DIR or ROOT_DIR.strip() == "":
        ROOT_DIR = default_root
    print("🐍 Using native paths")

print(f"TV_ROOT env: {os.environ.get('TV_ROOT')}")
print(f"ROOT_DIR computed: {ROOT_DIR}")

# Test SWAN executable path
swan_exe = os.path.join(ROOT_DIR, 'executables', 'swan.exe')
print(f"SWAN path: {swan_exe}")
print(f"EXISTS: {os.path.exists(swan_exe)}")

# Test other common paths
test_paths = [
    os.path.join(os.getcwd(), '..', 'executables', 'swan.exe'),
    os.path.join(os.path.dirname(__file__), '..', 'executables', 'swan.exe'),
    './executables/swan.exe',
    '../executables/swan.exe'
]

print("\n🔍 Testing various paths:")
for path in test_paths:
    resolved = os.path.abspath(path)
    exists = os.path.exists(resolved)
    print(f"  {path} -> {resolved} ({'✅' if exists else '❌'})")
