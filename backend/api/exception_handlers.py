from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from backend.core.exceptions import (TasketError, TaskNotFoundError, PermissionDeniedError,
                                            InvalidCredentialsError, UserAlreadyExistsError)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(TaskNotFoundError)
    async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
        return JSONResponse(status_code=404, content={"detail": exc.message})

    @app.exception_handler(PermissionDeniedError)
    async def permission_denied_handler(request: Request, exc: PermissionDeniedError):
        return JSONResponse(status_code=403, content={"detail": exc.message})

    @app.exception_handler(InvalidCredentialsError)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsError):
        return JSONResponse(status_code=401, content={"detail": exc.message})

    @app.exception_handler(UserAlreadyExistsError)
    async def user_exists_handler(request: Request, exc: UserAlreadyExistsError):
        return JSONResponse(status_code=409, content={"detail": exc.message})

    @app.exception_handler(TasketError)
    async def base_error_handler(request: Request, exc: TasketError):
        return JSONResponse(status_code=500, content={"detail": exc.message})
