from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    # add group for /docs
    tags=['Users']
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # hash password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    user_dict = user.dict()
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    # token authentication return user obj
    curren_user: object = Depends(oauth2.get_current_user)
):

    user = db.query(models.User).filter(
        models.User.id == id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    else:

        return user
