import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

class Config:
    # Fetch the API Key from environment variables (Security Best Practice)
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Folder where the Fees Dept's PPTs, PDFs, and Photos will be stored
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    # Allowed file types as per Problem Statement ID25104
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'jpg', 'jpeg', 'png'}

    # Local SQLite database file (Zero-cost storage)
    DATABASE = os.path.join(os.getcwd(), 'database.db')

    # Ensure the upload directory exists
    @staticmethod
    def init_app():
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)