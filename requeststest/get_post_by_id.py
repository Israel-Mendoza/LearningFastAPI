import requests

post_id: int = 0
post_url: str = f"http://localhost:8000/post/{post_id}"


response: requests.models.Response = requests.get(post_url)

print(response.json())
