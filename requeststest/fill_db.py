import asyncio
import httpx
from random import choice

"""Using two end-points to populate the API's database with 10 posts and 3 comments per post."""


post_url: str = "http://localhost:8000/post"
comment_url: str = "http://localhost:8000/comment"

posts: list[dict[str, str]] = [
    {
        "body": "This is one example"
    },
    {
        "body": "Esto es un ejemplo",
    },
    {
        "body": "Ceci est un exemple"
    },
    {
        "body": "Isto é um exemplo"
    }
]

comments: list[dict[str, str]] = [
    {
        "body": "This is a comment",
        "post_id": ""
    },
    {
        "body": "Esto es un comentario",
        "post_id": ""
    },
    {
        "body": "Ceci est un commentaire",
        "post_id": ""
    },
    {
        "body": "Isto é um comentário",
        "post_id": ""
    }
]


async def main() -> None:
    for i in range(1, 101):
        async with httpx.AsyncClient() as client:
            await client.post(post_url, json=choice(posts))
            for j in range(100):
                response = await client.post(comment_url, json={**choice(comments), "post_id": i})
                print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
