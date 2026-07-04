import requests
import json

anki_connect_url = "http://127.0.0.1:8765"

def invoke(action, **params):
    requestJson = json.dumps({'action': action, 'params': params, 'version': 6})
    response = requests.post(anki_connect_url, data=requestJson)
    return json.loads(response.text)

# Define your new Note Type structure
new_note_type_definition = {
    "modelName": "My Japanese Language Note",
    "inOrderFields": ["Japanese", "English", "Reading", "Example Sentence", "Audio"],
    "css": """
        .card {
            font-family: Arial;
            font-size: 20px;
            text-align: center;
            color: black;
            background-color: white;
        }
        .jp {
            font-size: 28px;
            color: darkblue;
        }
        .ex-sentence {
            font-style: italic;
            color: gray;
        }
    """,
    "cardTemplates": [
        {
            "Name": "Japanese to English",
            "Front": "<div class='jp'>{{Japanese}}</div>",
            "Back": "{{FrontSide}}<hr id='answer'><br>{{English}}<br><span class='ex-sentence'>{{Example Sentence}}</span><br>{{Audio}}"
        },
        {
            "Name": "English to Japanese",
            "Front": "{{English}}",
            "Back": "{{FrontSide}}<hr id='answer'><br><div class='jp'>{{Japanese}}</div><br>{{Reading}}<br>{{Audio}}"
        }
    ]
}

# Create the model (Note Type)
result = invoke('createModel', model=new_note_type_definition)

if result.get('error'):
    print(f"Error creating model: {result['error']}")
else:
    print(f"Model '{new_note_type_definition['modelName']}' created successfully. Model ID: {result['result']}")


# storeMediaFile action to save media    
