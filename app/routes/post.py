from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import Response
from starlette import status

from app.database.models import Posts, Users, Like
from app.schema import CreatePostRequest
from app.services.auth import AuthService

router = APIRouter()

@router.post("/", response_model=dict)
async def create_post(
    request: CreatePostRequest,
    user: Users = Depends(AuthService.get_current_user),
):
    # 3.	Create Posts
    body = request.model_dump()
    caption = body.get("caption", "")
    post_media_url = body.get("post_media_url", "")
    background_music_url = body.get("background_music_url", None)
    category = body.get("category", "")
    publisher_user_id = user.user_id

    post = Posts(
        caption=caption,
        post_media_url=post_media_url,
        background_music_url=background_music_url,
        category=category,
        publisher_user_id=publisher_user_id,
    ).save()

    if post:
        return Response(
            content={"msg": "SUCCESS", "data": post.to_dict()},
            status_code=status.HTTP_201_CREATED,
        )

    return Response(
        content={"msg": "FAILED"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@router.get("/user/{user_id}", response_model=dict)
async def get_user_posts(
        user_id: str,
        current_user: Users = Depends(AuthService.get_current_user)
):
    # 7.	Get contents posted by other users on the platform.
    posts = Posts.get_posts_by_user(user_id=user_id)
    if posts is None:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg":"No posts found for this user"}
        )

    posts_data = [post.to_dict() for post in posts]
    return Response(
        content={"msg": "SUCCESS", "data": posts_data},
        status_code=status.HTTP_200_OK
    )


@router.get("/{post_id}", response_model=dict)
async def get_post_details(
        post_id: str,
        current_user: Users = Depends(AuthService.get_current_user)
):
    post = Posts.get_post_by_id(post_id=post_id)
    if not post:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg":"Post not found"}
        )

    post_data = post.to_dict()

    return Response(
        content={"msg": "SUCCESS", "data": post_data},
        status_code=status.HTTP_200_OK
    )


@router.post("/like", response_model=dict)
async def like_post(
    post_id: str,
    current_user: Users = Depends(AuthService.get_current_user)
):
    # 9.	Like a post.
    post = Posts.get_post_by_id(post_id=post_id)
    if not post:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg":"Post not found"}
        )

    existing_like = Like.get_like_count(post_id=post_id, user_id=str(current_user.user_id))
    if existing_like > 0:
        # Unlike the post
        success = Like.delete(post_id=post_id, user_id=str(current_user.user_id))
        if success:
            return Response(
                content={"msg": "UNLIKED"},
                status_code=status.HTTP_200_OK
            )
        else:
            return Response(
                content={"msg": "FAILED"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    new_like = Like(
        user_id=str(current_user.user_id),
        post_id=post_id
    ).save()

    if new_like:
        return Response(
            content={"msg": "LIKED"},
            status_code=status.HTTP_201_CREATED
        )

    return Response(
        content={"msg": "FAILED"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

@router.get("/{post_id}/likes", response_model=dict)
async def get_post_likes(
    post_id: str,
    current_user: Users = Depends(AuthService.get_current_user)
):
    # Check if the post exists
    post: Posts = Posts.get_post_by_id(post_id=post_id)
    if not post:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg":"Post not found"}
        )


    likes: List[Like] = Like.get_likes_for_post(post_id=post_id)
    if not likes:
        return Response(
            content={"msg": "No likes found for this post"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    users_data = []
    for like in likes:
        user = Users.get_user({"user_id": like.user_id})
        if user:
            users_data.append(user.to_dict())

    return Response(
        content={"msg": "SUCCESS", "data": users_data},
        status_code=status.HTTP_200_OK
    )