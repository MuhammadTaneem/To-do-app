import formencode
from fastapi import APIRouter, status, Response, Depends, Request
from fastapi.responses import JSONResponse
from core.dependencis import send_email, create_active_token, verify_active_token
from core.exception import CustomException
from modules.users.models import User
from core.db import SessionManager
from .validator import UserValidator, PasswordValidator, UserUpdateValidator, UserLoginValidator, ResetPasswordValidator
from . import schema
from core.decorators import login_required
from core.enum import TokenType
from core.dependencis import get_hash_password, verify_password, create_access_token, get_current_user, \
    create_reset_token, RESET_TOKEN_EXPIRE_MINUTES, generate_token, verify_reset_token, ACTIVE_TOKEN_EXPIRE_MINUTES

router = APIRouter()


@router.get("/")
def get_user(response: Response, ):
    try:
        # session = create_session()
        session = SessionManager.create_session()

        result = session.query(User).all()
        session.close()
        result = schema.UserListView(users=result)
        response.status_code = status.HTTP_200_OK
        return {'status': status.HTTP_200_OK, 'message': 'User list loaded', 'users': result.users}

    except CustomException as e:
        raise e

    except Exception as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': status.HTTP_404_NOT_FOUND, 'message': 'Internal server error ', 'error_dict': e}


# pydantic with formencode

# @router.post("/")
# def create_user(user: schema.NewUser):
#     try:
#         user_dict = user.__dict__
#         clean_data = UserValidator.to_python(user_dict)
#         clean_data.update({'password': get_hash_password(clean_data["password"])})
#         del clean_data["password_confirm"]
#         data = User(**clean_data)
#         session = create_session()
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         session.close()
#         data = schema.ReadUser(**data.__dict__)
#         return JSONResponse(status_code=status.HTTP_201_CREATED,
#                             content={'status': 'Success', 'message': 'User Created successfully',
#                                      'user': data})
#
#     except formencode.Invalid as e:
#         return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
#                             content={'status': 'Failed', 'message': 'Fix the following error',
#                                      'errors': e.unpack_errors()})
#
#     except Exception as e:
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             content={'status': 'Failed', 'message': 'Internal server error',
#                                      'errors': e})


# only formencode without pydantic validation
@router.post("/")
async def create_user(request: Request):
    try:
        # user_dict = user.__dict__
        user_dict = await request.json()
        # import pdb;pdb.set_trace()
        clean_data = UserValidator.to_python(user_dict)
        clean_data.update({'password': get_hash_password(clean_data["password"])})
        del clean_data["password_confirm"]
        data = User(**clean_data)
        # session = create_session()
        session = SessionManager.create_session()

        session.add(data)
        session.commit()
        session.refresh(data)
        session.close()

        # import pdb;pdb.set_trace()
        active_token = create_active_token(data)

        active_link = f' {str(request.url)}active?token={active_token}'
        msg = f"Dear {data.first_name} {data.last_name}, \nClick the link to reset your password: \n {active_link}this link will be expired in. {ACTIVE_TOKEN_EXPIRE_MINUTES} minutes."
        send_email(data.email, "Account Activation", msg)
        data = schema.ReadUser.from_orm(data).__dict__

        # data = schema.ReadUser(**data.__dict__)
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content={'status': 'Success', 'message': 'User Created successfully. Please Check your '
                                                                     'email to active your account', 'user': data})
    except formencode.Invalid as e:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content={'status': 'Failed', 'message': 'Fix the following error',
                                     'errors': e.unpack_errors()})

    except CustomException as e:
        raise e

    except Exception as e:
        # import pdb;pdb.set_trace()
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error', error=e)

        # CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed', message='Internal server error', error=e)
        #                              'errors': e)
        # return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #                     content={'status': 'Failed', 'message': 'Internal server error',
        #                              'errors': e})


# only pydantic
# @router.post("/")
# async def create_user(request: Request):
#     try:
#         user_dict = await request.json()
#         clean_data = schema.NewUser(**user_dict)
#         print(f"clean_data: {clean_data}")
#         clean_data.password = get_hash_password(clean_data.password)
#         del clean_data.password_confirm
#         data = User(**clean_data.__dict__)
#         session = create_session()
#         session.add(data)
#         session.commit()
#         session.refresh(data)
#         session.close()
#         data = schema.ReadUser(**data.__dict__).__dict__
#         return JSONResponse(status_code=status.HTTP_201_CREATED,
#                             content={'status': 'Success', 'message': 'User Created successfully',
#                                      'user': data})
#
#     except ValidationError as e:
#         return pydanticError(e)
#         # return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
#         #                     content={'status': 'Failed', 'message': 'Fix the following error',
#         #                              'errors': e})
#     except Exception as e:
#         return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             content={'status': 'Failed', 'message': 'Internal server error',
#                                      'errors': e})


@router.post("/login")
async def login_user(request: Request):
    try:
        user_dict = await request.json()
        # import pdb;pdb.set_trace()
        UserLoginValidator.to_python(user_dict)

        # session = create_session()
        session = SessionManager.create_session()

        user_exists = session.query(User).filter(User.email == user_dict['email']).first()
        session.close()

        if not user_exists:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={'status': 'Failed', 'message': 'User not found, Please create an account.',
                                         'errors': None})

        password_verification = verify_password(user_dict['password'], user_exists.password)
        # import pdb;pdb.set_trace()
        if not password_verification:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={'status': 'Failed', 'message': 'Incorrect password.',
                                         'errors': None})

        data = {
            'id': user_exists.id,
            'email': user_exists.email,
            'token': generate_token(email=user_exists.email, token_type=TokenType.access.value)
        }
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'status': 'Success', 'message': 'Login successfully',
                                     'user': data})
    except formencode.Invalid as e:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content={'status': 'Failed', 'message': 'Fix the following error.',
                                     'errors': e.unpack_errors()})

    except CustomException as e:
        raise e

    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal  server error', error=e)



