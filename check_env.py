"""
Helper script to check if .env file is configured correctly.
Run this script to verify your .env setup before starting the Flask server.
"""
import os
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).parent.absolute()
ENV_PATH = BASE_DIR / '.env'

print("="*60)
print("MediAgent - Environment Configuration Checker")
print("="*60)
print(f"\nChecking for .env file in: {BASE_DIR}")
print(f"Full path: {ENV_PATH}\n")

# Check if .env file exists
if ENV_PATH.exists():
    print("✓ .env file found!")
    print(f"  Location: {ENV_PATH}\n")
    
    # Try to read and parse it
    try:
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=str(ENV_PATH), override=True)
        
        # Check for GOOGLE_API_KEY
        api_key = os.environ.get('GOOGLE_API_KEY')
        
        if api_key:
            # Mask the key for security
            masked_key = api_key[:10] + "..." + api_key[-4:] if len(api_key) > 14 else "***"
            print(f"✓ GOOGLE_API_KEY is set!")
            print(f"  Value: {masked_key}")
            print(f"  Length: {len(api_key)} characters\n")
            
            # Check if it looks like a valid Google API key
            if api_key.startswith('AIza'):
                print("✓ API key format looks correct (starts with 'AIza')\n")
            else:
                print("⚠ Warning: API key doesn't start with 'AIza'")
                print("  Make sure you're using a Google API key\n")
        else:
            print("✗ GOOGLE_API_KEY not found in .env file")
            print("\nPlease add the following line to your .env file:")
            print('  GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY_HERE"\n')
            
    except Exception as e:
        print(f"✗ Error reading .env file: {e}\n")
        
else:
    print("✗ .env file NOT found!\n")
    print("To fix this:")
    print("1. Create a file named '.env' (no extension) in this directory")
    print(f"2. Location: {ENV_PATH}")
    print("3. Add the following content:")
    print('   GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY_HERE"')
    print("\nExample .env file content:")
    print('   GOOGLE_API_KEY="AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"')
    print("\nGet your API key from: https://makersuite.google.com/app/apikey\n")

print("="*60)

