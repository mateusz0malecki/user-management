from fastapi import APIRouter, status, Depends, Response

from typing import Any

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from data import schemas, models
from data.database import get_db
from data.exceptions import UserNotFound

router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/', status_code=status.HTTP_200_OK)
async def read_all_users(
        db: Session = Depends(get_db),
        page: int = 1,
        page_size: int = 10
):
    users = models.User.get_all_users(db)
    first = (page - 1) * page_size
    last = first + page_size
    response = schemas.UserPagination(users, first, last, page, page_size)
    return response


@router.get('/{user_id}', response_model=schemas.User, status_code=status.HTTP_200_OK)
async def read_user(
        user_id: str,
        db: Session = Depends(get_db)
):
    user = models.User.get_user_by_id(db, user_id).first()
    if not user:
        raise UserNotFound(user_id)
    return user


@router.post('/', response_model=schemas.User | Any, status_code=status.HTTP_201_CREATED)
async def create_user(
        request: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    created_user = models.User(**request.dict())
    try:
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
        return created_user
    except IntegrityError as e:
        return {
            "message": "Username is already used, try again.",
            "error": e
        }


@router.put('/{user_id}', status_code=status.HTTP_202_ACCEPTED)
async def edit_user(
        user_id: str,
        request: schemas.UserEdit,
        db: Session = Depends(get_db)
):
    user_to_edit = models.User.get_user_by_id(db, user_id)
    if not user_to_edit.first():
        raise UserNotFound(user_id)
    user_to_edit.update(request.dict())
    db.commit()
    return {
        "message": f"User with id '{user_id}' edited."
    }


@router.delete('/{user_id}')
async def delete_user(
        user_id: str,
        db: Session = Depends(get_db)
):
    user_to_delete = models.User.get_user_by_id(db, user_id)
    if not user_to_delete.first():
        raise UserNotFound(user_id)
    user_to_delete.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
