from flask import Flask, request, send_file
from flask_sock import Sock
import os
import threading

app = Flask(__name__)
sock = Sock(app)
IMAGE_PATH = "latest.jpg"
INDEX_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web", "index.html"))
_clients = set()
_clients_lock = threading.Lock()

@app.route("/upload", methods=["POST"])
def upload():
    try:
        with open(IMAGE_PATH, "wb") as f:
            f.write(request.data)
        _broadcast(request.data)
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
    if os.path.exists(INDEX_PATH):
        return send_file(INDEX_PATH)
    return "<h1>Server running</h1>"

@sock.route("/ws")
def ws_client(ws):
    with _clients_lock:
        _clients.add(ws)
    try:
        if os.path.exists(IMAGE_PATH):
            with open(IMAGE_PATH, "rb") as f:
                ws.send(f.read())
        while True:
            msg = ws.receive()
            if msg is None:
                break
    finally:
        with _clients_lock:
            _clients.discard(ws)

@sock.route("/ws-upload")
def ws_upload(ws):
    while True:
        data = ws.receive()
        if data is None:
            break
        if isinstance(data, str):
            continue
        with open(IMAGE_PATH, "wb") as f:
            f.write(data)
        _broadcast(data)

def _broadcast(data):
    dead = []
    with _clients_lock:
        for client in _clients:
            try:
                client.send(data)
            except Exception:
                dead.append(client)
        for client in dead:
            _clients.discard(client)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
