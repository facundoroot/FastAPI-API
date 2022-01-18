from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


# validates that there are sent
# only title and content to our endpoint and their data type
# tries to convert the body to that data type and if it cant also sends
# an error, if there are keys missing also sends an error
class PostBase(BaseModel):
    title: str
    content: str
    # optional
    published: bool = True
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserLogin(UserBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    vote_dir: int


# RESPONSE

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# we can also use validation for the data response, specify the values will
# send in the response (remember it also inherits the values) from POstBase
# and check their data type
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    post_owner: UserResponse

    # this permits to be able to check any type of response, not only dict
    # in this case an orm object
    class Config:
        orm_mode = True


class PostResponseJoin(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True
