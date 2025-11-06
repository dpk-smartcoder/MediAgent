from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import json
import os
import sys

# Ensure the 'Utils' directory is in the path to import Agents
# This is required because Flask runs from a different context than the original Main.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'Utils'))

# Imports the Agent classes from Utils/Agents.py (must be present)
try:
    from Agents import Cardiologist, Psychologist, Pulmonologist, MultidisciplinaryTeam
except ImportError:
    print("FATAL ERROR: Could not import Agent classes. Ensure 'Utils/Agents.py' exists.")
    sys.exit(1)


# --- Initialization ---
# Load API key from apikey.env before Flask starts
load_dotenv(dotenv_path='apikey.env')

app = Flask(__name__)
# ----------------------


# Core logic function, extracted from your original Main.py
def run_analysis(medical_report: str) -> str:
    """
    Runs the multi-agent analysis on a given medical report string.
    """
    if not medical_report or len(medical_report.strip()) < 50:
        return "Error: Medical report is too short or empty. Analysis aborted."
    
    agents = {
        "Cardiologist": Cardiologist(medical_report),
        "Psychologist": Psychologist(medical_report),
        "Pulmonologist": Pulmonologist(medical_report)
    }

    # Function to run each agent and get their response
    def get_response(agent_name, agent):
        response = agent.run()
        return agent_name, response

    # Run the agents concurrently and collect responses
    responses = {}
    print("--- Running Specialized Agents Concurrently ---")
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(get_response, name, agent): name for name, agent in agents.items()}
        
        for future in as_completed(futures):
            agent_name, response = future.result()
            responses[agent_name] = response
            print(f"✅ {agent_name} finished analysis.")
            
    # Run the MultidisciplinaryTeam agent to generate the final diagnosis
    team_agent = MultidisciplinaryTeam(
        cardiologist_report=responses.get("Cardiologist", "No Cardiologist Report"),
        psychologist_report=responses.get("Psychologist", "No Psychologist Report"),
        pulmonologist_report=responses.get("Pulmonologist", "No Pulmonologist Report")
    )
    
    print("--- Running Multidisciplinary Team Synthesis ---")
    final_diagnosis = team_agent.run()
    
    return final_diagnosis


# --- API Endpoints ---

@app.route('/', methods=['GET'])
def home():
    """Simple check to ensure the API is running."""
    return jsonify({
        "status": "API is running",
        "message": "Use POST /process_string (JSON body) or POST /process_file (File Upload) for analysis."
    })

@app.route('/process_string', methods=['POST'])
def process_string():
    """
    Analyzes a medical report provided directly as a string in the JSON body.
    Expected JSON: {"report_content": "Patient reports severe chest pain..."}
    """
    data = request.get_json()
    if not data or 'report_content' not in data:
        return jsonify({"error": "Missing 'report_content' in request body."}), 400
    
    report_content = data['report_content']
    
    try:
        final_diagnosis = run_analysis(report_content)
        
        return jsonify({
            "status": "success",
            "diagnosis": final_diagnosis
        })
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return jsonify({"error": "Internal server error during agent execution.", "details": str(e)}), 500

@app.route('/process_file', methods=['POST'])
def process_file():
    """
    Analyzes the text content of a medical report file uploaded via form data.
    The frontend should send the file under the key 'file'.
    """
    # 1. Check if the file part is present in the request
    if 'file' not in request.files:
        return jsonify({"error": "Missing file upload. Please submit a file under the form data key 'file'."}), 400
    
    file = request.files['file']
    
    # 2. Check if a file was actually selected
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400
        
    # Optional: Check file extension (e.g., must be a .txt file)
    if not file.filename.lower().endswith('.txt'):
        return jsonify({"error": "Invalid file type. Only .txt files are accepted for analysis."}), 415

    if file:
        try:
            # 3. Read the file content and decode it into a standard string (UTF-8)
            report_content = file.read().decode('utf-8')
            
            # 4. Run the analysis with the extracted text
            final_diagnosis = run_analysis(report_content)
            
            return jsonify({
                "status": "success",
                "diagnosis": final_diagnosis,
                "filename_processed": file.filename
            })
        except Exception as e:
            print(f"An error occurred during file processing or analysis: {e}")
            return jsonify({"error": "Internal server error during processing.", "details": str(e)}), 500


if __name__ == '__main__':
    # To run: flask run
    # For local testing, you might use: app.run(debug=True, host='0.0.0.0')
    print("To run this application, use 'flask run' in your terminal.")
    # The runner environment will start the Flask app automatically.