from fastapi import Request
from starlette import status

from core.dependencis import get_current_user
from .exception import CustomException


async def user_middleware(request: Request, call_next):
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    request.state.user = None
    if token:
        # user = await get_current_user(token)
        # request.state.user = user
        try:
            user = await get_current_user(token)
            request.state.user = user

        except CustomException as e:
            raise e

        except Exception as e:
            # import pdb;pdb.set_trace()
            raise CustomException(status="Failed", status_code=status.HTTP_401_UNAUTHORIZED,
                                  message='Internal Server Error', error=e)
    return await call_next(request)

# @lru_cache(maxsize=128)
# async def get_cached_user(token: str):
#     return await get_current_user(token)
#
# async def user_middleware(request: Request, call_next):
#     token = request.headers.get('Authorization', '').replace('Bearer ', '')
#     if token:
#         try:
#             user = await get_cached_user(token)
#             request.state.user = user
#         except Exception as e:
#             # Log the error
#             print(f"Error fetching user: {e}")
#             # Return a 401 response
#             return JSONResponse(status_code=401, content={"detail": "Invalid authentication token"})
#     else:
#         request.state.user = None
#
#     response = await call_next(request)
#     return response
