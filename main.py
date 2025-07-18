from flask import Flask, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from converter import bionic_pdf_converter
import os

app = Flask(__name__)
CORS(app)  # Engedélyezi a külső domainről jövő kéréseket (pl. Google Sites)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/ping")
def ping():
    return "pong", 200

@app.route("/convert", methods=["POST"])
def convert():
    if "pdf" not in request.files:
        return "❌ Nincs PDF fájl a kérésben.", 400

    pdf_file = request.files["pdf"]
    filename = secure_filename(pdf_file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"bionic_{filename}")

    pdf_file.save(input_path)

    try:
        bionic_pdf_converter(input_path, output_path)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return f"Hiba a konvertálás során: {str(e)}", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
