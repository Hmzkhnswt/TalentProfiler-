import os
import pickle
import re
import nltk
import pdfplumber
from flask import Flask, request, render_template

# Load the classifier and CV from pickle files
clf = pickle.load(open('Resume Parsing\clf.pkl', 'rb'))
cv = pickle.load(open('Resume Parsing\cv.pkl', 'rb'))

app = Flask(__name__)

# Function to clean the resume text
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)  
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText

# Function to extract skills from a resume
def extract_skills_from_resume(resume_text, skills_list):
    # Tokenize the resume text using NLTK
    tokens = nltk.word_tokenize(resume_text, language="english", preserve_line= "False")
    # Extract skills that exist in the skills_list and are present in the resume
    skills = [skill.lower() for skill in skills_list if skill.lower() in [token.lower() for token in tokens]]
    return skills
skills_list = [
    "Python","Java","JavaScript","C++","SQL","Data Analysis","Machine Learning","Deep Learning","Artificial Intelligence (AI)",
    "Natural Language Processing (NLP)","Data Mining","Data Visualization","Statistical Analysis","Cloud Computing (e.g., AWS, Azure)",
    "DevOps","Docker","Kubernetes","Web Development","Mobile App Development","Front-End Development","Back-End Development","Full-Stack Development",
    "Agile Methodology","Scrum","Project Management","Leadership","Teamwork","Communication","Problem Solving","Critical Thinking","Creativity","UX/UI Design",
    "Cybersecurity","Network Administration","Database Management","Big Data","Internet of Things (IoT)","Blockchain","Robotics","Automation",
    "Quality Assurance (QA)","Technical Support","Sales","Marketing","Content Writing","Graphic Design","Customer Service",
    "Financial Analysis","Legal Knowledge","Healthcare Management","Pandas","Numpy","Matplotlib","Seaborn","Sklearn","Algorithms"
]

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'resume' not in request.files:
            return render_template('upload.html', message='No file part')

        resume_file = request.files['resume']

        # Check if the file has an allowed extension
        if resume_file.filename == '':
            return render_template('upload.html', message='No selected file')

        if resume_file:
            # Save the uploaded file to the 'static' directory
            file_extension = resume_file.filename.rsplit('.', 1)[1].lower()
            if file_extension in ['pdf', 'docx']:
                if not os.path.exists('static'):
                    os.makedirs('static')

                resume_path = os.path.join('static', 'uploaded_resume.' + file_extension)
                resume_file.save(resume_path)

                # Extract text from PDF or DOCX file
                if file_extension == 'pdf':
                    with pdfplumber.open(resume_path) as pdf:
                        pdf_text = ""
                        for page in pdf.pages:
                            pdf_text += page.extract_text()
                    resume_text = pdf_text
                elif file_extension == 'docx':
                    import docx2txt
                    resume_text = docx2txt.process(resume_path)

                # Clean the resume text
                cleaned_resume = cleanResume(resume_text)

                # Extract skills from the cleaned resume text
                skills = extract_skills_from_resume(cleaned_resume, skills_list)

                # Transform the cleaned resume text using CountVectorizer
                input_features = cv.transform([cleaned_resume])

                # Predict the category
                prediction_id = clf.predict(input_features)[0]

                category_mapping = {
                    15: "Java Developer",
                    23: "Testing",
                    8: "DevOps Engineer",
                    20: "Python Developer",
                    24: "Web Designing",
                    12: "HR",
                    13: "Hadoop",
                    3: "Blockchain",
                    10: "ETL Developer",
                    18: "Operations Manager",
                    6: "Data Science",
                    22: "Sales",
                    16: "Mechanical Engineer",
                    1: "Arts",
                    7: "Database",
                    11: "Electrical Engineering",
                    14: "Health and fitness",
                    19: "PMO",
                    4: "Business Analyst",
                    9: "DotNet Developer",
                    2: "Automation Testing",
                    17: "Network Security Engineer",
                    21: "SAP Developer",
                    5: "Civil Engineer",
                    0: "Advocate"
                }

                category_name = category_mapping.get(prediction_id, "Unknown")

                return render_template('upload.html', message=f'Category: {category_name}', skills=skills)

    return render_template('upload.html', message='Upload a resume')

if __name__ == '__main__':
    app.run(debug=True)
