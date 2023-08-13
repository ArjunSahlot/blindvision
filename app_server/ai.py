import requests
import base64
import os
import time
import pytesseract
from copy import deepcopy
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


class ChatBot:
    def __init__(self):
        self.message_history = []
        self.image = {}
        self.rejected = False

        self.refresh_chat()

    def image_ready(self):
        if not self.image:
            return (
                False,
                "No image has been taken yet. Press the camera button to take an image.",
            )
        age = time.time() - self.image["time"]
        if not self.rejected and age > 120:
            return (
                False,
                f"Current image was taken over {age//60} minutes ago, are you sure you want to use this image? Click the button again if you want to reuse it, click the camera button if you want to reset it!",
            )
        self.rejected = False
        return (True, "Image is ready to be described!")

    def refresh_chat(self):
        self.message_history = [
            {
                "role": "system",
                "content": self.start_message(),
            }
        ]

    def chat(self, prompt):
        self.message_history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )
        return self.chatgpt()

    def default(self):
        return self.chat(
            "Please summarize this information accurately and descriptively in simple language with a couple sentences so that it is easy and quick for me to understand. This is not an art piece, this is just a picture from my camera, so please do not be creative or poetic, just describe my situation."
        )

    def risks(self):
        return self.chat(
            "Being a blind person, the world can be very dangerous. I need to be aware of my surroundings and any potential risks. Please describe any potential risks in the image."
        )

    def start_message(self):
        string = (
            "I am a blind person. I have used a vision AI to come up with a description of what I am seeing. Here it is:\n"
            + self.image["description"]
            + "\n\n"
        )
        objects = ", ".join(
            [obj["name"] for obj in self.image["objects"] if obj["confidence"] > 0.7]
        ).strip()
        if objects:
            string += (
                "I have also used an object detection AI to identify the objects in the image. Here they are:\n"
                + objects
                + "\n\n"
            )
        if self.image["ocr"]:
            string += (
                "I have also used an OCR AI to read any text in the image. Here it is:\n"
                + self.image["ocr"]
                + "\n\n"
            )

        return string.strip()

    def chatgpt(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.message_history
        )
        reply = response.choices[0].message.content.strip()
        print(reply)
        self.message_history.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )
        return reply

    def refresh_image(self):
        asticaAPI_timeout = 60

        asticaAPI_endpoint = "https://astica.ai:9141/vision/describe"
        asticaAPI_modelVersion = "2.1_full"

        path_to_local_file = "pic.jpg"
        with open(path_to_local_file, "rb") as file:
            image_data = file.read()
        image_extension = os.path.splitext(path_to_local_file)[1]
        asticaAPI_input = f"data:image/{image_extension[1:]};base64,{base64.b64encode(image_data).decode('utf-8')}"

        asticaAPI_visionParams = "objects, gpt"

        asticaAPI_payload = {
            "tkn": os.getenv("ASTICA_KEY"),
            "modelVersion": asticaAPI_modelVersion,
            "visionParams": asticaAPI_visionParams,
            "input": asticaAPI_input,
        }

        response = requests.post(
            asticaAPI_endpoint,
            data=asticaAPI_payload,
            timeout=asticaAPI_timeout,
            verify=False,
        )
        if response.status_code == 200:
            asticaAPI_result = response.json()
        else:
            asticaAPI_result = {
                "status": "error",
                "error": "Failed to connect to the API.",
            }

        text = pytesseract.image_to_string("pic.jpg").strip()
        asticaAPI_result["ocr"] = text
        asticaAPI_result["description"] = asticaAPI_result.pop("caption_GPTS")
        asticaAPI_result["time"] = time.time()
        print(asticaAPI_result)

        self.image = deepcopy(asticaAPI_result)


ChatBot().describe()
