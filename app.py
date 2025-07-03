from flask import Flask, request, render_template
import os
import fitz  # PyMuPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html', text=None)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    file = request.files.get('pdfFile')
    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Extract text using PyMuPDF
        doc = fitz.open(file_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        doc.close()

        return render_template('index.html', text=full_text)

    return "Please upload a valid PDF file."

if __name__ == '__main__':
    app.run(debug=True)
