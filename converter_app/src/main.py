from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from src.db.db import engine
from src.db.base import Base
from src.core.config.settings import AuthSettings
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

app = FastAPI()

Base.metadata.create_all(bind=engine)

@AuthJWT.load_config
def get_config():
    return AuthSettings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": exc.message}
    )


@app.get("/ping", status_code=200)
def healthcheck():
    return "pong"

