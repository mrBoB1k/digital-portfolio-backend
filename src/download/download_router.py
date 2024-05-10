from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
import os
import uuid

from sqlalchemy import select
from auth.base_config import current_user
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session

from auth.models import User
from download.schemas import FileProfile, Upload, FileName, Download
from download.models import Download as dbDownload
from auth.models import User as dbUser

router = APIRouter(
  tags=["file"]
)

router2 = APIRouter(
  tags=["avatar"]
)

@router.get("/file/download/{file_id}")
async def download_file(
    file_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(dbDownload).filter(dbDownload.id == file_id))
    file = result.scalars().first()
    
    if file:
        return FileResponse(path=file.path, filename=file.filename, media_type='multipart/form-data')
    else:
        raise HTTPException(status_code=404, detail="Not found")

@router.get("/file/search/{user_id}")
async def search_file(
    user_id: int,
    tag: str,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(dbDownload).filter(dbDownload.user_id == user_id).filter(dbDownload.tag == tag))
    files = result.scalars().all()
    
    if files:
        file_profiles = []
        for file in files:
            file_profile = FileProfile(id=file.id, filename=file.filename)
            file_profiles.append(file_profile)
        return file_profiles
    else:
        raise HTTPException(status_code=404, detail="Not found")

@router.delete("/file/delete/{file_id}")
async def delete_file(
    file_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(dbDownload).filter(dbDownload.id == file_id))
    file = result.scalars().first()
    
    if file:
        if file.user_id == user.id:
            # Удаление файла по указанному пути
            pathFile = file.path
            try:
                await session.delete(file)
                await session.commit()  # Важно вызвать commit() после delete() и использовать await
                os.remove(pathFile)
                return {"message": "File deleted successfully"}
            except Exception as e:
                await session.rollback()  # Откатываем транзакцию в случае ошибки
                raise HTTPException(status_code=500, detail="Failed to delete file from database") from e
        else:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have permission to delete this file")
    else:
        raise HTTPException(status_code=404, detail="File not found")

@router.put("/file/update_tag/{file_id}")
async def update_file_tag(
    file_id: int,
    new_tag: str,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(dbDownload).filter(dbDownload.id == file_id))
    file = result.scalars().first()
    
    if file:
        if file.user_id == user.id:
            try:
                file.tag = new_tag
                await session.commit()  # Важно вызвать commit() после изменения объекта и использовать await
                return {"message": "File tag updated successfully"}
            except Exception as e:
                await session.rollback()  # Откатываем транзакцию в случае ошибки
                raise HTTPException(status_code=500, detail="Failed to update file tag in database") from e
        else:
            raise HTTPException(status_code=403, detail="Forbidden: You do not have permission to update this file's tag")
    else:
        raise HTTPException(status_code=404, detail="File not found")

async def upload_file(file: UploadFile):
    file_name = str(uuid.uuid4())[:8]  # генерируем уникальное имя из первых 8 символов UUID
    file_extension = os.path.splitext(file.filename)[1]  # расширение файла
    file_path = os.path.join('dynamic/', file_name + file_extension)

    # сохраняем содержимое пришедшего файла
    with open(file_path, 'wb') as file_save:
        for chunk in file.file:
            file_save.write(chunk)
        
    return FileName(
        filename = file.filename,
        nameuuid4 = file_path
    )

@router.post("/file/upload_file", response_model=FileProfile)
async def upload_file2(
    tag: str,
    filename: FileName = Depends(upload_file),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    download = dbDownload(
        user_id=user.id,
        tag=tag,
        path=filename.nameuuid4,
        filename=filename.filename
    )
    session.add(download)

    try:
        # Коммитим изменения, чтобы они были сохранены в базе данных
        await session.commit()
        # Возвращаем объект FileProfile
        return FileProfile(id=download.id, filename=download.filename)
    except Exception as e:
        # Если возникла ошибка, откатываем транзакцию
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to upload file")
    finally:
        # Закрываем сессию
        await session.close()

async def upload_avatar(file: UploadFile):
    file_name = str(uuid.uuid4())[:8] 
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join('dynamic_avatar/', file_name + file_extension)
    
    allowed_formats = [".jpg"]  
    file_format = file_extension.lower()

    if file_format not in allowed_formats:
        raise HTTPException(status_code=400, detail="Unsupported file format. Only JPG. '.jpg' ")

    with open(file_path, 'wb') as file_save:
        for chunk in file.file:
            file_save.write(chunk)
        
    return file_path


@router2.put("/avatar/upload")
async def upload_avatar2(
    file_path: str = Depends(upload_avatar),
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    old_avatar_path = None

    try:
        if user.avatar:
            old_avatar_path = user.avatar

        user.avatar = file_path
        
        await session.commit()

        if old_avatar_path:
                os.remove(old_avatar_path)

        return {"message": "Avatar uploaded successfully"}
    except Exception as e:
        # Откатить транзакцию в случае ошибки
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to upload avatar") from e
    finally:
        # Закрыть сессию после завершения всех операций
        await session.close()


@router2.get("/avatar/{user_id}")
async def get_avatar(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(select(dbUser).filter(dbUser.id == user_id))
    user = result.scalars().first()

    if user:
        if user.avatar:
            return FileResponse(path=user.avatar, media_type="image/jpeg")
        else: 
            return FileResponse(path="dynamic_avatar/anonimus.jpg", media_type="image/jpeg")
    else:
        raise HTTPException(status_code=404, detail="User not found")