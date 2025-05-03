
import os
from flask import Flask, request, jsonify
import oss2
import base64
import uuid

app = Flask(__name__)

access_key_id = os.environ.get("ALIYUN_ACCESS_KEY_ID")
access_key_secret = os.environ.get("ALIYUN_ACCESS_KEY_SECRET")
endpoint = os.environ.get("ALIYUN_OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")
bucket_name = os.environ.get("ALIYUN_BUCKET_NAME", "xhs-image-proxy")

auth = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(auth, endpoint, bucket_name)

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.json
        base64_data = data.get('base64')
        if not base64_data:
            return jsonify({"error": "base64 data missing"}), 400

        image_data = base64.b64decode(base64_data.split(",")[-1])
        filename = f"{uuid.uuid4()}.jpg"

        bucket.put_object(filename, image_data)
        url = f"https://{bucket_name}.{endpoint}/{filename}"

        return jsonify({"message": "Upload successful", "url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
