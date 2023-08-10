import requests
import json
import base64
import os
from dotenv import load_dotenv
load_dotenv()

class ChatBot:
    def __init__(self):
        self.message_history = []
    
    def start_message(self, response):
        return "I am a blind person, blah blah blah, here is description: " + response['caption_GPTS']
    
    def chat(self, prompt):
        return
    
    def describe(self):
        asticaAPI_key = os.getenv("ASTICA_KEY")
        asticaAPI_timeout = 60

        asticaAPI_endpoint = 'https://astica.ai:9141/vision/describe'
        asticaAPI_modelVersion = '2.1_full'

        path_to_local_file = 'pic.jpg';
        with open(path_to_local_file, 'rb') as file:
            image_data = file.read()
        image_extension = os.path.splitext(path_to_local_file)[1]
        asticaAPI_input = f"data:image/{image_extension[1:]};base64,{base64.b64encode(image_data).decode('utf-8')}"

        asticaAPI_visionParams = "description, objects, describe_all, text_read, gpt"

        asticaAPI_payload = {
            'tkn': asticaAPI_key,
            'modelVersion': asticaAPI_modelVersion,
            'visionParams': asticaAPI_visionParams,
            'input': asticaAPI_input,
        }

        response = requests.post(asticaAPI_endpoint, data=asticaAPI_payload, timeout=asticaAPI_timeout, verify=False)
        if response.status_code == 200:
            asticaAPI_result = response.json()
        else:
            asticaAPI_result = {'status': 'error', 'error': 'Failed to connect to the API.'}
        