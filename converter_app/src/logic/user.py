from sqlalchemy.orm import Session
from src.core.config.settings import Settings
from src.models.user import User as UserModel
from src.schemas.user import UserCreate, UserLogin, UserLoginSuccess, UserResetSuccess
from fastapi import HTTPException, status
import hashlib
import re
from fastapi_jwt_auth import AuthJWT


def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_username(db: Session, username: str) -> UserModel | None:
    return db.query(UserModel).filter(UserModel.username == username).first()


def create_user(db: Session, user: UserCreate):
    new_user = UserModel(
        email=user.email,
        username=user.username,
        password_hash=hash_password(user.password1),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def validate_user(db: Session, user: UserCreate):
    if invalid_email(email=user.email):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Email {user.email} is not a valid email address",
        )
    if get_user_by_email(db=db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email '{user.email}' already registered",
        )
    if get_user_by_username(db=db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{user.username}' already registered",
        )
    if passwords_do_not_match(password1=user.password1, password2=user.password2):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Passwords do not match",
        )
    if password_not_strong(password=user.password1):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password is not strong enough. It must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter and one number",
        )


def invalid_email(email: str):
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
    return not re.fullmatch(regex, email)


def passwords_do_not_match(password1: str, password2: str):
    return password1 != password2


def password_not_strong(password: str):
    return (
        len(password) < 8
        or password.isalpha()
        or password.isnumeric()
        or password.islower()
        or password.isupper()
    )


def hash_password(password: str):
    return hashlib.sha512(password.encode()).hexdigest()


def validate_user_login(db: Session, user: UserLogin):
    db_user = get_user_by_username(db=db, username=user.username)
    if not db_user or not db_user.password_hash == hash_password(user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return db_user


def get_token(db_user: UserModel, Authorize: AuthJWT):
    token = Authorize.create_access_token(subject=db_user.username)
    return UserLoginSuccess(token=token)


def reset_users(db: Session):
    db.query(UserModel).delete()
    db.commit()
    return UserResetSuccess()
