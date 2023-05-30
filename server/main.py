import uvicorn
from fastapi import FastAPI
from starlette.responses import JSONResponse
from core.exception import CustomException
from core.middleware import user_middleware
from modules.users.main import router as userRouter
from modules.pages.main import router as pageRouter

app = FastAPI()
# app.add_middleware(user_middleware)
app.middleware("http")(user_middleware)
app.include_router(
    userRouter,
    prefix="/user",
    tags=["user"],
)

app.include_router(
    pageRouter,
    prefix="/page",
    tags=["page"],
)


# Custom Exception_handler --------------------------------
@app.exception_handler(Exception)
async def custom_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code,
                        content={"status": exc.status, "message": exc.message, "error": exc.error})


# @app.exception_handler(HTTPException)
# async def custom_exception_handler(request, exc):
#     print(exc)
#     import pdb;pdb.set_trace()
#     return JSONResponse(status_code=exc.status_code,
#                         content={"status": exc.status, "message": exc.message, "error": exc.error})
#
#

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    # import pdb;pdb.set_trace()
    return JSONResponse(status_code=exc.status_code,
                        content={"status": exc.status, "message": exc.message, "error": exc.error})

# pydantic validation exception handler  -----------------------------------------------

# @app.exception_handler(RequestValidationError)
# async def http_exception_accept_handler(request :Request, exc: RequestValidationError) -> JSONResponse:
#     error_dict = {}
#     # import pdb;pdb.set_trace()
#     for error in exc.raw_errors:
#         print(error)
#         if error.exc.errors:
#             for error_detail in error.exc.errors():
#                 field_name = error_detail['loc'][0]
#                 error_msg = error_detail['msg']
#                 error_dict[field_name] = error_msg
#     if error_dict:
#         error_message = "Fix the following errors:"
#         return JSONResponse(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             content={
#                 'status': status.HTTP_422_UNPROCESSABLE_ENTITY,
#                 'message': error_message,
#                 'errors': error_dict
#             }
#         )
#     else:
#         error_message = "Unknown validation error"
#         return JSONResponse(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             content={
#                 'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 'message': error_message
#             }
#         )


if __name__ == "__main__":
    print("program running")
    # uvicorn.run(app, host='0.0.0.0', port=8000)
    # uvicorn.run(app, host='localhost', port=8000)
    uvicorn.run(app)
