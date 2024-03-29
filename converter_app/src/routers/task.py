from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.db.db import get_db
from src.schemas.task import UserTasks, TaskInfo
from src.logic.task import get_user_tasks, delete_task_by_id
from typing import List
import shutil
import os
from fastapi import APIRouter, Depends, status, Request, UploadFile, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from src.db.db import get_db
from src.logic.tasks import get_all_tasks
from src.schemas.task import (
    ConversionTaskBase,
    ConversionTaskCreateSuccess,
    ConversionTaskCreate,
    TaskCreate
)
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import HTTPException
from fastapi import UploadFile, Form, HTTPException
from datetime import datetime
from src.models.task import TaskState


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", status_code=200, response_model=list[UserTasks])
def get_available_tasks(
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends(),
    max: int = 100,
    order: int = 0,
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    tasks = get_user_tasks(db, user_id=current_user, limit=max, order=order)
    return tasks


@router.get("/{id}", status_code=200, response_model=TaskInfo)
def get_task_by_id(
    id: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    task = get_task_by_id(db, id=id, user_id=current_user)
    return task


@router.delete("/{id}", status_code=204)
def get_delete_task_by_id(
    id: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    delete_task_by_id(db, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


get_tasks_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid credentials",
        "content": {"application/json": {"example": {"detail": "Invalid credentials"}}},
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Task not found",
        "content": {"application/json": {"example": {"detail": "Task not found"}}},
    },
}

get_task_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid credentials",
        "content": {"application/json": {"example": {"detail": "Invalid credentials"}}},
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Task not found",
        "content": {"application/json": {"example": {"detail": "Task not found"}}},
    },
}

create_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid credentials",
        "content": {"application/json": {"example": {"detail": "Invalid credentials"}}},
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Task not found",
        "content": {"application/json": {"example": {"detail": "Task not found"}}},
    },
}


def get_current_user(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except AuthJWTException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return Authorize


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ConversionTaskCreateSuccess,
    responses=create_responses,
)
def create_conversion_task(
    task: TaskCreate,
    current_user: AuthJWT = Depends(get_current_user),
    #filePath: str = "/",
    #format: str = " ",
    db: Session = Depends(get_db),
):
    # Extract the file
    #file_location = f"uploads/{file.filename}"
    #with open(file_location, "wb+") as buffer:
        #buffer.write(file.file.read())
    fileName = os.path.basename(task.filePath)
    print(task.filePath)
    print(type(task.filePath))
    f = open(task.filePath, "r")
    print(f.read())
    
    shutil.move(task.filePath, f'uploaded/{fileName}')
    new_task = ConversionTaskCreate(
        filename=fileName,
        timestamp=datetime.utcnow(),
        status=TaskState.uploaded,
        desired_format=format,
        url_original_file=task.filePath
    )
    db.add(new_task)
    db.commit()
