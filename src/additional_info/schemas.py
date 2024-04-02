from datetime import datetime

from pydantic import BaseModel


class AddataionalInfo(BaseModel):
    additional_information: str
    telegram: str
    vkontakte: str
    telephone: str