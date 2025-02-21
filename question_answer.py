# importing needed modules
# importing the needed modules
import google.generativeai as genai

class QnA:

    def __init__(self, job_title, job_description):
        # storing our api key
        self.api_key = "AIzaSyBm3tp-_rKmye6dj7FdhrsLYVAPHd8Pm2g"
        # creating the gemini object
        genai.configure(api_key=self.api_key)
        # choosing the model of gemini
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.job_title = job_title
        self.job_description = job_description
        self.data = {}

    # creating the chat
    def generate_question(self, questions_asked):
        response = self.model.start_chat(
            history=[
                {"role": "user", "parts": f"Hello, I am the HR manager. I would like you to help me conduct an interview for a {self.job_title} position. And this is the job decription {self.job_description}.Please ask the candidate relevant questions that assess their skills, experience, and cultural fit for the role. Focus on their technical abilities, teamwork, problem-solving skills, and how they handle challenges. Start by asking the candidate to introduce themselves and their relevant experience."}
            ]
        )
        response = response.send_message(f"Ask me question very small but they should be very technical and job specific and tailored questions, which are not asked already, here's the list {questions_asked}. Just give me question and nothing else, send it to me in json format 'question'.").text.replace('```','').split(":")[-1].replace('"', '').replace("\n", "")[1:-2]
        # print(response)
        return {"question": response}
    
    def generate_video_question(self, questions_asked):
        response = self.model.start_chat(
        history=[
                {"role": "user", "parts": f"Hello, I am the HR manager. I would like you to help me conduct a video interview for a {self.job_title} position. Here is the job description: {self.job_description}. Please ask the candidate relevant technical and job-specific questions related to video format. Focus on their ability to explain complex concepts clearly, demonstrate problem-solving approaches, and how they adapt to dynamic work situations. Start with a question that checks their understanding of the role and its responsibilities."}
            ]
        )
        response = response.send_message(f"Ask me concise and specific questions related to {self.job_title} job, which assess their expertise and suitability for the role, avoiding questions already asked. Here's the list of questions asked: {questions_asked}. Just send me the question in JSON format 'question'.").text.replace('```','').split(":")[-1].replace('"', '').replace("\n", "")[1:-2]
        return {"question": response}

    def analyse_response(self, data):
        response = self.model.start_chat(
            history=[
                {"role": "user", "parts": "You are a very expert HR who an evaluate the candidates based on their answes to the questions."}
            ]
        )
        response = response.send_message(f"Please analyze the questions answers and give me the wheter we should hire or no in a single word. {self.data} . I don't want a huge answer only a single word response either yes or no")
        print(response)
        return response.text

if __name__ == "__main__":
    print("hello world!")
    # number_of_questions = 5
    # name = input("Enter your Name: ")
    # job_tile = input("Enter Job Title: ")
    # questions_asked = []
    # for n in range(number_of_questions):
    #     question_data = generate_question(job_tile, questions_asked)
    #     questions_asked.append(question_data["question"])
    #     data[n+1] = question_data
    #     print("\n")
    #     print(f"Question: {question_data['question']}")
    #     print("\n")
    #     response = input("Write your answer: ")
    #     data[n+1]['response'] = response
    # analyse_response(data)

