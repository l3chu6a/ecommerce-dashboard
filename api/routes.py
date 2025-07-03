from flask import Blueprint, request, jsonify
import os

api = Blueprint("api", __name__)
UPLOAD_FOLDER = "data"

@api.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, "uploaded_settlement.csv")
    file.save(filepath)
    return jsonify({"message": f"File saved to {filepath}"}), 200
