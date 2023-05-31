from formencode import Schema, validators


class PageValidator(Schema):
    parent_page_id = validators.Int(not_empty=False)
    author = validators.Int(not_empty=True)
    page_name = validators.String(not_empty=True, strip=True)
    page_description = validators.String(not_empty=False, strip=True)
    color = validators.String(not_empty=False, strip=True)
