from datetime import datetime
from typing import List

from pydantic import BaseModel


class AddataionalInfoPut(BaseModel):
    email: str
    technology: List[str]
    tg: str
    vk: str
    education: str
    work: str


class AddataionalInfoPutRead(BaseModel):
    user_id: int
    email: str
    technology: List[str]
    tg: str
    vk: str
    education: str
    work: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AddataionalInfoRead(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    city: str
    technology: List[str]
    birth_date: datetime
    sex: str
    education: str
    work: str
    vk: str
    email: str
    tg: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime
    sex: str
    city: str
