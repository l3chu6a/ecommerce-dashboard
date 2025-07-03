# from flask import Blueprint, request, jsonify
# import os

# api = Blueprint("api", __name__)
# UPLOAD_FOLDER = "data"

# @api.route("/upload", methods=["POST"])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400

#     filepath = os.path.join(UPLOAD_FOLDER, "uploaded_settlement.csv")
#     file.save(filepath)
#     return jsonify({"message": f"File saved to {filepath}"}), 200


from flask import Blueprint, request, jsonify
import os

api = Blueprint("api", __name__)
BASE_FOLDER = "data"

@api.route("/upload", methods=["POST"])
def upload_file():
    client_id = request.form.get("client_id")
    if not client_id:
        return jsonify({"error": "client_id is required"}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    client_folder = os.path.join(BASE_FOLDER, client_id)
    os.makedirs(client_folder, exist_ok=True)

    # filepath = os.path.join(client_folder, "uploaded_settlement.csv")
    original_filename = file.filename
    prefixed_filename = f"upload_{original_filename}"
    filepath = os.path.join(client_folder, prefixed_filename)

    file.save(filepath)

    return jsonify({"message": f"File saved to {filepath}"}), 200
