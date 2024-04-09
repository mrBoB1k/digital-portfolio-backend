from datetime import datetime

from pydantic import BaseModel


class AddataionalInfo(BaseModel):
    user_id: int
    additional_information: str
    telegram: str
    vkontakte: str
    education: str
    work: str