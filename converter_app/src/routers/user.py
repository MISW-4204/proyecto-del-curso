from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from src.db.db import get_db
from src.logic.user import (
    validate_user,
    create_user,
    validate_user_login,
    get_token,
    reset_users,
)
from fastapi_jwt_auth import AuthJWT
from src.core.config.settings import AuthSettings
from src.schemas.user import (
    UserCreate,
    UserCreateSuccess,
    UserLogin,
    UserLoginSuccess,
    UserResetSuccess,
)
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException

router = APIRouter(prefix="/auth", tags=["auth"])


@AuthJWT.load_config
def get_config():
    return AuthSettings()


signup_responses = {
    status.HTTP_409_CONFLICT: {
        "description": "Email or username already registered",
        "content": {
            "application/json": {
                "example": {"detail": "Email 'user_email' already registered"}
            }
        },
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "One or more fields are invalid",
        "content": {
            "application/json": {
                "example": {"detail": "Email 'user_email' is not a valid email address"}
            }
        },
    },
}

login_responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Invalid credentials",
        "content": {"application/json": {"example": {"detail": "Invalid credentials"}}},
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "description": "One or more fields are invalid",
        "content": {
            "application/json": {
                "example": {"detail": "Email 'user_email' is not a valid email address"}
            }
        },
    },
}


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=UserCreateSuccess,
    responses=signup_responses,
)
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        validate_user(db, user)
        user = create_user(db, user)
        return UserCreateSuccess(detail=f"User created successfully")
    except HTTPException as e:
        raise e


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=UserLoginSuccess,
    responses=login_responses,
)
def login_user(
    user: UserLogin, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()
):
    try:
        db_user = validate_user_login(db, user)
        return get_token(db_user, Authorize)
    except HTTPException as e:
        raise e


@router.delete("/reset", status_code=200, response_model=UserResetSuccess)
def reset(
    db: Session = Depends(get_db),
):
    return reset_users(db=db)
