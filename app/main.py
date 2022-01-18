from fastapi import FastAPI
# SQLAlchemy
from . import models
from .database import engine
# Router
from .routers import post, user, auth, vote
# Config
from .config import settings

# CORS
from fastapi.middleware.cors import CORSMiddleware

print(settings.secret_key)

# create all models
# when we use alembic it is not needed, but doesent harm
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# for CORS
# middleware is a function that runs before every request
# origins is a list of domain wich we let send request to our API
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    # allow specific methods
    allow_methods=["*"],
    # allow specific headers
    allow_headers=["*"],
)

# add paths from routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root() -> dict:

    return {"message": "Welcome to my API"}
