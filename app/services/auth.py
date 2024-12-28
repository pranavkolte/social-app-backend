import uuid
import jwt
from datetime import datetime, timedelta
from typing import Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext

from app.database.models import Users
from app.schema import Token
from app.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", scheme_name="JWT")


class AuthService:
    # Load settings from configuration
    SECRET_KEY = settings.SECRET_KEY
    REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
    ADMIN_SECRET_KEY = settings.ADMIN_SECRET_KEY
    ADMIN_REFRESH_SECRET_KEY = settings.ADMIN_REFRESH_SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


    @classmethod
    def verify_password(
        cls,
        plain_password: Union[str, None],
        hashed_password: Union[str, None] = None,
    ):
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str):
        return pwd_context.hash(password)

    @classmethod
    def verify_token(cls, token: str, secret_key: str = None):
        """Verify the provided token."""
        payload = jwt.decode(token, secret_key, algorithms=[cls.ALGORITHM])
        if datetime.fromtimestamp(payload.get("exp")) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
            )
        if not payload.get("sub"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return payload

    @classmethod
    def create_access_token(
        cls,
        data: dict,
        expires_delta: timedelta = None,
        secret_key: str = None,
    ) -> Token:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, secret_key, algorithm=cls.ALGORITHM
        )
        return encoded_jwt


    @classmethod
    def login(cls, username: str, password: str):
        if not username or not password:
            raise HTTPException(
                status_code=400, detail="Invalid username or password"
            )

        user: Users = Users.get_user({"email": username}, use_or=True)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect email")

        if not cls.verify_password(password, user.password_hash):
            raise HTTPException(status_code=400, detail="Incorrect password")

        return Token(
            access_token=cls.create_access_token(
                data={
                    "sub": user.email,
                    "user_id": str(user.user_id),
                    "user_type": user.user_type,
                    "username": user.username,
                },
                secret_key=cls.SECRET_KEY,
            ),
            token_type="bearer"
        )

    @classmethod
    def get_current_user(
            cls, token:
            str = Depends(oauth2_scheme)
    ) -> Users:
        payload = cls.verify_token(token=token, secret_key=cls.SECRET_KEY)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        user = Users.get_user({"user_id": uuid.UUID(user_id)}, use_or=False)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user
