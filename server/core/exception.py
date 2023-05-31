from fastapi import status


class CustomException(Exception):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, status='Failed', message='', error:any=None):
        self.status_code = status_code
        self.status = status
        self.error = str(error)
        self.message = message
