from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.database import db
from app.settings import settings


def handle_startup():
    db.create_engine(POSTGRES_URI=settings.POSTGRES_URI)
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

""""

Login : POST user/login
GET USER : GET /user/{user_id}
follow : POST /user/{user_id}/follow     follow unfollow user 

Create POST : POST post/
GET specific post : GET /post/{post_id}
Like POST : POST /post/like
get like: GET /post/like 
comment on post : POST /post/{post_id}/comment
GET comments : GET /comment/{comment_id}

GET FEED : GET /feed: (pagination,the users they follow,Latest post on top) 


Optional ------------------------
search user : GET /search  --- required 
"""

@app.get("/", tags=["Health Check"])
def index():
    return {"message": f"social app backend  is running"}


app.include_router(
    prefix="/api/v1/auth", router=auth_router, tags=["Authentication"]
)

app.include_router(
    prefix="/api/v1/user", router=user_router, tags=["User"]
)