from flask import Flask, render_template, request, send_file
import os
import shutil
from werkzeug.utils import secure_filename
from zipfile import ZipFile

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ORGANIZED_FOLDER = "organized"

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ORGANIZED_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/organize", methods=["POST"])
def organize():

    # Clear old files
    shutil.rmtree(UPLOAD_FOLDER)
    shutil.rmtree(ORGANIZED_FOLDER)
    os.makedirs(UPLOAD_FOLDER)
    os.makedirs(ORGANIZED_FOLDER)

    files = request.files.getlist("files")

    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        ext = filename.split(".")[-1].lower()

        category_path = os.path.join(ORGANIZED_FOLDER, ext)
        os.makedirs(category_path, exist_ok=True)

        shutil.move(filepath, os.path.join(category_path, filename))

    # Create ZIP
    zip_path = "organized_files.zip"
    with ZipFile(zip_path, "w") as zipf:
        for root, dirs, files in os.walk(ORGANIZED_FOLDER):
            for file in files:
                full_path = os.path.join(root, file)
                zipf.write(full_path)

    return send_file(zip_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)