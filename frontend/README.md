# MediAgent Frontend

React-based frontend for the MediAgent Multi-Agent Medical Diagnosis System.

## Features

- **File Upload**: Upload medical reports in .txt format
- **Real-time Processing**: Submit files to backend API for analysis
- **Markdown Rendering**: Beautiful display of diagnosis results in markdown format
- **Responsive Design**: Modern UI built with Tailwind CSS
- **Navigation**: Seamless routing between home and results pages

## Installation

1. Install dependencies:
```bash
npm install
```

2. Configure API URL (optional):
   - Create a `.env` file in the root directory
   - Add: `REACT_APP_API_URL=http://localhost:5000`
   - Default is `http://localhost:5000`

## Running the Application

Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

## Build for Production

```bash
npm run build
```

## Project Structure

```
src/
  ├── pages/
  │   ├── Home.js          # Main upload page
  │   └── Results.js       # Results display page
  ├── services/
  │   └── api.js           # API service functions
  ├── App.js               # Main app component with routing
  ├── index.js             # Entry point
  └── index.css            # Global styles with Tailwind
```

## Backend Integration

The frontend communicates with the Flask backend API:
- **Endpoint**: `/process_file` (POST)
- **Format**: FormData with file under key 'file'
- **Response**: JSON with `status`, `diagnosis`, and `filename_processed`

## Technologies Used

- React 18
- React Router DOM
- React Markdown
- Tailwind CSS
- Fetch API

