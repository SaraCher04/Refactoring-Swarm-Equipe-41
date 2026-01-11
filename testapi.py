import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the .env file
API_KEY = os.getenv("GOOGLE_API_KEY")

# Endpoint to list available models
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

headers = {
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    available_models = response.json()
    print(available_models)  # This will print the list of available models
else:
    print(f"❌ Error fetching models: {response.status_code} - {response.text}")
