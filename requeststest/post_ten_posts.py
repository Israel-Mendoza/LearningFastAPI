import requests
from random import choice

post_url: str = "http://localhost:8000/post"

posts: list[dict[str, str]] = [
    {
        "body": "This is one example"
    },
    {
        "body": "Esto es un ejemplo",
    },
    {
        "body": "Ceci est un exemple"
    }
]

for i in range(10):
    new_post: dict[str, str] = choice(posts)
    last = requests.post(
        post_url,
        json=new_post
    )



