# importing needed modules
# importing the needed modules
import google.generativeai as genai

class QnA:

    def __init__(self, job_title, job_description):
        # storing our api key
        self.api_key = "AIzaSyCgQMrldhKd6mBKyoI206BRLKtHL5m0MDQ"
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

    def analyse_response(self, data):
        response = self.model.start_chat(
            history=[
                {"role": "user", "parts": "You are a psychologist who generates the analysis of the user's brain dominance based on the answers they give over the questions asked,"}
            ]
        )
        response = response.send_message(f"Tell me which part of the user is dominat: Right or Left. Based on the Questions Answered: {self.data}")
        print(response)

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

