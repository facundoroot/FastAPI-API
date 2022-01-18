from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    # add group for /docs
    tags=['Posts']
)


# in this case because we send a list of posts we need a list
# of PostResponse schema, because if we
# only put response_model=schemas.PostResponse
# it will try to force a list of posts into one to validate it
@router.get("/", response_model=List[schemas.PostResponseJoin])
def get_posts(
    db: Session = Depends(get_db),
    # token authentication return user id
    curren_user: object = Depends(oauth2.get_current_user),
    # parameter sent to URL ?limit=
    limit: int = 10,
    # skip amount n of posts
    skip: int = 0,
    # search by title
    search: Optional[str] = ""
):

    all_posts_with_n_votes_query = db.query(
        # values from Post and value called votes
        # with n of votes in post
        models.Post, func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(
        models.Post.id
    )

    queried_posts_with_url_params = all_posts_with_n_votes_query.filter(
        models.Post.title.contains(search)
    ).limit(
        limit
    ).offset(
        skip
    ).all()
    return queried_posts_with_url_params


@router.get(
    "/{id}",
    response_model=schemas.PostResponseJoin
)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    # token authentication return user id
    curren_user: object = Depends(oauth2.get_current_user)
):

    all_posts_with_n_votes_query = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(
        models.Post.id
    )

    post = all_posts_with_n_votes_query.filter(
        models.Post.id == id
    ).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return post


# when is ok created it will send a 201 code
# lets add the schema for the response
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse
)
# lets add the schema for the data that is sent to us to
# check it with PostCreate
# also Depends(oauth2.oauth2.get_current_user)
# to verify the token
# (to verify the token will verify if the user is logged correctly also)
# and get id the token owner
# the token will be send in the header of the request
# Authorization : Bearer <token>
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    curren_user: object = Depends(oauth2.get_current_user)
) -> object:

    post_dict = post.dict()
    post_dict['user_id'] = curren_user.id
    # ** to unpack automaticly all the fields like title=..., content=...
    new_post = models.Post(**post_dict)
    # otra forma: models.Post(user_id=curreint_user.id, **post_dict)
    db.add(new_post)
    db.commit()
    # refresh to get the default values of the post after creation
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    curren_user: object = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    # current user can only delete their own posts
    if post.user_id != curren_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/{id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse
)
def update_post(
    id: int,
    update_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    curren_user: object = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(
        models.Post.id == id
    )

    post = post_query.first()

    if post is None:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    # current user can only upgrade their own posts
    if post.user_id != curren_user.id:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.update(
        update_post.dict(),
        synchronize_session=False
    )
    db.commit()

    return post_query.first()
