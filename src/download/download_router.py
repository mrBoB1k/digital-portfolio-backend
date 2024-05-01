from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
import os
import uuid
from auth.base_config import current_user
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

from auth.models import User
from download.schemas import Download, Upload

router = APIRouter(
  tags=["file"]
)

@router.get("/file/download")
async def download_file():
    return FileResponse(path='dynamic/'+'89380bfe.png', filename='Мой милый кот.png', media_type='multipart/form-data')

# @router.post("/file/upload-bytes")
# async def upload_file_bytes(file_bytes: bytes = File()):
#   return {'file_bytes': str(file_bytes)}


# @router.post("/file/upload-file")
# async def upload_file(file: UploadFile):
#     file_name = str(uuid.uuid4())[:8]  # генерируем уникальное имя из первых 8 символов UUID
#     file_extension = os.path.splitext(file.filename)[1]  # расширение файла
#     file_path = os.path.join('dynamic/', file_name + file_extension)

#     # сохраняем содержимое пришедшего файла
#     with open(file_path, 'wb') as file_save:
#         for chunk in file.file:
#             file_save.write(chunk)
        
#     return {"filename": file.filename}



@router.post("/file/upload-file", response_model=Download)
async def upload_file(
    file: Upload,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    file_name = str(uuid.uuid4())[:8]  # генерируем уникальное имя из первых 8 символов UUID
    file_extension = os.path.splitext(file.file.filename)[1]  # расширение файла
    file_path = os.path.join('dynamic/', file_name + file_extension)

    # сохраняем содержимое пришедшего файла
    with open(file_path, 'wb') as file_save:
        for chunk in file.file.file:
            file_save.write(chunk)
        
    return {"filename": file.file.filename}
