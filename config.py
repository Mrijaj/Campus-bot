import os
from dotenv import load_dotenv

# Load variables from the .env file in the root directory
load_dotenv()


class Config:
    """
    Configuration settings for the Campus Assistant Bot.
    Separates environment secrets from application logic.
    """

    # 1. API Keys & Security
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev_fallback_key_sih_2025")

    # 2. File Handling
    # Folder where the Fees Dept's PPTs, PDFs, and Photos will be stored
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')

    # Allowed file types as per Problem Statement ID25104
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'jpg', 'jpeg', 'png'}

    # 3. Database
    # Local SQLite database file (Zero-cost storage)
    DATABASE = os.path.join(os.getcwd(), 'database.db')

    # 4. Folder Initialization
    # Ensure the upload directory exists immediately upon app start
    @staticmethod
    def init_app():
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)