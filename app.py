from flask import Flask, request, redirect, url_for, render_template
from google.cloud import storage
import os

app = Flask(__name__)

# Configuration
GCS_BUCKET_NAME = 'medical_dat'

def upload_to_gcs(file, filename):
    """Upload a file to a GCS bucket."""
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_file(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return 'No file part'
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return 'No selected file'
    uploaded_files = []
    for file in files:
        filename = file.filename
        upload_to_gcs(file, filename)
        uploaded_files.append(filename)
    return f'Files {", ".join(uploaded_files)} uploaded to {GCS_BUCKET_NAME}.'

if __name__ == '__main__':
    app.run(debug=True)
