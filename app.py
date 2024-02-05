from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import fitz  # PyMuPDF
import spacy
from collections import Counter

app = Flask(__name__, template_folder='public')

app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Adjust the folder as needed
nlp = spacy.load("en_core_web_sm")

# Home page route
@app.route("/")
def index():
    return render_template("templates/index.html")

# Serve files from the 'public' directory
@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory('public', filename)

# Extract text from uploaded PDF or job description
@app.route("/extract-text", methods=["POST"])
def extract_text():
    try:
        pdf_file = request.files.get("pdfFile")
        job_description = request.form.get("jobDescription")

        if pdf_file:
            pdf_text = extract_text_from_pdf(pdf_file)
            return jsonify({"extractedText": pdf_text})
        
        elif job_description:
            pdf_text = request.form.get("pdfText")
            similarity_score = calculate_similarity(pdf_text, job_description)
            return jsonify({"similarityScore": similarity_score * 100})  # Return similarity score as a percentage
        else:
            return jsonify({"error": "No text provided"})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error processing text"})

# Get common coding skills based on the provided job description
@app.route("/common-skills", methods=["POST"])
def common_skills():
    try:
        pdf_text = request.form.get("pdfText")
        job_description = request.form.get("jobDescription")  # Get the job description
        doc = nlp(pdf_text)
        common_skills = get_coding_skills(doc, job_description)
        return jsonify({"commonSkills": common_skills})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error processing text"})

# Extract text content from a PDF file
def extract_text_from_pdf(pdf_file):
    result = ""
    try:
        pdf_content = pdf_file.read()
        with fitz.open("pdf", pdf_content) as doc:
            for page in doc:
                result += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
    return result

# Calculate similarity score between the resume and job description
def calculate_similarity(pdf_text, job_description):
    doc1 = nlp(pdf_text)
    doc2 = nlp(job_description)
    similarity_score = doc1.similarity(doc2)
    return similarity_score

# Get coding skills mentioned in the document based on the job description
def get_coding_skills(doc, job_description):
    # Extract coding terms from the job description
    job_coding_terms = extract_coding_terms(job_description)
    
    # Filter out only coding terms from the document
    doc_coding_skills = [token.text.lower() for token in doc if token.text.lower() in job_coding_terms]
    
    return doc_coding_skills

# Extract coding terms from the job description
def extract_coding_terms(job_description):
    # This is a simple example; you can customize this based on your coding terminology
    # Extracting coding terms from the job description (e.g., using spaCy)
    job_doc = nlp(job_description)
    coding_terms = [
    "python", "javascript", "java", "html", "css", "sql", 
    "c", "c++", "c#", "ruby", "php", "swift", "kotlin", "typescript", 
    "react", "angular", "vue", "node.js", "express.js", "django", "flask", 
    "spring", "laravel", "html5", "css3", "sass", "less", "bootstrap", 
    "jquery", "ajax", "json", "rest", "graphql", 
    "mysql", "postgresql", "mongodb", "sqlite", "firebase", 
    "machine learning", "deep learning", "neural networks", "data science", 
    "numpy", "pandas", "matplotlib", "seaborn", "scikit-learn", 
    "tensorflow", "keras", "pytorch", "natural language processing", 
    "docker", "kubernetes", "git", "github", "bitbucket", 
    "agile", "scrum", "kanban", "devops", "continuous integration", 
    "webpack", "gulp", "babel", "eslint", "jest", 
    "jenkins", "travis-ci", "heroku", "aws", "azure", "google cloud"
    # Add more as needed
]
    
    job_coding_terms = [term.lower() for term in coding_terms if term.lower() in [token.text.lower() for token in job_doc]]
    
    return job_coding_terms

# Get frequent nouns in the document
@app.route("/frequent-nouns", methods=["POST"])
def frequent_nouns():
    try:
        pdf_text = request.form.get("pdfText")
        doc = nlp(pdf_text)
        
        # Filter out only nouns from the document
        nouns = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
        
        # Remove spaces and convert to lowercase for better word counting
        word_counts = Counter(nouns)
        frequent_nouns = word_counts.most_common(10)  # Change 10 to the desired number of words
        
        return jsonify({"frequentNouns": frequent_nouns})

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Error processing text"})

if __name__ == "__main__":
    app.run(debug=True)
