from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from starlette import status
from app.database.models import Users, Follow
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
