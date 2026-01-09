import cv2
import time
from websocket import create_connection

SERVER_URL = "wss://websocketserver-for-rpi-live-video.onrender.com/ws-upload"

cap = cv2.VideoCapture(0)

def _connect():
    return create_connection(SERVER_URL, timeout=10)

ws = None
while True:
    if ws is None:
        try:
            ws = _connect()
        except Exception as e:
            print(f"WebSocket connect error: {e}")
            time.sleep(2)
            continue

    ret, frame = cap.read()
    if not ret:
        continue

    _, buffer = cv2.imencode(".jpg", frame)
    try:
        ws.send(buffer.tobytes(), opcode=0x2)
    except Exception as e:
        print(f"WebSocket send error: {e}")
        try:
            ws.close()
        except Exception:
            pass
        ws = None
        time.sleep(1)
        continue

    time.sleep(0.1)  # ~10 FPS
