import os
from flask import Flask, request, jsonify
import oss2

app = Flask(__name__)

# 从环境变量读取配置
OSS_ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID")
OSS_ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET")
OSS_BUCKET = os.getenv("OSS_BUCKET")
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT")
OSS_FOLDER_PREFIX = os.getenv("OSS_FOLDER_PREFIX", "")

auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    key = f"{OSS_FOLDER_PREFIX}{file.filename}"
    bucket.put_object(key, file.stream)
    url = f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{key}"
    return jsonify({"url": url})

@app.route("/healthz")
def healthz():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)