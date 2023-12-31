from dotenv import load_dotenv
load_dotenv()
import requests
import json
import base64
import os

def asticaAPI(endpoint, payload, timeout):
    response = requests.post(endpoint, data=payload, timeout=timeout, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'error': 'Failed to connect to the API.'}

asticaAPI_key = os.getenv("ASTICA_KEY") # visit https://astica.ai/api-keys/
asticaAPI_timeout = 60 # seconds  Using "gpt" or "gpt_detailed" will increase response time.

asticaAPI_endpoint = 'https://astica.ai:9141/vision/describe'
asticaAPI_modelVersion = '2.1_full' # '1.0_full' or '2.0_full'

#Input Method 1: https URL of a jpg/png image (faster)
asticaAPI_input = 'https://astica.ai/example/asticaVision_sample.jpg' 

'''
#Input Method 2: base64 encoded string of a local image (slower)
path_to_local_file = 'image.jpg';
with open(path_to_local_file, 'rb') as file:
    image_data = file.read()
image_extension = os.path.splitext(path_to_local_file)[1]
#For now, let's make sure to prepend appropriately with: "data:image/extension_here;base64" 
asticaAPI_input = f"data:image/{image_extension[1:]};base64,{base64.b64encode(image_data).decode('utf-8')}"
'''


asticaAPI_visionParams = 'description, objects, describe_all, text_read, gpt'
'''
    '1.0_full' supported options:
        description
        objects
        categories
        moderate
        tags
        brands
        color
        faces
        celebrities
        landmarks
        gpt new (Slow - be patient)
        gpt_detailed new (Much Slower)

    '2.0_full' supported options:
        description
        objects
        tags
        describe_all new
        text_read new
        gpt new (Slow - be patient)
        gpt_detailed new (Much Slower)
        
    '2.1_full' supported options:
        Supports all options
'''

# Define payload dictionary
asticaAPI_payload = {
    'tkn': asticaAPI_key,
    'modelVersion': asticaAPI_modelVersion,
    'visionParams': asticaAPI_visionParams,
    'input': asticaAPI_input,
}

# Call API function and store result
asticaAPI_result = asticaAPI(asticaAPI_endpoint, asticaAPI_payload, asticaAPI_timeout)

print('\nastica API Output:')
print(json.dumps(asticaAPI_result, indent=4))
print('=================')
print('=================')
with open("get.json", "w") as outfile:
    json.dump(asticaAPI_result, outfile)

# # Handle asticaAPI response
# if 'status' in asticaAPI_result:
#     # Output Error if exists
#     if asticaAPI_result['status'] == 'error':
#         print('Output:\n', asticaAPI_result['error'])
#     # Output Success if exists
#     if asticaAPI_result['status'] == 'success':
#         if 'caption_GPTS' in asticaAPI_result and asticaAPI_result['caption_GPTS'] != '':
#             print('=================')
#             print('GPT Caption:', asticaAPI_result['caption_GPTS'])
#         if 'caption' in asticaAPI_result and asticaAPI_result['caption']['text'] != '':
#             print('=================')
#             print('Caption:', asticaAPI_result['caption']['text'])
#         if 'CaptionDetailed' in asticaAPI_result and asticaAPI_result['CaptionDetailed']['text'] != '':
#             print('=================')
#             print('CaptionDetailed:', asticaAPI_result['CaptionDetailed']['text'])
#         if 'objects' in asticaAPI_result:
#             print('=================')
#             print('Objects:', asticaAPI_result['objects'])
# else:
#     print('Invalid response')