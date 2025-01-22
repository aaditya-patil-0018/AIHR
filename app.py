# importing needed modules
from flask import Flask
from flask import render_template, request, session, redirect, url_for, jsonify, Response
from werkzeug.utils import secure_filename
# all user defined modules
from user_management import Users
from hr_management import HR
from question_answer import QnA
from company_management import Company
from openings_management import Openings
from resume_analyzer import ResumeAnalyzer
# for files and databases
import json
import os
# for machine learning
import cv2
import numpy as np
import base64
import logging
from deepface import DeepFace

# flask object
app = Flask(__name__)
app.secret_key = "shss!thisisasecretkey."

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'  # You can change this to any path you want
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

# Other configurations
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # Set max upload size to 16MB

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

analyzer = ResumeAnalyzer()

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to read and write JSON data
def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {}

def write_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

# Ensure the openings_data.json file exists
OPENINGS_FILE = "openings_data.json"
def create_openings_file():
    # check if file is present or not
    # if not present then create it
    if not os.path.exists(OPENINGS_FILE):
        with open(OPENINGS_FILE, 'w') as f:
            json.dump([], f)
    return load_openings()

# Load the job openings data
def load_openings():
    # load the openings database file
    with open(OPENINGS_FILE, 'r') as f:
        return json.load(f)

