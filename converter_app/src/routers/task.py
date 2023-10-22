from typing import List

from fastapi import APIRouter, Depends, status, Request, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from sqlalchemy.orm import Session
from src.db.db import get_db
from src.logic.tasks import get_all_tasks
from src.schemas.task import ConversionTaskBase, ConversionTaskCreateSuccess
from fastapi_jwt_auth import AuthJWT
from fastapi import HTTPException
from fastapi import UploadFile, Form, HTTPException
from datetime import datetime
from src.models.task import Task
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
    response_model=List[ConversionTaskBase],
    responses=get_tasks_responses
)
def get_conversion_tasks(
        current_user: AuthJWT = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    # Implicitly the depends (get_current_user function will check for the JWT requirements)
    tasks = get_all_tasks(db)

    return tasks


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ConversionTaskList,
    responses=get_task_responses
)
def get_conversion_task(
        current_user: AuthJWT = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    pass


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ConversionTaskCreateSuccess,
    responses=create_responses
)
def create_conversion_task(
        current_user: AuthJWT = Depends(get_current_user),
        file: UploadFile = Form(...),
        format: str = Form(...),
        db: Session = Depends(get_db)
):
    # Extract the file
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb+") as buffer:
        buffer.write(file.file.read())

    # Create a new database entry with status "uploaded"
    new_task = ConversionTask(
        filename=file.filename,
        timestamp=datetime.utcnow(),
        status="uploaded",
        desired_format=format
    )
    db.add(new_task)
    db.commit()


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
        current_user: AuthJWT = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return None
