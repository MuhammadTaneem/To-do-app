# import secrets
# from datetime import datetime, timedelta
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from passlib.context import CryptContext
# from modules.users import schema
# from core.db import create_session
# from modules.users.models import User, UserReset
#
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 9999999
# RESET_TOKEN_EXPIRE_MINUTES = 2
#
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def get_hash_password(password):
#     return pwd_context.hash(password)
#
#
# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Session expired",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#     except JWTError as e:
#         raise credentials_exception
#
#     try:
#         session = create_session()
#         user = session.query(User).filter(User.email == email).first()
#         session.close()
#     except Exception as e:
#
#         credentials_exception.detail = 'Internal server error'
#         raise credentials_exception
#
#     if user is None:
#         credentials_exception.detail = 'User not found'
#         raise credentials_exception
#     return schema.ReadUser(**user.__dict__)
#
#
# def create_reset_token(user_id):
#     try:
#         reset_token = secrets.token_hex(16)
#         expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
#
#         # data = UserReset({
#         #     'author': user_id,
#         #     'expire': expire,
#         #     'reset_token': reset_token
#         # })
#         data = UserReset(author=user_id, expire=expire, reset_token=reset_token)
#         session = create_session()
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         session.close()
#         return reset_token
#     except Exception as e:
#         return {'status': status.HTTP_500_INTERNAL_SERVER_ERROR, 'message': 'Internal server error ',
#                 'error_dict': e}
#
#
