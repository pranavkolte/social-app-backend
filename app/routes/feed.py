from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status
from starlette.responses import Response

from app.database.models import Users
from app.schema import Token, CreateUserRequest
from app.services.auth import AuthService

router = APIRouter()
