from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.db import get_db


from src.core.config.settings import AuthSettings

router = APIRouter(prefix="/tasks", tags=["tasks"])
