from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.exceptions import AppBaseError

def register_exception_handlers(app):
    @app.exception_handler(AppBaseError)
    async def app_base_error_handler(request: Request, exc: AppBaseError):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

