from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from zipfile import ZipFile
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    zip_path = filepath + '.zip'
    with ZipFile(zip_path, 'w') as zipf:
        zipf.write(filepath, arcname=filename)

    os.remove(filepath)
    return send_file(zip_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
