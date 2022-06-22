import os

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from jose import JWTError, jwt

from data import schemas
from data.database import get_db
from data.models import User
from data.hash import Hash
from data.exceptions import CredentialsException
from data.jwt_handler import OAuth2Password, UserLoginRequestForm

from datetime import timedelta, datetime


router = APIRouter(tags=["Auth"])

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = 30

auth_scheme = OAuth2Password(tokenUrl='login')


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


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
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
    user = User.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise CredentialsException
    return user


@router.post('/login', response_model=schemas.Token)
async def login_for_access_token(
        form_data: UserLoginRequestForm = Depends(),
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
