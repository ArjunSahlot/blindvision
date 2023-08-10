from flask import Flask, render_template, Response
import cv2
import numpy as np
from picamera2 import Picamera2

app = Flask(__name__, template_folder=".")
camera = Picamera2()
camera.start()

def generate_frames(): 
    while True:
        frame = camera.capture_array("main")
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ret, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video")
def video():
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
