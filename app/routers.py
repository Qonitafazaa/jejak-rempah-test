# from flask import Blueprint, request, jsonify
# from .utils import process_image, get_rempah_info

# api = Blueprint('api', __name__)

# @api.route('/scan', methods=['POST'])
# def scan_image():
#     if 'image' not in request.files:
#         return jsonify({"status": "failed", "message": "No image file provided"}), 400

#     image = request.files['image']
#     rempah_name = process_image(image)  # Memproses gambar untuk mengenali rempah

#     if not rempah_name:
#         return jsonify({"status": "failed", "message": "Rempah not recognized"}), 404

#     rempah_info = get_rempah_info(rempah_name)
#     if not rempah_info:
#         return jsonify({"status": "failed", "message": "No information found for the rempah"}), 404

#     return jsonify({
#         "status": "success",
#         "data": {
#             "name": rempah_info["name"],
#             "benefits": rempah_info["benefits"],
#             "funfact": rempah_info["funfact"],
#             "history": rempah_info["history"],
#             "shopee_link": rempah_info["shopee_link"],
#             "image_urls": rempah_info["image_urls"]  # Menambahkan gambar rempah
#         }
#     }), 200

# INI KODE BARU YAAA

from flask import Blueprint, request, jsonify
from app.utils import validate_rempah
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Membuat Blueprint untuk API
api = Blueprint('api', __name__)

@api.route('/scan', methods=['POST'])
def scan_image():
    """
    Endpoint untuk memproses gambar dan memvalidasi apakah itu rempah.
    """
    if 'image' not in request.files:
        logging.error("No image file provided")
        return jsonify({"message": "No image file provided", "status": "failed"}), 400

    file = request.files['image']
    logging.debug(f"Uploaded file: {file.filename}, Content-Type: {file.content_type}")

    if file.filename == '':
        logging.error("No selected file")
        return jsonify({"message": "No selected file", "status": "failed"}), 400

    # Mengecek apakah file yang diupload adalah gambar dengan ekstensi yang diperbolehkan
    allowed_extensions = ['jpg', 'jpeg', 'png', 'gif']
    filename = file.filename.lower()
    if not any(filename.endswith(ext) for ext in allowed_extensions):
        logging.error(f"Invalid image file type: {file.filename}")
        return jsonify({"message": "Invalid image file type", "status": "failed"}), 400

    # Memproses dan memvalidasi gambar
    try:
        result = validate_rempah(file)
        if result["success"]:
            logging.info("categories detected successfully")
            return jsonify({
                "message": "categories detected",
                "status": "success",
                "data": {"rempah_name": result["name"]}
            }), 200
        else:
            logging.warning(f"Validation failed: {result['message']}")
            return jsonify({
                "message": result["message"],
                "status": "failed"
            }), 400
    except Exception as e:
        logging.error(f"Error during rempah validation: {e}")
        return jsonify({"message": "Error during validation", "status": "failed"}), 500
