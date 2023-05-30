from fastapi import status, HTTPException


class CustomException(Exception):
    def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, status='Failed', message='', error:any=None):
        self.status_code = status_code
        self.status = status
        self.error = str(error)
        self.message = message



# class CustomException(HTTPException):
#     def __init__(self, status_code=status.HTTP_401_UNAUTHORIZED, status='Failed', message='', error=None):
#         self.status = status
#         self.status_code = status_code
#         self.message = message
#         self.error = error
        # super().__init__(status_code, detail=self.message)

