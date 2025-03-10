# Resume Analyzer
![alt text](https://github.com/MercifulB/Resume-Analyzer/blob/main/Resume_analyzer1.png?raw=true)

# Overview
This Resume Analyzer is a web application that allows users to analyze resumes and job descriptions for relevant information. The application extracts text from PDF resumes, compares them with a provided job description, and displays common technical skills, frequently mentioned words, and a similarity score between their resume and the job description.

# Instructions

# Prerequisites
1. Python installed (version 3.6 or higher)
2. Node.js installed
3. npm (Node Package Manager) installed

# Installation
1. Clone the repository and download:
   - git clone https://github.com/MercifulB/Resume-Analyzer.git

2. Install dependencies:
   Open a new terminal and intall the following using these lines:
   - npm install
   - pip install Flask spacy
   - python -m spacy download en_core_web_sm
   - pip install pymupdf

3. Run the app:
   Type the following in the terminal:
   - python app.py

# Approach
To tackle this project I started by simple front end HTML/JS/CSS with node.js backend to create a simple UI for uploading resume text
and a job desc. I then used Javascript to parse over the PDF if it was uploaded taking advantage of pdfParse and 
express-fileupload from the express.js framework. Next, I used the Flask Python backend framework to create a Flask app and
serve frontend files. I used the spaCy Natural Language Processing library to compare the resume and job desc. text and return 
a similarity score and comparing smilar common nouns. To extract text from the PDF on the server side I used the PyMuPDF Python 
library. 

# Tools Used
# Frontend:
- The frontend is implemented using:
  - HTML
  - CSS
  - JavaScript
- It uses the Fetch API to communicate with the backend.

# Backend:
The backend is implemented using:
- Flask (Python) for the backend server
- spaCy (Python) a library for natural language processing
- PyMuPDF (Python) for PDF parsing
- Node.js for the frontend server
- Express.js (Node.js) for the API
- pdf-parse (Node.js) for PDF parsing

# Demo
https://drive.google.com/file/d/1GuA2Kb6mT4pNOkavWqth9wSUMF89DIvC/view?usp=sharing
