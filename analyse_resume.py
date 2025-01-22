import os
import spacy
from PyPDF2 import PdfReader
from docx import Document
from collections import Counter
import re


class ResumeAnalyzer:
    def __init__(self):
        # Load SpaCy NLP model
        self.nlp = spacy.load("en_core_web_sm")

    def extract_text(self, file_path):
        """
        Extract text from a resume file (.txt, .pdf, or .docx).
        """
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_extension == ".pdf":
            reader = PdfReader(file_path)
            return "".join(page.extract_text() for page in reader.pages)
        elif file_extension == ".docx":
            doc = Document(file_path)
            return "\n".join(paragraph.text for paragraph in doc.paragraphs)
        else:
            raise ValueError("Unsupported file format. Use .txt, .pdf, or .docx.")

    def extract_contact_info(self, text):
        """
        Extract contact details (email and phone number) from the text.
        """
        email = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
        phone = re.search(r"\+?\d[\d\s\-]{7,15}", text)
        linkedin = re.search(r"(https?://[^\s]+linkedin\.com[^\s]+)", text)
        return {
            "email": email.group(0) if email else "Not found",
            "phone": phone.group(0) if phone else "Not found",
            "linkedin": linkedin.group(0) if linkedin else "Not found"
        }

    def extract_skills(self, text):
        """
        Extract skills from the resume using keyword matching.
        """
        skills = [
            "python", "java", "c++", "sql", "machine learning", "data analysis",
            "project management", "communication", "leadership", "excel", "tableau",
            "css", "html", "javascript", "aws", "docker", "kubernetes", "react",
            "angular", "flask", "django", "node.js"
        ]
        found_skills = [skill for skill in skills if skill.lower() in text.lower()]
        return list(set(found_skills))

    def extract_education(self, text):
        """
        Extract education details from the text.
        """
        education_keywords = [
            "bachelor", "master", "phd", "mba", "bsc", "msc", "engineering",
            "university", "college", "degree", "certification"
        ]
        education = []
        for sentence in text.split("\n"):
            if any(keyword in sentence.lower() for keyword in education_keywords):
                education.append(sentence.strip())
        return education

    def extract_experience(self, text):
        """
        Extract experience details, including job roles and companies.
        """
        roles = ["software engineer", "developer", "analyst", "manager", "consultant", "intern"]
        companies = []
        experience = []
        for sentence in text.split("\n"):
            if re.search(r"\d{4}.*\d{4}|present", sentence.lower()):
                experience.append(sentence.strip())
                # Extract company names
                company_match = re.search(r"at\s+([\w\s&]+)", sentence, re.IGNORECASE)
                if company_match:
                    companies.append(company_match.group(1).strip())

        return {"roles": roles, "companies": list(set(companies)), "experience_details": experience}

    def extract_certifications(self, text):
        """
        Extract certifications mentioned in the resume.
        """
        certification_keywords = ["certified", "certification", "course", "diploma", "training"]
        certifications = []
        for sentence in text.split("\n"):
            if any(keyword in sentence.lower() for keyword in certification_keywords):
                certifications.append(sentence.strip())
        return certifications

    def extract_languages(self, text):
        """
        Extract languages mentioned in the resume.
        """
        languages = ["english", "hindi", "spanish", "french", "german", "mandarin", "japanese"]
        found_languages = [lang.capitalize() for lang in languages if lang.lower() in text.lower()]
        return list(set(found_languages))

    def extract_achievements(self, text):
        """
        Extract achievements based on patterns like awards, recognitions, etc.
        """
        achievements_keywords = ["award", "recognition", "achievement", "honor", "accomplishment"]
        achievements = []
        for sentence in text.split("\n"):
            if any(keyword in sentence.lower() for keyword in achievements_keywords):
                achievements.append(sentence.strip())
        return achievements

    def extract_soft_skills(self, text):
        """
        Extract soft skills from the text.
        """
        soft_skills = [
            "teamwork", "communication", "leadership", "problem solving",
            "time management", "adaptability", "collaboration"
        ]
        found_skills = [skill for skill in soft_skills if skill.lower() in text.lower()]
        return list(set(found_skills))

    def analyze_resume(self, file_path):
        """
        Analyze the resume and return detailed insights.
        """
        try:
            text = self.extract_text(file_path)
            doc = self.nlp(text)

            # Extract information
            contact_info = self.extract_contact_info(text)
            skills = self.extract_skills(text)
            education = self.extract_education(text)
            experience = self.extract_experience(text)
            certifications = self.extract_certifications(text)
            languages = self.extract_languages(text)
            achievements = self.extract_achievements(text)
            soft_skills = self.extract_soft_skills(text)

            # Word frequency (for visualization)
            word_freq = Counter([token.text.lower() for token in doc if token.is_alpha])

            return {
                "contact_info": contact_info,
                "skills": skills,
                "education": education,
                "experience": experience,
                "certifications": certifications,
                "languages": languages,
                "achievements": achievements,
                "soft_skills": soft_skills,
                "word_frequency": word_freq.most_common(10)
            }
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    # Example usage
    analyzer = ResumeAnalyzer()
    file_path = "uploads/trail_resume.pdf"  # Replace with your file path
    analysis = analyzer.analyze_resume(file_path)

    # Print the structured analysis
    print("\nResume Analysis:")
    for key, value in analysis.items():
        print(f"{key.capitalize()}: {value}")