from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    email: str
    password1: str
    password2: str


class UserLogin(UserBase):
    password: str


class UserCreateSuccess(BaseModel):
    detail: str = "User created successfully"


class UserLoginRequest(BaseModel):
    username: str
    password: str


class UserLoginSuccess(BaseModel):
    token: str


class UserResetSuccess(BaseModel):
    detail: str = "All users deleted successfully"
