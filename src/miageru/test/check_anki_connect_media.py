import requests
import json
import base64

anki_connect_url = "http://127.0.0.1:8765"

def invoke(action, **params):
    requestJson = json.dumps({'action': action, 'params': params, 'version': 6})
    response = requests.post(anki_connect_url, data=requestJson)
    return json.loads(response.text)

# 1. Store the media file in Anki's media folder
# (Replace with your actual file path)
audio_file_path = "path/to/your_audio_file.mp3"
image_file_path = "path/to/your_image_file.jpg"

# Read audio file as base64
with open(audio_file_path, "rb") as f:
    audio_data = base64.b64encode(f.read()).decode("utf-8")
audio_filename = "my_awesome_word.mp3" # Name it will have in Anki's media folder

# Read image file as base64
with open(image_file_path, "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")
image_filename = "illustrative_image.jpg" # Name it will have in Anki's media folder

# Store audio
store_audio_result = invoke('storeMediaFile', filename=audio_filename, data=audio_data)
if store_audio_result.get('error'):
    print(f"Error storing audio: {store_audio_result['error']}")
else:
    print(f"Audio file '{audio_filename}' stored successfully.")

# Store image
store_image_result = invoke('storeMediaFile', filename=image_filename, data=image_data)
if store_image_result.get('error'):
    print(f"Error storing image: {store_image_result['error']}")
else:
    print(f"Image file '{image_filename}' stored successfully.")


# 2. Add the note with the correct media tags in the fields
note = {
    "deckName": "My Japanese Language Deck",
    "modelName": "My Japanese Language Note", # The Note Type you defined earlier
    "fields": {
        "Japanese": "猫",
        "English": "Cat",
        "Reading": "ねこ",
        "Audio": f"[sound:{audio_filename}]",  # <--- Critical: Use the Anki sound tag
        "Image": f"<img src=\"{image_filename}\">" # <--- Critical: Use the HTML img tag
    },
    "tags": ["vocabulary", "N5", "animals"]
}

add_note_result = invoke('addNote', note=note)

if add_note_result.get('error'):
    print(f"Error adding note: {add_note_result['error']}")
else:
    print(f"Note added successfully. Note ID: {add_note_result['result']}")


