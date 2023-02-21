import requests
import json

import os
import openai

openai.organization = "org-G5vsVn2ZVS1EkIbhVJXbAJtu"
openai.api_key = os.getenv("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")
openai.Model.list()


# The text prompt to generate art from
prompt = "A beautiful sunset over a calm ocean"

# The API endpoint
endpoint = "https://api.openai.com/v1/images/generations"

openai.api_key = <API-KEY>

# The data for the API request
data = {
    "model": "image-dall-e-002",
    "prompt": prompt
}

# Make the API request
response = requests.post(endpoint, headers=headers, json=data)

# Get the JSON response
response_json = response.json()

# Print the URL of the generated image
print(response_json)
