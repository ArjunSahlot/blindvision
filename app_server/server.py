from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from picamera2 import Picamera2
import cv2
from ai import ChatBot

app = Flask(__name__, template_folder=".")
socketio = SocketIO(app)
camera = Picamera2()
camera.start()

@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("default")
def default(var):
    print("Default event received!")
    emit("tts", {"message": "raspberry pi thinks you picked default"}, broadcast=True)

@socketio.on("risks")
def default(var):
    print("Risks event received!")
    emit("tts", {"message": "raspberry pi thinks you picked risks"}, broadcast=True)

@socketio.on("chat")
def default(var):
    print(f"Chat event received: {var['message']}!")
    emit("tts", {"message": f"raspberry pi thinks you picked chat: {var['message']}"}, broadcast=True)

@socketio.on("camera")
def default(var):
    print("Camera event received!")
    pic = camera.capture_array("main")
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    cv2.imwrite("pic.jpg", pic)
    emit("tts", {"message": "Picture updated!"}, broadcast=True)

socketio.run(app, host="0.0.0.0", port=5000)
