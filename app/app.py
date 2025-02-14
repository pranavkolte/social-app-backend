from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.post import router as post_router
from app.routes.feed import router as feed_router
from app.database import db
from app.settings import settings


def handle_startup():
    db.create_engine()
    db.create_session()

def handle_shutdown():
    db.close_session()


app = FastAPI(
    title="social app Backend",
    contact={
        "name": "Pranav Kolte",
        "email": "dnavaria15@gmail.com"
    },
    docs_url="/docs",
    on_startup=[handle_startup],
    on_shutdown=[handle_shutdown],
)

@app.get("/", tags=["Health Check"])
async def index():
    return {"message": f"social app backend  is running"}


app.include_router(
    prefix="/api/v1/auth", router=auth_router, tags=["Authentication"]
)

app.include_router(
    prefix="/api/v1/user", router=user_router, tags=["User"]
)

app.include_router(
    prefix="/api/v1/post", router=post_router, tags=["Posts"]
)

app.include_router(
    prefix="/api/v1/feed", router=feed_router, tags=["Posts"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
    