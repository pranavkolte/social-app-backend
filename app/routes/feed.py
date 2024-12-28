from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from starlette import status

from app.database.models import Users, Posts, Follow
from app.services.auth import AuthService

router = APIRouter()

@router.get("/")
async def get_user_feed(
    current_user: Users = Depends(AuthService.get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    # 13.	Implement user feed, where a user can get a list of posts based on the users they follow,
    #          in a reverse chronological order (Latest post on top). This should be paginated.
    following = Follow.get_following(user_id=str(current_user.user_id))
    if not following:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"msg": "no follwing found"}
        )

    following_ids = [f.following_id for f in following]
    posts = Posts.get_posts_by_user_list(user_ids=following_ids, limit=limit, offset=offset)
    if not posts:
        return Response(
            content={"msg": "No posts found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    posts_data = [post.to_dict() for post in posts]
    return Response(
        content={"msg": "SUCCESS", "data": posts_data},
        status_code=status.HTTP_200_OK
    )
