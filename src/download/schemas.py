from datetime import datetime
from typing import List

from fastapi import UploadFile
from pydantic import BaseModel

class Upload(BaseModel):
    tag: str
    file: UploadFile

class Download(BaseModel):
    user_id: int
    tag: str
    file: UploadFile