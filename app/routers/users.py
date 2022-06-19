from fastapi import APIRouter, status, Depends, HTTPException, Response

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from data import schemas, models
from data.database import get_db
from data.hash import Hash


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

    response = {
        "page_number": page,
        "page_size": page_size,
        "total_record_count": len(users),
        "pagination": {},
        "records": users[first:last],
    }

    if last >= len(users):
        response["pagination"]["next"] = None
        if page > 1:
            response["pagination"]["previous"] = f"/users?page={page - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None
    else:
        response["pagination"]["next"] = f"/users?page={page + 1}&page_size={page_size}"
        if page > 1:
            response["pagination"]["previous"] = f"/users?page={page - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

    return response


@router.get('/{username}', response_model=schemas.User, status_code=status.HTTP_200_OK)
async def read_user(
        username: str,
        db: Session = Depends(get_db)
):
    user = models.User.get_user_by_username(db, username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found."
        )
    return user


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
        request: schemas.UserCreate,
        db: Session = Depends(get_db)
):
    created_user = models.User(
        username=request.username,
        password=Hash.get_password_hash(request.password)
    )
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


@router.put('/{username}', status_code=status.HTTP_202_ACCEPTED)
async def edit_user(
        username: str,
        request: schemas.UserEdit,
        db: Session = Depends(get_db)
):
    user_to_edit = models.User.get_user_by_username(db, username)
    if not user_to_edit.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found."
        )
    message = None
    if request.password == '':
        message = "Password cannot be empty."
    if not message:
        user_to_edit.update(
            {
                "password": Hash.get_password_hash(request.password)
            }
        )
        message = f"User '{username}' edited."
        return {"message": message}
    return Response(
        content={"message": message},
        status_code=status.HTTP_400_BAD_REQUEST
    )


@router.delete('/{username}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        username: str,
        db: Session = Depends(get_db)
):
    user_to_delete = models.User.get_user_by_username(db, username)
    if not user_to_delete.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username '{username}' not found."
        )
    user_to_delete.delete()
    db.commit()
    return Response()
