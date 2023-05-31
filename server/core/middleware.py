from fastapi import Request
from starlette import status

from core.dependencis import get_current_user
from .exception import CustomException


async def user_middleware(request: Request, call_next):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    request.state.user = None
    if token:
        try:
            user = await get_current_user(token)
            request.state.user = user

        except CustomException as e:
            raise e
        except Exception as e:
            raise CustomException(status="Failed", status_code=status.HTTP_401_UNAUTHORIZED,
                                  message='Internal Server Error', error=e)
    return await call_next(request)