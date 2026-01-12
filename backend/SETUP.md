# Backend Setup Guide

## Environment Configuration

The backend requires a Google API key to use the Gemini AI model. You need to create a `.env` file in this directory.

### Steps to Create .env File

1. **Get a Google API Key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Create a new API key
   - Copy the API key

2. **Create the .env file:**
   - In the directory: `MediAgent/Backend/model_and_api_multiagentic_diagnosis/`
   - Create a new file named `.env` (no extension)
   - Add the following content:

```env
GOOGLE_API_KEY="YOUR_ACTUAL_API_KEY_HERE"
```

**Important:** Replace `YOUR_ACTUAL_API_KEY_HERE` with your actual Google API key.

### Example .env file:

```env
GOOGLE_API_KEY="AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

### File Location

The `.env` file should be located at:
```
MediAgent/Backend/model_and_api_multiagentic_diagnosis/.env
```

### Verification

After creating the `.env` file, restart your Flask server. The server will check for the API key on startup and display a warning if it's not found.

### Troubleshooting

If you still get the error "GOOGLE_API_KEY is not set":
1. Make sure the `.env` file is in the correct directory (same folder as `app.py`)
2. Make sure there are no extra spaces around the `=` sign
3. Make sure the API key is wrapped in quotes: `GOOGLE_API_KEY="your_key"`
4. Restart the Flask server after creating/modifying the `.env` file

