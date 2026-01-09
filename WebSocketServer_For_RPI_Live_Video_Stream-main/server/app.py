from flask import Flask, request, send_file
import os

app = Flask(__name__)
IMAGE_PATH = "latest.jpg"

@app.route("/upload", methods=["POST"])
def upload():
    try:
        with open(IMAGE_PATH, "wb") as f:
            f.write(request.data)
        return "OK", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route("/latest.jpg")
def latest():
    if not os.path.exists(IMAGE_PATH):
        return "No image", 404
    return send_file(IMAGE_PATH, mimetype="image/jpeg")

@app.route("/")
def index():
    return "<h1>Server running</h1>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
