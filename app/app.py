from  fastapi import FastAPI

app = FastAPI(
    title="social app Backend",
    contact={
        "name": "Pranav Kolte",
        "email": "dnavaria15@gmail.com"
    },
    docs_url="/docs",
)

""""
POST : POST user/signup 
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