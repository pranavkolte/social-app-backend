from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.responses import Response
from starlette import status

from app.database.models import Posts, Users
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