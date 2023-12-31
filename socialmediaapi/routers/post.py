from typing import Any
from fastapi import APIRouter, HTTPException
from socialmediaapi.models.post import UserPost, UserPostIn, Comment, CommentIn, UserPostWithComment

router = APIRouter()

# Creating our databases, one for the posts, and the other for the comments:
post_db: dict[int, UserPost] = {}
comment_db: dict[int, Comment] = {}


def find_post_in_db(post_id: int) -> UserPost | None:
    """
    Finds a post in the database based on the post ID.
    :param post_id: The ID of the searched post.
    :return: The UserPost in question. None if it doesn't exits.
    """
    return post_db.get(post_id, None)


@router.get("/", response_model=list[UserPost])
async def get_all_posts():
    """
    :return: The list of saved posts.
    """
    return list(post_db.values())


@router.get("/post/{post_id}/comments", response_model=list[Comment])
async def get_post_comments(post_id: int):
    """
    :param post_id: The ID of the searched post.
    :return: The list of comments related to the searched post.
    """
    post_in_question: UserPost | None = find_post_in_db(post_id)
    if post_in_question is None:
        raise HTTPException(status_code=404, detail=f"Post with ID '{post_id}' not found")

    return [comment for comment in comment_db.values() if comment.post_id == post_id]


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: int):
    """
    :param post_id: The ID of the searched posts.
    :return: The post in question including the comments related to it.
    """
    post_in_question: UserPost = find_post_in_db(post_id)
    if post_in_question is None:
        raise HTTPException(status_code=404, detail=f"Post with ID '{post_id}' not found")
    return UserPostWithComment(post=post_in_question, comments=await get_post_comments(post_id))


@router.post("/post", response_model=UserPost, status_code=201)
async def create_post(post: UserPostIn):
    """
    :param post: The post we want to add. Must comply with the UserPostIn schema.
    :return: The post as it will be stored in the database.
    """
    data: dict[str, Any] = post.model_dump()  # Serializes the model to a dictionary
    last_record_id: int = len(post_db)
    new_post: UserPost = UserPost.model_validate({**data, "id": last_record_id})
    post_db[last_record_id] = new_post
    return new_post


@router.post("/comment", response_model=Comment, status_code=201)
async def create_comment(comment: CommentIn):
    """
    :param comment: The comment we want to attach. Must comply with the Comment schema.
    :return: The comment as it will be stored in the database.
    """
    post_to_comment: UserPost | None = find_post_in_db(comment.post_id)
    if post_to_comment is None:
        raise HTTPException(status_code=404, detail=f"Post with ID '{comment.post_id}' not found")
    comment_dict: dict = comment.model_dump()
    comment_id: int = len(comment_db)
    comment = Comment.model_validate({**comment_dict, "id": comment_id})
    comment_db[comment_id] = comment
    return comment
