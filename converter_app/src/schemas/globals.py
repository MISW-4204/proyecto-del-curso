from pydantic import BaseModel


class PingResponse(BaseModel):
    detail: str = "pong"
