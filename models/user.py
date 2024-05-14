from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    mobile: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
