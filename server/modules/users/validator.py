from formencode import Schema, validators, FancyValidator, Invalid, All
from core.db import SessionManager
from modules.users.models import User


class UniqueUserValidator(FancyValidator):

    def _convert_to_python(self, value, state):
        # session = create_session()
        session = SessionManager.create_session()

        user_exists = session.query(User).filter(User.email == value).first()
        session.close()
        email_msg = 'That email already exists'
        if user_exists:
            raise Invalid(email_msg, value, state)

        return value


class UserValidator(Schema):
    first_name = validators.ByteString(not_empty=True, strip=True)
    last_name = validators.ByteString(not_empty=False, strip=True)
    address = validators.ByteString(not_empty=False, strip=True)
    email = All(validators.Email(not_empty=True, strip=True), UniqueUserValidator())
    password = validators.ByteString(not_empty=True, strip=True)
    password_confirm = validators.ByteString(not_empty=True, strip=True)
    chained_validators = [validators.FieldsMatch('password', 'password_confirm')]


class UserUpdateValidator(Schema):
    first_name = validators.ByteString(not_empty=True, strip=True)
    last_name = validators.ByteString(not_empty=False, strip=True)
    address = validators.ByteString(not_empty=False, strip=True)
    email = All(validators.Email(not_empty=True, strip=True))


class UserLoginValidator(Schema):
    password = validators.ByteString(not_empty=True, strip=True)
    email = All(validators.Email(not_empty=True, strip=True))


class PasswordValidator(Schema):
    old_password = validators.ByteString(not_empty=False, strip=True, if_missing=None)
    new_password = validators.ByteString(not_empty=True, strip=True)
    new_password_confirm = validators.ByteString(not_empty=True, strip=True)
    chained_validators = [validators.FieldsMatch('new_password', 'new_password_confirm')]
    # allow_extra_fields = True


class ResetPasswordValidator(Schema):
    token = validators.ByteString(not_empty=False, strip=True)
    new_password = validators.ByteString(not_empty=True, strip=True)
    new_password_confirm = validators.ByteString(not_empty=True, strip=True)
    chained_validators = [validators.FieldsMatch('new_password', 'new_password_confirm')]
