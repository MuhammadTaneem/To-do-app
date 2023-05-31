from formencode import Schema, validators


class TaskValidator(Schema):
    page_id = validators.Int(not_empty=False)
    author = validators.Int(not_empty=True)
    task_name = validators.String(not_empty=True, strip=True)
    task_description = validators.String(not_empty=False, strip=True)
    status = validators.String(not_empty=False, strip=True)
