import os
import requests
from PyPDF2 import PdfReader
from docx import Document
import google.generativeai as genai
import json

class ResumeAnalyzer:
    def __init__(self):
        # self.api_key = "AIzaSyCgQMrldhKd6mBKyoI206BRLKtHL5m0MDQ"
        self.api_key = "AIzaSyBm3tp-_rKmye6dj7FdhrsLYVAPHd8Pm2g"
        genai.configure(api_key=self.api_key)
        # choosing the model of gemini
        self.model = genai.GenerativeModel("gemini-1.5-flash")

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
            # headers = {
            #     "Authorization": f"Bearer {self.api_key}",
            #     "Content-Type": "application/json",
            # }
            # payload = {
            #     "model": self.model,
            #     "input": file_content,
            #     "context": "Analyze this resume for an HR perspective.",
            # }
            # response = requests.post(self.api_url, json=payload, headers=headers)
            # response.raise_for_status()
            # return response.json().get("analysis", "No analysis provided.")
            response = self.model.start_chat(
                history=[
                        {"role": "user", "parts": "You are the HR Head of the company. You have been analysing the resumes since last 10 years and have created a well defined sense of analyzing the resumes."}
                    ]
                )
            response = response.send_message(f"Please analyze this resume with the content: {file_content}. I am a HR please recommend me how best this candidate, please rate him on scale of 10. please return response in json format with keys = [rating, strenghts, weakness, recommendation]")
            # print(response)
            return json.loads(response.text.replace("*","").replace("```","")[5:])
        except requests.exceptions.RequestException as e:
            return str(e)
        
if __name__ == "__main__":
    r = ResumeAnalyzer()
    t = r.extract_text("uploads/trail_resume.pdf")
    d = r.analyze(t)
    print([i for i in d])
    print(d)