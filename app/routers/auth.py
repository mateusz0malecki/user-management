from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from data import schemas
from data.database import get_db
from data.jwt_helper import authenticate_user, create_token, ACCESS_TOKEN_EXPIRE_MINUTES
from data.exceptions import CredentialsException

from datetime import timedelta


router = APIRouter(tags=["Auth"])


@router.post('/login', response_model=schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise CredentialsException
    access_token = create_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token}
