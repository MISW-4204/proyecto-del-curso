from fastapi import FastAPI, status
from src.schemas.globals import PingResponse
from src.db.db import engine
from src.db.base import Base
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response
from src.routers import user

description = """Esta es una API para convertir de un archivo de video de un formato a otro.

Para poder usarla, primero debes registrarte y luego iniciar sesión.

Una vez iniciada la sesión, puedes subir un archivo de video y convertirlo a otro formato.

"""

tags_metadata = [
    {
        "name": "auth",
        "description": "Autenticación de usuarios",
    },
    {
        "name": "tasks",
        "description": "Tareas de conversión de videos",
    },
]

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Video Converter API",
    description=description,
    summary="API para convertir formatos de video",
    version="0.0.1",
    openapi_tags=tags_metadata,
)
app.include_router(
    user.router,
    prefix="/api",
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )


@app.get("/", status_code=status.HTTP_200_OK, response_model=PingResponse)
def ping():
    return PingResponse(detail="pong")
