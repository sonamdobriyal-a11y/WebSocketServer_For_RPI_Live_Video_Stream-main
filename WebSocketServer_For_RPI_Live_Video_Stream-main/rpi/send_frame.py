import cv2
import requests
import time

SERVER_URL = "https://your-render-app.onrender.com/upload"

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    _, buffer = cv2.imencode('.jpg', frame)
    response = requests.post(SERVER_URL, data=buffer.tobytes(), headers={"Content-Type": "image/jpeg"})
    print(f"Sent frame: {response.status_code}")

    time.sleep(0.5)  # ~2 FPS
