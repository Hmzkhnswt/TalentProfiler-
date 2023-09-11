# TalentProfiler
# Resume Classifier

The Resume Classifier is a web application that allows users to upload a resume in PDF or DOCX format, and it extracts skills from the resume while predicting the most relevant job category based on the content using a machine learning classifier.

## Features

- Upload a resume in PDF or DOCX format.
- Extract skills from the resume text.
- Predict and display the most relevant job category.
- User-friendly web interface.

## Prerequisites

Before running the application, make sure you have the following installed:

- Python 3.x
- Required Python libraries (specified in `requirements.txt`)
- Pickle files for the classifier and CountVectorizer (`clf.pkl` and `cv.pkl`)
- Flask (web framework)
- Pdfplumber (for PDF text extraction)
- Docx2txt (for DOCX text extraction)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/Hmzkhnswt/resume-classifier.git
   ```

2. Install the required Python libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Place the `clf.pkl` and `cv.pkl` pickle files in the project directory.

4. Run the Flask application:

   ```bash
   python app.py
   ```

5. Access the application in your web browser at `http://localhost:5000`.

## Usage

1. Upload a resume file in PDF or DOCX format using the provided form.

2. Click the "Upload" button.

3. The application will process the resume, extract skills, predict the job category, and display the results on the web page.

## Customization

- Skills List: You can customize the list of skills in the `skills_list` variable in the `app.py` script to match the specific skills you want to extract.

- Category Mapping: You can modify the `category_mapping` dictionary in the `app.py` script to customize the job categories and their corresponding IDs.


## Acknowledgments

- This project uses [Flask](https://flask.palletsprojects.com/) for web development.
- Text extraction from PDF files is done with [Pdfplumber](https://github.com/jsvine/pdfplumber).
- Text extraction from DOCX files is done with [Docx2txt](https://pypi.org/project/docx2txt/).

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your improvements.

## Contact

For questions or issues related to this project, feel free to contact the project maintainer: hamzakhanswati117191@gmail.com