# Save the job openings data
def save_openings(data):
    with open(OPENINGS_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Emotion mappings
emotion_mappings = {
    "happy": "Confidence",
    "sad": "Anxious",
    "angry": "Irritated",
    "fear": "Anxious",
    "surprise": "Excitement",
    "neutral": "Calm",
    "disgust": "Displeased"
}

# landing page
@app.route("/")
def landing():
    return render_template('landing.html')

@app.route('/privacy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route('/terms')
def terms_of_service():
    return render_template('terms_of_service.html')

################
# HR SIDE CODE #
################

@app.route('/add/company', methods=["GET", "POST"])
def add_company():
    if request.method == "GET":
        return render_template("company_registration.html")
    else:
        name = request.form.get('name')
        ty = request.form.get('type')
        website = request.form.get('website')
        description = request.form.get('description')
        size = request.form.get('size')
        city = request.form.get('city')
        state = request.form.get('state')
        company = Company()
        company.add(name, ty, website, description, size, city, state)
        return redirect(url_for('landing'))

# hr signup page
@app.route("/hr/signup", methods=["GET", "POST"])
def signup():
    if "hr" not in session:
        session["hr"] = False
        session["company"] = ""
    if session["hr"] == False:
        usertype = "hr"
        if request.method == "GET":
            session["company"] = ""
            return render_template("signup.html", usertype=usertype)
        elif request.method == "POST":
            user = Users()
            email = request.form.get("email")
            password = request.form.get("password")
            if user.signup(email, password, usertype):
                session[usertype] = True
                return redirect(url_for("hr_dashboard"))
            else:
                session[usertype] = False
                return "Retry Again!"
    else:
        return redirect(url_for('hr_dashboard'))

# hr login page
@app.route("/hr/login", methods=["GET", "POST"])
def hr_login():
    if "hr" not in session:
       session["hr"] = False 
       session["company"] = ""
    if session["hr"] == False:
        usertype = "hr"
        session["company"] = ""
        if request.method == "GET":
            return render_template("login.html", usertype=usertype)
        elif request.method == "POST":
            user = Users()
            email = request.form.get("email")
            password = request.form.get("password")
            if user.login(email, password, usertype):
                session[usertype] = True
                if usertype == "hr":
                    hr = HR()
                    company = hr.get(email=email)[3]
                    session["company"] = company
                return redirect(url_for("hr_dashboard"))
            else:
                session[usertype] = False
                return "Retry Again!"
    else:
        return redirect(url_for("hr_dashboard"))
    
@app.route("/hr/logout")
def hr_logout():
    session["hr"] = False
    return redirect(url_for("landing"))

@app.route("/hr/dashboard", methods=["GET", "POST"])
def hr_dashboard():
    if session["company"] != "":
        if request.method == "GET":
            opening_data = Openings()  # Ensure the openings data file exists
            company = session['company']
            data = opening_data.get_all_opening(company=company)
            return render_template('hr_dashboard.html', data=data, company=company)
        elif request.method == "POST":
            title = request.form.get('type')
            description = f"{request.form.get('description')} Requirements: {request.form.get('requirements')}" 
            user_role = request.form.get('title')
            data = {
                "type": title,
                "description": description,
                "user_role": user_role,
                "status": "Open",
                "users_enrolled": 0
            }
            opening_data = Openings()
            company = session['company']
            opening_data.create_opening(company=company, d=data)
            return redirect(url_for('hr_dashboard'))
            # return "post method evoked!"
    else:
        return redirect(url_for('hr_registration'))

@app.route("/hr/registration", methods=["GET", "POST"])
def hr_registration():
    if session["hr"] == True:
        if request.method == "GET":
            company = Company()
            data = company.load_data()
            return render_template("hr_registration.html", data=data)
        elif request.method == "POST":
            data = {
                "email": request.form.get('email'),
                "name": request.form.get('name'),
                "company": request.form.get('company'),
                "role": request.form.get('role'),
                "phone": request.form.get('phone'),
                "city": request.form.get('city'),
                "state": request.form.get('state')
            }
            hr = HR()
            hr.register(data)
            session["company"] = request.form.get('company')
            return redirect(url_for('hr_dashboard'))
    else:
        return render_template("not_allowed.html")

# Route to get all job openings
# @app.route('/hr/get-openings')
# def get_openings():
#     openings = load_openings()
#     return jsonify(json.dumps(openings["TechCorp"]))

# Route to add a new job opening
# @app.route('/hr/add-job', methods=['POST'])
# def add_job():
#     if request.method == 'POST':
#         title = request.form['title']
#         description = request.form['description']
#         requirements = request.form['requirements']

#         # Get existing job openings
#         openings = load_openings()

#         # Create new job opening
#         new_job = {
#             'title': title,
#             'description': description,
#             'requirements': requirements,
#             'applicants': 0  # Default applicants to 0
#         }

#         # Add to the openings list and save it
#         openings["TechCorp"].append(new_job)
#         save_openings(openings)

#         return redirect('/hr/dashboard')

# Route to delete a job opening (to be linked to the delete button on the frontend)
@app.route('/hr/delete-job/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    openings = load_openings()
    if 0 <= job_id < len(openings):
        openings.pop(job_id)
        save_openings(openings)
    return redirect('/hr')

#######################
# APPLICANT SIDE CODE #
#######################

# applicant signup page
@app.route("/applicant/signup", methods=["GET", "POST"])
def applicant_signup():
    if "applicant" not in session:
        session["applicant"] = False 
        session["user-email"] = ""
    if session["applicant"] == False:
        usertype = "applicant"
        if request.method == "GET":
            return render_template("signup.html", usertype=usertype)
        elif request.method == "POST":
            user = Users()
            email = request.form.get("email")
            password = request.form.get("password")
            if user.signup(email, password, usertype):
                session[usertype] = True
                session["user-email"] = email
                return redirect("/applicant/slide")
            else:
                session[usertype] = False
                session["user-email"] = ""
                return "Retry Again!"
    else:
        return redirect("/applicant/slide")

# applicant login page
@app.route("/applicant/login", methods=["GET", "POST"])
def applicant_login():
    if "applicant" not in session:
        session["applicant"] = False
        session["user-email"] = ""
    if session["applicant"] == False:
        usertype = "applicant"
        if request.method == "GET":
            return render_template("login.html", usertype=usertype)
        elif request.method == "POST":
            user = Users()
            email = request.form.get("email")
            password = request.form.get("password")
            if user.login(email, password, usertype):
                session[usertype] = True
                session["user-email"] = email
                return redirect("/applicant/dashboard")
            else:
                session[usertype] = False
                session["user-email"] = ""
                return "Retry Again!"
    else:
        return redirect("/applicant/dashboard")
    
@app.route("/applicant/logout")
def applicant_logout():
    print(f"Session Applicant Status: {session['applicant']}")
    session["applicant"] = False
    print(f"Session Applicant Status: {session['applicant']}")
    return redirect(url_for("landing"))

@app.route("/applicant/details", methods=["GET", "POST"])
def applicant_details():
    if session["applicant"] == True:
        if request.method == "GET":
            return render_template("applicant_details.html", email=session["user-email"])
        elif request.method == "POST":
            data = {
                "name": request.form.get("name"),
                "email": request.form.get("email"),
                "phone": request.form.get("phone"),
                "location": request.form.get("location"),
                "skills": request.form.get("skills")
            }
            user_resume = request.files.get("resume")

            # users database
            u = Users()
            print(session["user-email"])
            uid = u.get_id(session["user-email"])

            # save resume file
            if user_resume and allowed_file(user_resume.filename):
                # Create uploads folder if it doesn't exist
                if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                    os.makedirs(app.config["UPLOAD_FOLDER"])
                
                # Save the file with user-defined name
                file_extension = os.path.splitext(user_resume.filename)[1]
                saved_filename = f"{uid}_resume{file_extension}"
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], saved_filename)
                try:
                    user_resume.save(save_path)
                    data["resume_path"] = save_path
                except Exception as e:
                    return {"error": f"File saving failed: {str(e)}"}, 500
            else:
                return {"error": "Invalid file type or missing file"}, 400
            
            # Save user data to JSON file
            json_data = read_json("users.json")
            json_data[uid] = data
            write_json("users.json", json_data)

            return redirect(url_for("applicant_dashboard"))
    else:
        return redirect(url_for("applicant_login"))

@app.route("/applicant/dashboard")
def applicant_dashboard():
    openings = Openings()
    data = openings.get_all()
    return render_template("applicant_dashboard.html", data=data)

@app.route("/applicant/slide/<companyname>/<listingid>")
def applicant_slide(companyname, listingid):
    if "applicant" in session and session["applicant"] == True:
        heading = "Get Ready for the Virtual Interview"
        para = "You'll be under observation for the next 20 minutes, kindly maintain the decency, be confident and answer the questions asked by the Virtual interviewer. This activity will be recorded."
        openings = Openings()
        data = openings.get_all()
        data = data[companyname][listingid]
        return render_template("applicant_slide.html", heading=heading, para=para, data=data, companyname=companyname, listingid=listingid)
    else:
        return redirect(url_for("applicant_login"))

@app.route('/applicant/qna/<companyname>/<listingid>', methods=["GET", "POST"])
def applicant_qna(companyname, listingid):
    if request.method == "GET":
        openings = Openings()
        data = openings.get_all()
        data = data[companyname][listingid]
        q = QnA(job_title=data["user_role"], job_description=data["description"])
        question_asked = []

        #question to ask
        question_to_ask = 5

        for i in range(question_to_ask):
            quest = q.generate_question(question_asked)
            print(quest)
            question_asked.append(quest['question'])
        questions = {}
        c = 1
        for i in question_asked:
            questions[c] = i
            c+=1
        return render_template("applicant_qna.html", questions=questions, companyname=companyname, listingid=listingid)
    elif request.method == "POST":
        return redirect(url_for("video_interview"))

@app.route('/applicant/submit-answer', methods=["POST"])
def applicant_submit():
    if request.method == "POST":
        data = {
            "1": {
                "question": "Tell us about a time when you faced a challenge at work and how you overcame it.",
                "answer": request.form.get("answer1")
            },
            "2": {
                "question": "Describe a time when you had to work in a team to achieve a goal. How did you contribute?",
                "answer": request.form.get("answer2")
            }
        }
        return data

@app.route('/applicant/video_interview')
def video_interview():
    return render_template("video_interview.html")

# Set up logging for better error tracking
logging.basicConfig(level=logging.DEBUG)

@app.route('/applicant/analyze', methods=['POST'])
def analyze():
    try:
        # Get the base64-encoded image from the request
        data_url = request.json.get("image")
        if not data_url:
            return jsonify({"error": "No image data provided"}), 400

        # Decode the base64 image
        logging.debug("Received base64 image data, starting decoding.")
        image_data = base64.b64decode(data_url.split(",")[1])
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise Exception("Failed to decode image.")

        # Analyze the emotion using DeepFace
        logging.debug("Image decoded successfully, performing emotion analysis.")
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)

        dominant_emotion = result[0]['dominant_emotion']
        extended_emotion = emotion_mappings.get(dominant_emotion, "Unknown")

        return jsonify({
            "dominant_emotion": dominant_emotion,
            "extended_emotion": extended_emotion
        })
    except Exception as e:
        logging.error(f"Error occurred during emotion analysis: {e}")
        return jsonify({"error": str(e)}), 500

# @app.route("/applicant/resume")
# def resume():
#     return render_template("resume.html")  

# @app.route("/upload", methods=["POST"])
# def upload_file():
#     if "file" not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files["file"]

#     if file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#         file.save(file_path)

#         try:
#             # Extract text from the uploaded file
#             file_content = analyzer.extract_text(file_path)
#             # Analyze resume content
#             analysis = analyzer.analyze(file_content)
#             return jsonify({"message": "File uploaded successfully", "analysis": analysis})
#         except ValueError as e:
#             return jsonify({"error": str(e)}), 400
#         except Exception as e:
#             return jsonify({"error": "An error occurred", "details": str(e)}), 500

#     return jsonify({"error": "Invalid file type"}), 400

#################
# main function #
#################
if __name__ == "__main__":
    app.run(debug=True)
