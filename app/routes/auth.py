from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import Response

from app.database.models import Users
from app.schema import Token, CreateUserRequest
from app.services.auth import AuthService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 2.	User Login
    token = AuthService.login(
        username=form_data.username, password=form_data.password
    )
    if not token:
        return Token(access_token="", token_type="bearer", refresh_token="")
    return token



@router.post("/register")
async def register(request: CreateUserRequest):
    # 1.User Registration

    username: str = request.username
    username = username.lower()

    if Users.get_user(filter={"email": request.email,"username": username}, use_or=True,):
        return Response(
            content={
              "msg": "ALREADY_EXIST",
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = Users(
        email=request.email,
        username=username if request.username else request.email,
        password_hash=AuthService.get_password_hash(request.password),
        name=request.name,
    )

    user: Users = user.save()

    if user:
        return Response(
            content={
                "msg": "SUCCESS",
                "data": user.to_dict(),
            },
            status_code=status.HTTP_201_CREATED,
        )

    return Response(
        content={
            "msg": "FAILED",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

