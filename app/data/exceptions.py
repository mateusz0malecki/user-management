from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id '{user_id}' not found.")
