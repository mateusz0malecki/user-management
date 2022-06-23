import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from data import schemas
from data.database import get_db
from data.models import User
from data.hash import Hash
from data.exceptions import CredentialsException

from datetime import timedelta, datetime


router = APIRouter(tags=["Auth"])

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_scheme = OAuth2PasswordBearer(tokenUrl='login')


def authenticate_user(
        username: str,
        password: str,
        db: Session = Depends(get_db)
):
    user = User.get_user_by_username(db, username).first()
    if not user:
        return False
    if not Hash.verify_password(password, user.password):
        return False
    return user


def create_token(data: dict, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
        token: str = Depends(auth_scheme),
        db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise CredentialsException
    user = User.get_user_by_username(db, username=token_data.username).first()
    if user is None:
        raise CredentialsException
    return user


def check_if_active_user(current_user: schemas.UserCheck = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated (inactive user)."
        )
    return current_user


def check_if_superuser(current_user: schemas.UserCheck = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated as admin."
        )
    return current_user
