import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import oss2

app = Flask(__name__)

# 从环境变量获取配置
OSS_ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID")
OSS_ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET")
OSS_BUCKET = os.getenv("OSS_BUCKET")
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT")
OSS_FOLDER_PREFIX = os.getenv("OSS_FOLDER_PREFIX", "")

# 初始化 OSS 授权
auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    filename = secure_filename(file.filename)
    upload_path = OSS_FOLDER_PREFIX + filename if OSS_FOLDER_PREFIX else filename
    bucket.put_object(upload_path, file)
    file_url = f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{upload_path}"
    return jsonify({"url": file_url})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
