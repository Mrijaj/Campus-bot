import os
import fitz  # PyMuPDF
import base64
import httpx
from docx import Document
from pptx import Presentation
from groq import Groq
from config import Config


class FileProcessor:
    def __init__(self):
        # SSL Bypass for HPE/Corporate Network
        custom_client = httpx.Client(verify=False)

        self.client = Groq(
            api_key=Config.GROQ_API_KEY,
            http_client=custom_client
        )

    def process(self, file_path):
        try:
            ext = file_path.rsplit('.', 1)[1].lower()

            if ext == 'pdf':
                return self._extract_pdf(file_path)
            elif ext == 'docx':
                return self._extract_docx(file_path)
            elif ext == 'pptx':
                return self._extract_pptx(file_path)
            elif ext in ['jpg', 'jpeg', 'png']:
                return self._extract_image_vision(file_path)
            return ""
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            return ""

    def _extract_pdf(self, path):
        text = ""
        with fitz.open(path) as doc:
            for page in doc:
                text += page.get_text()
        return text

    def _extract_docx(self, path):
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _extract_pptx(self, path):
        prs = Presentation(path)
        text = []
        for slide in prs.slides:
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    text.append(shape.text)
        return "\n".join(text)

    def _extract_image_vision(self, path):
        with open(path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        completion = self.client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract all text from this image accurately."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }]
        )
        return completion.choices[0].message.content