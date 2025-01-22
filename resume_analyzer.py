import os
import requests
from PyPDF2 import PdfReader
from docx import Document

class ResumeAnalyzer:
    def __init__(self, model="gemini-model-name"):
        # self.api_key = "AIzaSyCgQMrldhKd6mBKyoI206BRLKtHL5m0MDQ"
        self.api_key = "AIzaSyBm3tp-_rKmye6dj7FdhrsLYVAPHd8Pm2g"
        self.api_url = "https://gemini-api-url/analyze"
        self.model = model

    def extract_text(self, file_path):
        """
        Extract text from the uploaded file.
        Supports .txt, .pdf, and .docx formats.
        """
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == ".txt":
            with open(file_path, "r") as file:
                return file.read()
        elif file_extension == ".pdf":
            reader = PdfReader(file_path)
            return "".join(page.extract_text() for page in reader.pages)
        elif file_extension == ".docx":
            doc = Document(file_path)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        else:
            raise ValueError("Unsupported file format")

    def analyze(self, file_content):
        """
        Analyze the resume content using Gemini API.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": self.model,
                "input": file_content,
                "context": "Analyze this resume for an HR perspective.",
            }
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json().get("analysis", "No analysis provided.")
        except requests.exceptions.RequestException as e:
            return str(e)
        
if __name__ == "__main__":
    r = ResumeAnalyzer()
    t = r.extract_text("uploads/trail_resume.pdf")
    print(r.analyze(t))