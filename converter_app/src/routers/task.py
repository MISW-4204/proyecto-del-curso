from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session
from src.db.db import get_db
from src.schemas.task import ConversionTaskBase, ConversionTaskList, ConversionTaskCreateSuccess
from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException

from src.core.config.settings import AuthSettings

router = APIRouter(prefix="/tasks", tags=["tasks"])

get_tasks_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid credentials",
        "content": {
            "application/json": {
                "example": {
                    {
                        "detail": "Invalid credentials"
                    }
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Task not found",
        "content": {
            "application/json": {
                "example": {
                    {
                        "detail": "Task not found"
                    }
                }
            }
        }
    }
}

get_task_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid credentials",
        "content": {
            "application/json": {
                "example": {
                    {
                        "detail": "Invalid credentials"
                    }
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Task not found",
        "content": {
            "application/json": {
                "example": {
                    {
                        "detail": "Task not found"
                    }
                }
            }
        }
    }
}

create_responses = {
    status.HTTP_: {
        "description": "Invalid credentials",
        "content": {
            "application/json": {
                "example": {
                    {
                        "detail": "Invalid credentials"
                    }
                }
            }
        }
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Task not found",
        "content": {
            "application/json": {
                "example": {
                    {
                        "detail": "Task not found"
                    }
                }
            }
        }
    }
}


def get_current_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return Authorize


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ConversionTaskBase,
    responses=get_tasks_responses
)
def get_conversion_tasks(current_user: AuthJWT = Depends(get_current_user)):
    pass


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ConversionTaskList,
    responses=get_task_responses
)
def get_conversion_task(current_user: AuthJWT = Depends(get_current_user)):
    pass


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ConversionTaskCreateSuccess,
    responses=create_responses
)
def create_conversion_task(current_user: AuthJWT = Depends(get_current_user)):
    pass


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(current_user: AuthJWT = Depends(get_current_user)):
    return None
