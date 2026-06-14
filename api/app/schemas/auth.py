from pydantic import BaseModel

from app.models.user import UserRole


class LoginRequest(BaseModel):
    email: str
    password: str


class UserRead(BaseModel):
    id: int
    email: str
    role: UserRole


class AuthUserResponse(BaseModel):
    user: UserRead
