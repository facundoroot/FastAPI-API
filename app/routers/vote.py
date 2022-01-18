from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    # add group for /docs
    tags=['Votes']
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED
    )
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    # token authentication return user id
    curren_user: object = Depends(oauth2.get_current_user)
):
    """Vote or unvote post"""

    post_to_vote = db.query(models.Post).filter(
        models.Post.id == vote.post_id
    ).first()

    if not post_to_vote:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {vote.post_id} was not found",
        )

    # query if user already voted this post
    vote_query = db.query(models.Vote).filter(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == curren_user.id
        )

    found_vote = vote_query.first()

    if vote.vote_dir == 1:

        if found_vote:

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Current user already liked this post",
            )

        new_vote = models.Vote(post_id=vote.post_id, user_id=curren_user.id)

        db.add(new_vote)
        db.commit()

        return {'message': f'post: {vote.post_id} liked!'}
    else:

        if not found_vote:

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Current user didn't like post before",
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': f'post: {vote.post_id} unliked!'}
