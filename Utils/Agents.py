from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
# NEW IMPORT: Import the dotenv function
from dotenv import load_dotenv

# --- Load the .env file at the start of the script ---
load_dotenv()
# -----------------------------------------------------

class Agent:
    def __init__(self, medical_report=None, role=None, extra_info=None):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info
        
        # Check that the key was loaded from the .env file
        if 'GOOGLE_API_KEY' not in os.environ:
            # Note: The error is more precise here since we tried to load it.
            raise ValueError(
                "The GOOGLE_API_KEY is not set. Please ensure you have a '.env' file "
                "in your project root with the format: GOOGLE_API_KEY=\"YOUR_KEY\""
            )

        # Initialize the prompt based on role and other info
        self.prompt_template = self.create_prompt_template()
        
        # MODEL INITIALIZATION: ChatGoogleGenerativeAI automatically uses 
        # the GOOGLE_API_KEY environment variable loaded by load_dotenv()
        self.model = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0
        )

    def create_prompt_template(self):
        # ... (Your existing create_prompt_template logic remains the same)
        if self.role == "MultidisciplinaryTeam":
            templates = f"""
                Act like a multidisciplinary team of healthcare professionals.
                You will receive a medical report of a patient visited by a Cardiologist, Psychologist, and Pulmonologist.
                Task: Review the patient's medical report from the Cardiologist, Psychologist, and Pulmonologist, analyze them and come up with a list of 3 possible health issues of the patient.
                Just return a list of bullet points of 3 possible health issues of the patient and for each issue provide the reason.
                
                Cardiologist Report: {self.extra_info.get('cardiologist_report', '')}
                Psychologist Report: {self.extra_info.get('psychologist_report', '')}
                Pulmonologist Report: {self.extra_info.get('pulmonologist_report', '')}
            """
        else:
            templates = {
                "Cardiologist": """
                    Act like a cardiologist. You will receive a medical report of a patient.
                    Task: Review the patient's cardiac workup, including ECG, blood tests, Holter monitor results, and echocardiogram.
                    Focus: Determine if there are any subtle signs of cardiac issues that could explain the patient’s symptoms. Rule out any underlying heart conditions, such as arrhythmias or structural abnormalities, that might be missed on routine testing.
                    Recommendation: Provide guidance on any further cardiac testing or monitoring needed to ensure there are no hidden heart-related concerns. Suggest potential management strategies if a cardiac issue is identified.
                    Please only return the possible causes of the patient's symptoms and the recommended next steps.
                    Medical Report: {medical_report}
                """,
                "Psychologist": """
                    Act like a psychologist. You will receive a patient's report.
                    Task: Review the patient's report and provide a psychological assessment.
                    Focus: Identify any potential mental health issues, such as anxiety, depression, or trauma, that may be affecting the patient's well-being.
                    Recommendation: Offer guidance on how to address these mental health concerns, including therapy, counseling, or other interventions.
                    Please only return the possible mental health issues and the recommended next steps.
                    Patient's Report: {medical_report}
                """,
                "Pulmonologist": """
                    Act like a pulmonologist. You will receive a patient's report.
                    Task: Review the patient's report and provide a pulmonary assessment.
                    Focus: Identify any potential respiratory issues, such as asthma, COPD, or lung infections, that may be affecting the patient's breathing.
                    Recommendation: Offer guidance on how to address these respiratory concerns, including pulmonary function tests, imaging studies, or other interventions.
                    Please only return the possible respiratory issues and the recommended next steps.
                    Patient's Report: {medical_report}
                """
            }
            templates = templates[self.role]
            
        return PromptTemplate.from_template(templates)
    
    def run(self):
        print(f"{self.role} is running with Gemini-2.5-flash...")
        
        if self.role == "MultidisciplinaryTeam":
            prompt = self.prompt_template.format(**self.extra_info)
        else:
            prompt = self.prompt_template.format(medical_report=self.medical_report)

        try:
            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error occurred during Gemini API call for {self.role}: {e}")
            return None

# Define specialized agent classes (remain the same)
class Cardiologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Cardiologist")

class Psychologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Psychologist")

class Pulmonologist(Agent):
    def __init__(self, medical_report):
        super().__init__(medical_report, "Pulmonologist")

class MultidisciplinaryTeam(Agent):
    def __init__(self, cardiologist_report, psychologist_report, pulmonologist_report):
        extra_info = {
            "cardiologist_report": cardiologist_report,
            "psychologist_report": psychologist_report,
            "pulmonologist_report": pulmonologist_report
        }
        super().__init__(medical_report=None, role="MultidisciplinaryTeam", extra_info=extra_info)