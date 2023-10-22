from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from src.db.db import get_db
from fastapi_jwt_auth import AuthJWT
from src.schemas.task import (
    UserTasks,
    TaskInfo
)
from src.logic.task import (
    get_user_tasks,
    delete_task_by_id
)
from src.core.config.settings import AuthSettings

router = APIRouter(prefix="/tasks", tags=["tasks"])

@AuthJWT.load_config
def get_config():
    return AuthSettings()


@router.get("/", status_code=200, response_model=list[UserTasks])
def get_available_tasks(db: Session = Depends(get_db), Authorize: AuthJWT = Depends(), max: int = 100, order: int = 0):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    tasks = get_user_tasks(db, user_id=current_user, limit=max, order=order)
    return tasks
        

@router.get("/{id}", status_code=200, response_model=TaskInfo)
def get_task_by_id(id: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        task = get_task_by_id(db, id=id, user_id=current_user)
        return task
   

@router.delete("/{id}", status_code=204)
def get_delete_task_by_id(id: str, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    delete_task_by_id(db, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)