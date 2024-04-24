from datetime import datetime

from pydantic import BaseModel


class AddataionalInfoPut(BaseModel):
    additional_information: str
    telegram: str
    vkontakte: str
    education: str
    work: str


class AddataionalInfoRead(BaseModel):
    user_id: int
    additional_information: str
    telegram: str
    vkontakte: str
    education: str
    work: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True