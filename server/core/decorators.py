from fastapi import Request
from starlette import status
from core.exception import CustomException


def login_required(func):
    async def wrapper(request: Request):
        if not request.state.user:
            raise CustomException(status="Failed", status_code=status.HTTP_401_UNAUTHORIZED,
                                  message='Authentication credentials not provide.')
        return await func(request)
    return wrapper
