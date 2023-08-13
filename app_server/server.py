from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from picamera2 import Picamera2
import cv2
from ai import ChatBot

app = Flask(__name__, template_folder=".")
socketio = SocketIO(app)
camera = Picamera2()
camera.start()
chatbot = ChatBot()


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected!")


@socketio.on("default")
def default(var):
    print("Default event received!")
    ready = chatbot.image_ready()
    if ready[0]:
        emit("tts", {"message": chatbot.risks()}, broadcast=True)
    else:
        emit("tts", {"message": ready[1]}, broadcast=True)
    emit("tts", {"message": ""}, broadcast=True)


@socketio.on("risks")
def risks(var):
    print("Risks event received!")
    ready = chatbot.image_ready()
    if ready[0]:
        emit("tts", {"message": chatbot.risks()}, broadcast=True)
    else:
        emit("tts", {"message": ready[1]}, broadcast=True)


@socketio.on("chat")
def chat(var):
    print(f"Chat event received: {var['message']}!")
    ready = chatbot.image_ready()
    if ready[0]:
        emit("tts", {"message": chatbot.chat(var["message"])}, broadcast=True)
    else:
        emit("tts", {"message": ready[1]}, broadcast=True)


@socketio.on("camera")
def camera_(var):
    print("Camera event received!")
    pic = camera.capture_array("main")
    pic = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
    cv2.imwrite("pic.jpg", pic)
    emit("tts", {"message": "Picture updated!"}, broadcast=True)
    try:
        chatbot.refresh_image()
    except Exception as e:
        print(e)
        emit(
            "tts",
            {"message": "Error updating picture! Please try again later!"},
            broadcast=True,
        )


@socketio.on("refresh")
def refresh(var):
    print("Refresh event received!")
    chatbot.refresh_chat()
    emit("tts", {"message": "Chat refreshed!"}, broadcast=True)


socketio.run(app, host="0.0.0.0", port=5000)
