import os
from dotenv import load_dotenv

load_dotenv(".env")


class Settings:
    DB_URI: str = "mysql+mysqldb://user_name:user_password@localhost:3306/social_app"
    SERVICE_API_HOST: str = os.getenv("SERVICE_API_HOST", "localhost")
    SERVICE_API_PORT: int = int(os.getenv("SERVICE_API_PORT", "8000"))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SECRET_KEY")
    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY", "REFRESH_SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080"))

settings = Settings()
