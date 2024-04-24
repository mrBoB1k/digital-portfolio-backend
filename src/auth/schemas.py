from datetime import datetime

from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    first_name: str
    last_name: str
    city: str
    sex: str
    birth_date: datetime
    registered_at: datetime
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    city: str
    sex: str
    birth_date: datetime
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False