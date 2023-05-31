from pydantic import BaseModel, validator, Field
from core.db import SessionManager


class Header:
    token: str


# class UniqueUserValidator:
#     @classmethod
#     def validate(cls, value):
#         email_msg = 'That email already exists'
#         session = create_session()
#         user_exists = session.query(User).filter(User.email == value).first()
#         session.close()
#         if user_exists:
#             raise ValueError(email_msg)
#         return value


class User(BaseModel):
    first_name: str
    last_name: str | None = None
    email: str
    address: str | None = None

    # class Config:
    #     orm_mode = True

    class Config:
        orm_mode = True
        # error_msg_templates = {
        #     'value_error.missing': 'first_name address is not valid.',
        # }

    # @validator('email')
    # def validate_email(cls, email: str) -> str:
    #     print(UniqueUserValidator.validate())
    #     return UniqueUserValidator.validate(email)


class ReadUser(User):
    id: int | None

    class Config:
        orm_mode = True


# class LoginUser(BaseModel):
#     email: str
#     password: str = Field(..., min_length=6)
#
#     class Config:
#         orm_mode = True
#
#
# class PasswordChange(BaseModel):
#     old_password: str
#     new_password: str
#
#
# class NewUser(User):
#     password: str
#     password_confirm: str
#
#     class Config:
#         orm_mode = True
#
#
# class UserListView(BaseModel):
#     users: list[User]
#
#
# class PasswordResetRequest(BaseModel):
#     email: str
#
#
# class PasswordResetVerify(BaseModel):
#     email: str
#     reset_token: str
#     new_password: str
