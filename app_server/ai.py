import requests
import base64
import os
import pytesseract
from copy import deepcopy
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


class ChatBot:
    def __init__(self):
        self.message_history = []
        self.description = {}

    def refresh(self):
        self.get_description()
        self.message_history = [
            {
                "role": "system",
                "content": self.start_message(),
            }
        ]

    def default(self):
        self.message_history.append(
            {
                "role": "user",
                "content": "Please summarize this information accurately and descriptively in simple language with a couple sentences so that it is easy and quick for me to understand. This is not an art piece, this is just a picture from my camera, so please do not be creative or poetic, just describe my situation.",
            }
        )
        return self.chat()

    def start_message(self):
        string = (
            "I am a blind person. I have used a vision AI to come up with a description of what I am seeing. Here it is:\n"
            + self.description["description"]
            + "\n\n"
        )
        objects = ", ".join(
            [
                obj["name"]
                for obj in self.description["objects"]
                if obj["confidence"] > 0.7
            ]
        ).strip()
        if objects:
            string += (
                "I have also used an object detection AI to identify the objects in the image. Here they are:\n"
                + objects
                + "\n\n"
            )
        if self.description["ocr"]:
            string += (
                "I have also used an OCR AI to read any text in the image. Here it is:\n"
                + self.description["ocr"]
                + "\n\n"
            )

        return string.strip()

    def chat(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=self.message_history
        )
        return response.choices[0].message.content.strip()

    def describe(self):
        import time

        start = time.time()
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
        print(f"Astica API call took {time.time() - start} seconds")

        text = pytesseract.image_to_string("pic.jpg").strip()
        asticaAPI_result["ocr"] = text
        asticaAPI_result["description"] = asticaAPI_result.pop("caption_GPTS")

        self.description = deepcopy(asticaAPI_result)


ChatBot().describe()
