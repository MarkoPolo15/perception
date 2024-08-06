import json

def load_credentials():
    with open('.venv/resources/credentials.json') as f:
        return json.load(f)