@router.put("/change_password")
@login_required
async def change_password(request: Request):
    try:
        current_user = request.state.user
        passwords = await request.json()
        PasswordValidator.to_python(passwords)
        password_verification = verify_password(passwords['old_password'], current_user.password)
        if not password_verification:
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                                content={'status': 'Failed', 'message': 'Incorrect Password.',
                                         'errors': None})
        current_user.password = get_hash_password(passwords['new_password'])
        session = SessionManager.create_session()

        session.merge(current_user)
        session.commit()
        session.close()
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'status': 'Success', 'message': 'password changed.',
                                     'user': {
                                         'id': current_user.id,
                                         'email': current_user.email,
                                         'name': f'{current_user.first_name}  {current_user.last_name}',
                                     }})

    except formencode.Invalid as e:
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content={'status': 'Failed', 'message': 'Fix the following error.',
                                     'errors': e.unpack_errors()})

    except CustomException as e:
        raise e

    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={'status': 'Failed', 'message': 'Internal server error.',
                                     'errors': str(e)})


@router.post("/reset_password")
async def reset_password_request(request: Request):
    try:

        password_reset_data = await request.json()
        if not password_reset_data['email']:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                content={'status': 'Failed', 'message': 'Fix the following error',
                                         'errors': {
                                             'email': 'This field is required'
                                         }})
        session = SessionManager.create_session()

        user = session.query(User).filter(User.email == password_reset_data['email']).first()
        session.close()
        if user is None:
            return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                content={'status': 'Failed', 'message': 'User not found',
                                         'error': None})

        reset_token = create_reset_token(user)
        reset_link = f' {str(request.url)}confirm?token={reset_token}'
        msg = f"Dear {user.first_name} {user.last_name}, \nClick the link to reset your password: {reset_link}this link will be expired in. {RESET_TOKEN_EXPIRE_MINUTES} minutes."

        send_email(password_reset_data['email'], "Password Reset Request", msg)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'status': 'Success',
                                     'message': 'Password reset email sent. Please check you email'})

    except CustomException as e:
        raise e


    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error', error=e)


@router.post("/reset_password_verify")
async def reset_password_verify(request: Request):
    try:
        reset_dict = await request.json()
        db_token = verify_reset_token(reset_dict["token"])
        clean_data = ResetPasswordValidator.to_python(reset_dict)
        session = SessionManager.create_session()

        db_token.used = True
        db_token.user.password = get_hash_password(clean_data['new_password'])
        session.merge(db_token)
        session.commit()
        session.close()
        return {'status': status.HTTP_200_OK, 'message': 'password changed', 'user': ''}

    except formencode.Invalid as e:
        return {'status': status.HTTP_406_NOT_ACCEPTABLE, 'message': 'Fix the following error ',
                'errors': e.unpack_errors()}

    except CustomException as e:
        raise e

    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error ', error=e)


@router.post("/active")
async def active_user(request: Request):
    try:
        reset_dict = await request.json()
        db_token = verify_active_token(reset_dict["token"])
        session = SessionManager.create_session()

        db_token.user.active = True
        db_token.used = True
        session.merge(db_token)
        session.commit()
        session.close()
        user  = schema.ReadUser(**db_token.user.__dict__).__dict__
        return {'status': status.HTTP_200_OK, 'message': 'Account Activated', 'user': user}

    except formencode.Invalid as e:
        return {'status': status.HTTP_406_NOT_ACCEPTABLE, 'message': 'Fix the following error ',
                'errors': e.unpack_errors()}

    except CustomException as e:
        raise e

    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error ', error=e)


@router.get("/profile")
@login_required
async def get_user(request: Request):
    try:
        current_user = request.state.user
        current_user = schema.ReadUser(**current_user.__dict__).__dict__
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'status': 'Success', 'message': 'User Profile loaded', 'user': current_user})

    except CustomException as e:
        raise e

    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error', error=e)


@router.put("/profile")
@login_required
async def update_user(request: Request):
    try:
        user_dict = await request.json()
        current_user = request.state.user
        user_dict = UserUpdateValidator.to_python(user_dict)
        current_user.first_name = user_dict.get('first_name')
        current_user.last_name = user_dict.get('last_name')
        current_user.address = user_dict.get('address')
        current_user.email = user_dict.get('email')

        # session = create_session()
        session = SessionManager.create_session()

        session.merge(current_user)
        session.commit()
        session.close()
        current_user = schema.ReadUser(**current_user.__dict__).__dict__

        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={'status': 'Success', 'message': 'Profile updated', 'user': current_user})

    except formencode.Invalid as e:

        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            content={'status': 'Failed', 'message': 'Fix the following error.',
                                     'errors': e.unpack_errors()})

    except CustomException as e:
        raise e

    except Exception as e:
        raise CustomException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, status='Failed',
                              message='Internal server error.', error=e)


def pydanticError(e: any):
    error_dict = {}
    for error in e.errors():
        print(error)
        if error:
            field_name = error['loc'][0]
            error_msg = error['msg']
            error_dict[field_name] = error_msg

    if error_dict:
        error_message = "Fix the following errors:"
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
                'message': error_message,
                'errors': error_dict
            }
        )
    else:
        error_message = "Unknown validation error"
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': error_message
            }
        )
