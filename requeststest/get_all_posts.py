import requests

url: str = "http://localhost:8000"

response = requests.get(url)

if response.status_code:
    for item in response.json():
        print(item)
