import os
from flask import Flask, request, jsonify
import oss2
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 从环境变量中获取 OSS 配置
OSS_ACCESS_KEY_ID = os.environ.get("OSS_ACCESS_KEY_ID")
OSS_ACCESS_KEY_SECRET = os.environ.get("OSS_ACCESS_KEY_SECRET")
OSS_BUCKET = os.environ.get("OSS_BUCKET")
OSS_ENDPOINT = os.environ.get("OSS_ENDPOINT")
OSS_FOLDER_PREFIX = os.environ.get("OSS_FOLDER_PREFIX", "")

auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    oss_path = OSS_FOLDER_PREFIX + filename
    bucket.put_object(oss_path, file.stream)

    url = f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{oss_path}"
    return jsonify({"url": url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)