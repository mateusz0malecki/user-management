from fastapi import APIRouter, status, Depends
from typing import List
from data import schemas, models
from sqlalchemy.orm import Session
from data.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/', response_model=List[schemas.User], status_code=status.HTTP_200_OK)
async def users(
        db: Session = Depends(get_db)
):
    return models.User.get_all_users(db)
