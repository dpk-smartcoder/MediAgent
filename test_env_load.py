"""Quick test to verify .env loading works"""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, '.env')

print(f"Testing .env loading from: {ENV_PATH}")

if os.path.exists(ENV_PATH):
    # Handle BOM (Byte Order Mark) that Windows sometimes adds to UTF-8 files
    try:
        with open(ENV_PATH, 'r', encoding='utf-8-sig') as f:
            # Read and parse manually to handle BOM
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")  # Remove quotes
                    os.environ[key] = value
        print("✓ Loaded .env file (handled BOM)")
    except Exception as e:
        print(f"✗ Error loading .env: {e}")
else:
    print(f"✗ .env file not found at: {ENV_PATH}")

# Check result
if 'GOOGLE_API_KEY' in os.environ:
    api_key = os.environ.get('GOOGLE_API_KEY', '')
    masked = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
    print(f"✓ GOOGLE_API_KEY loaded successfully!")
    print(f"  Value: {masked}")
    print(f"  Length: {len(api_key)} characters")
else:
    print("✗ GOOGLE_API_KEY not found in environment")

