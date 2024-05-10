from datetime import datetime
from typing import List

from fastapi import UploadFile
from pydantic import BaseModel

class Download(BaseModel):
    user_id: int
    tag: str
    path: str
    filename: str

class Upload(BaseModel):
    user_id: int
    tag: str
    file: UploadFile

class FileName(BaseModel):
    filename: str
    nameuuid4: str

class FileProfile(BaseModel):
    id: int
    filename: str