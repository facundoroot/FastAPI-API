from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from .. import models, database, utils, oauth2


router = APIRouter(tags=["Authentication"])


# for this route because of OAuth2PasswordRequestForm
# we dont send the data of the request in the body
# but in form-data
@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):

    user = (
        db.query(models.User)
        # in OAuth2PasswordRequestForm email variable of the dict is called
        # username
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )
    else:

        # verify password
        verified_password = utils.verify_password(
            user_credentials.password, user.password
        )

        if not verified_password:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid credentials",
            )
        else:

            # create token
            access_token = oauth2.create_access_token(
                {
                    "user_id": user.id
                }
            )

            response = {
                "access_token": access_token,
                "token_type": "bearer"
            }

            return response
