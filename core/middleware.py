from fastapi.responses import JSONResponse
from fastapi import Request
from core.exceptions import CustomAPIException

async def custom_exception_handler(request: Request, exc: CustomAPIException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )
