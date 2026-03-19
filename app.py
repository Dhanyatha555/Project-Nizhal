from flask import Flask, request, jsonify
import os
from handler import process_image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        file = request.files['image']

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        result = process_image(file_path)

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)