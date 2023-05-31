from formencode import Schema, validators, FancyValidator, Invalid, All
# from core.db import create_session
from modules.users.models import User


class PageValidator(Schema):
    parent_page_id = validators.Int(not_empty=False)
    author = validators.Int(not_empty=True)
    page_name = validators.String(not_empty=True, strip=True)
    page_description = validators.String(not_empty=False, strip=True)
    color = validators.String(not_empty=False, strip=True)
    # first_name = validators.String(max=255, strip=True, not_empty=True)
    # create_date = validators.datetime_time()
    # last_edit = validators.datetime_time()
