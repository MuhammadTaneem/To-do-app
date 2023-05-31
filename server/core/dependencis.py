import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.db import SessionManager
from core.exception import CustomException
from modules.users.models import User, UserToken
from core.enum import TokenType


def send_email(email, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "Drafty.com"
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('famouswebdeveloper@gmail.com', 'uwemmsaacdgmklpe')
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())

    print(f'Email sent to {email}')


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RESET_TOKEN_EXPIRE_MINUTES = 60
ACTIVE_TOKEN_EXPIRE_MINUTES = 90

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message='Internal server error',
                              error=e)


def generate_token(email: str, token_type: TokenType):
    try:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        if token_type == TokenType.reset.value:
            expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)

        elif token_type == TokenType.active.value:
            expire = datetime.utcnow() + timedelta(minutes=ACTIVE_TOKEN_EXPIRE_MINUTES)

        to_encode = {"sub": email, "exp": expire, "type": token_type}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message='Internal server error',
                              error=e)


def verify_reset_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get('type') == TokenType.reset.value:

            email: str = payload.get("sub")
            if email is None:
                raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      status='Failed', message='Incorrect Token.', error=None)
        else:

            raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  status='Failed', message='Incorrect Reset Token.', error=None)
    except JWTError as e:
        message = str(e)
        if "Signature" in message:
            message = message.replace("Signature", "Token")

        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message=f'Invalid Token: {message}.', error=None)

    try:
        session = SessionManager.create_session()
        db_token = session.query(UserToken).filter(UserToken.token == token) \
            .order_by(UserToken.id.desc()).first()
        session.close()

        if db_token is None:
            raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                                  message='Token Not Found',
                                  error=None)

    except Exception as e:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message='Internal server error',
                              error=e)

    if db_token.used:
        raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE, status='Failed',
                              message='This Token is Used.', error=None)
    if db_token.user is None:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed', message='User not found',
                              error=None)
    return db_token


def verify_active_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get('type') == TokenType.active.value:

            email: str = payload.get("sub")
            if email is None:
                raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      status='Failed', message='Incorrect Token.', error=None)
        else:

            raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  status='Failed', message='Incorrect Active Token.', error=None)
    except JWTError as e:
        message = str(e)
        if "Signature" in message:
            message = message.replace("Signature", "Token")

        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                              status='Failed',
                              message=f'Invalid Token: {message}.',
                              error=None)

    try:
        session = SessionManager.create_session()

        db_token = session.query(UserToken).filter(UserToken.token == token) \
            .order_by(UserToken.id.desc()).first()
        session.close()

        if db_token is None:
            raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                                  message='Token Not Found',
                                  error=None)

    except Exception as e:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message='Internal server error',
                              error=e)

    if db_token.used:
        raise CustomException(status_code=status.HTTP_406_NOT_ACCEPTABLE, status='Failed',
                              message='This Token is Used.', error=None)

    if db_token.user is None:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed', message='User not found',
                              error=None)
    return db_token


def create_reset_token(user: any):
    try:
        reset_token = generate_token(email=user.email, token_type=TokenType.reset.value)
        expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
        data = UserToken(author=user.id, expire=expire, token=reset_token)
        session = SessionManager.create_session()

        session.add(data)
        session.commit()
        session.close()
        return reset_token

    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error', error=e)


def create_active_token(user: any):
    try:
        token = generate_token(email=user.email, token_type=TokenType.active.value)
        expire = datetime.utcnow() + timedelta(minutes=ACTIVE_TOKEN_EXPIRE_MINUTES)
        data = UserToken(author=user.id, expire=expire, token=token)
        session = SessionManager.create_session()

        session.add(data)
        session.commit()
        session.close()
        return token

    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error', error=e)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") == TokenType.access.value:
            email: str = payload.get("sub")
            if email is None:
                raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                                      status='Failed', message='Incorrect Token.', error=None)
        else:
            raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  status='Failed', message='Incorrect Access Token.', error=None)

    except JWTError as e:
        message = f'{str(e)} Please login.'
        if "Signature" in message:
            message = message.replace("Signature", "Token")
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message=f'Invalid Token: {message}.', error=None)
    except Exception as e:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message='Internal server error',
                              error=e)

    try:
        session = SessionManager.create_session()

        user = session.query(User).filter(User.email == email).first()
        session.close()
    except Exception as e:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED, status='Failed',
                              message='Internal server error',
                              error=e)

    if user is None:
        raise CustomException(status=status.HTTP_401_UNAUTHORIZED, message='User not found')
    return user
