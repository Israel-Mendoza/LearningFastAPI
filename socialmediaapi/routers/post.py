from typing import Any
from fastapi import APIRouter, HTTPException
from socialmediaapi.models.post import UserPost, UserPostIn, Comment, CommentIn, UserPostWithComment
from socialmediaapi.database import comment_db, post_db, database

router = APIRouter()

# Creating our databases, one for the posts, and the other for the comments:
# post_db: dict[int, UserPost] = {}
# comment_db: dict[int, Comment] = {}


async def find_post_in_db(post_id: int) -> UserPost | None:
    """
    Finds a post in the database based on the post ID.
    :param post_id: The ID of the searched post.
    :return: The UserPost in question. None if it doesn't exits.
    """
    query = post_db.select().where(post_db.c.id == post_id)
    return await database.fetch_one(query)


@router.get("/", response_model=list[UserPost])
async def get_all_posts():
    """
    :return: The list of saved posts.
    """
    query = post_db.select()
    return await database.fetch_all(query)


@router.get("/post/{post_id}/comments", response_model=list[Comment])
async def get_post_comments(post_id: int):
    """
    :param post_id: The ID of the searched post.
    :return: The list of comments related to the searched post.
    """
    query = comment_db.select().where(comment_db.c.post_id == post_id)
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    """
    :param post_id: The ID of the searched posts.
    :return: The post in question including the comments related to it.
    """
    post_in_question: UserPost = await find_post_in_db(post_id)
    if post_in_question is None:
        raise HTTPException(status_code=404, detail=f"Post with ID '{post_id}' not found")
    return UserPostWithComment(post=post_in_question, comments=await get_post_comments(post_id))


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    """
    :param post: The post we want to add. Must comply with the UserPostIn schema.
    :return: The post as it will be stored in the database.
    """
    data: dict[str, Any] = post.model_dump()  # Serializes the post to a dictionary
    query = post_db.insert().values(data)
    last_record_id = await database.execute(query)
    return UserPost.model_validate({**data, "id": last_record_id})


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    """
    :param comment: The comment we want to attach. Must comply with the Comment schema.
    :return: The comment as it will be stored in the database.
    """
    post_to_comment: UserPost | None = await find_post_in_db(comment.post_id)

    if post_to_comment is None:
        raise HTTPException(status_code=404, detail=f"Post with ID '{comment.post_id}' not found")

    comment_dict: dict = comment.model_dump()  # Serializes the comment to a dictionary

    query = comment_db.insert().values(comment_dict)
    comment_id: int = await database.execute(query)
    return Comment.model_validate({**comment_dict, "id": comment_id})
