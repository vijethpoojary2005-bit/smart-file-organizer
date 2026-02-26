from flask import Flask, render_template, request
import os
import shutil
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/organize", methods=["POST"])
def organize():

    folder_path = request.form.get("folder_path").strip()
    sort_option = request.form.get("sort_option")

    # Check if folder exists
    if not os.path.isdir(folder_path):
        return "❌ Invalid Folder Path! Please check and try again."

    # File type categories
    image_ext = ["jpg", "jpeg", "png", "gif", "bmp"]
    video_ext = ["mp4", "mkv", "avi", "mov"]
    audio_ext = ["mp3", "wav", "aac"]
    document_ext = ["pdf", "docx", "txt", "pptx", "xlsx"]

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        # Skip if it's already a folder
        if not os.path.isfile(file_path):
            continue

        # Get file extension
        if "." in filename:
            file_ext = filename.split(".")[-1].lower()
        else:
            file_ext = ""

        # Get last modified date
        timestamp = os.path.getmtime(file_path)
        file_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

        # SORTING LOGIC
        if sort_option == "type":

            if file_ext in image_ext:
                folder_name = "Images"
            elif file_ext in video_ext:
                folder_name = "Videos"
            elif file_ext in audio_ext:
                folder_name = "Audio"
            elif file_ext in document_ext:
                folder_name = "Documents"
            else:
                folder_name = "Others"

        elif sort_option == "date":
            folder_name = file_date

        elif sort_option == "both":

            if file_ext in image_ext:
                main_type = "Images"
            elif file_ext in video_ext:
                main_type = "Videos"
            elif file_ext in audio_ext:
                main_type = "Audio"
            elif file_ext in document_ext:
                main_type = "Documents"
            else:
                main_type = "Others"

            folder_name = f"{main_type}_{file_date}"

        else:
            folder_name = "Others"

        target_folder = os.path.join(folder_path, folder_name)

        # Create folder if not exists
        os.makedirs(target_folder, exist_ok=True)

        # Move file
        shutil.move(file_path, os.path.join(target_folder, filename))

    return "✅ Files Organized Successfully!"


# 🔹 Important for Online Deployment (Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)