import requests
import json

url = "http://127.0.0.1:5000/generate_diet/"
data = {
    "food": "Vegetarian",
    "calories": 2000,
    "allergy": "None"
}

response = requests.post(url, json=data)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")