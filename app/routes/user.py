from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.openapi.models import Response
from starlette import status
from app.database.models import Users, Follow, Posts
from app.services.auth import AuthService

router = APIRouter()

@router.get("/{user_id}")
async def get_user(
        user_id: str,
        current_user: Users = Depends(AuthService.get_current_user)
):
    user: Users = Users.get_user({"user_id": user_id})
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(
        content=user.to_dict(),
        status_code=status.HTTP_200_OK
    )

@router.post("/{user_id}/follow")
async def follow_user(
        user_id: str,
        current_user: Users = Depends(AuthService.get_current_user)
):
    # 5.	Follow other users.
    if user_id == str(current_user.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself"
        )

    result = Follow.follow_user(
        follower_id=str(current_user.user_id),
        following_id=user_id
    )

    if result is True:
        return Response(
            content={"msg": "UNFOLLOWED"},
            status_code=status.HTTP_200_OK
        )
    elif result:
        return Response(
            content={"msg": "FOLLOWED"},
            status_code=status.HTTP_201_CREATED
        )
    else:
        return Response(
            content={"msg": "FAILED"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@router.get("/me")
async def get_my_profile(current_user: Users = Depends(AuthService.get_current_user)):
    # 6.	Get contents posted by the logged in user.
    posts = Posts.get_posts_by_user(user_id=str(current_user.user_id))
    if posts is None:
        return Response(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Failed to retrieve posts"
        )

    posts_data = [post.to_dict() for post in posts]
    return Response(
        content={
            "msg": "SUCCESS",
            "data": posts_data
        },
        status_code=status.HTTP_200_OK
    )

@router.get("/search/{search_string}", response_model=dict)
async def search_users(
    search_string: str,
    current_user: Users = Depends(AuthService.get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    # -	Search for a user with user handle (username). Even better if substring search is supported
    users = Users.search_by_name_or_username(search_string=search_string, limit=limit, offset=offset)
    if not users:
        return Response(
            content={"msg": "No users found"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    users_data = [user.to_dict() for user in users]
    return Response(
        content={"msg": "SUCCESS", "data": users_data},
        status_code=status.HTTP_200_OK
    )