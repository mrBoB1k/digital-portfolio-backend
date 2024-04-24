from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session
from additional_info.models import Information
from additional_info.schemas import AddataionalInfoPut, AddataionalInfoPutRead, AddataionalInfoRead
from auth.utils import get_user_db
from auth.base_config import current_user

router = APIRouter(
    tags=["information"]
)

# async def get_current_user(user: User = Depends(get_user_db)):
#     if not user:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     return user
# , dependencies=[Depends(get_current_user)]

@router.put("/send_additional_information", response_model=AddataionalInfoPutRead)
async def add_user_additional_info(
    info_put: AddataionalInfoPut,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    # Ваша текущая реализация функции здесь
    stmt = select(Information).filter(Information.user_id == user.id)
    result = await session.execute(stmt)
    existing_info = result.scalars().first()

    if existing_info:
        # Если информация найдена, обновляем ее
        existing_info.technology = info_put.technology
        existing_info.tg = info_put.tg
        existing_info.vk = info_put.vk
        existing_info.education = info_put.education
        existing_info.work = info_put.work
    else:
        # Если информация не найдена, создаем новую запись
        new_info = Information(
            user_id=user.id,
            technology=info_put.technology,
            tg=info_put.tg,
            vk=info_put.vk,
            education=info_put.education,
            work=info_put.work
        )
        session.add(new_info)

    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update information")

    return AddataionalInfoPutRead(
        user_id=user.id,
        technology=info_put.technology,
        tg=info_put.tg,
        vk=info_put.vk,
        education=info_put.education,
        work=info_put.work
    )



@router.get("/get_additional_information/{user_id}", response_model=AddataionalInfoRead)
async def get_user_additional_info(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = select(User).filter(User.id == user_id).options(
        sqlalchemy.orm.selectinload(User.information)
    )
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.information:
        additional_info = AddataionalInfoRead(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            city=user.city,
            technology=[],
            birth_date=user.birth_date,
            sex=user.sex,
            education='',
            work='',
            vk='',
            email=user.email,
            tg='',
        )
    else:
        additional_info = AddataionalInfoRead(
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            city=user.city,
            technology=user.information.technology,
            birth_date=user.birth_date,
            sex=user.sex,
            education=user.information.education,
            work=user.information.work,
            vk=user.information.vk,
            email=user.email,
            tg=user.information.tg,
        )

    return additional_info


@router.get("/is_my_profile/{user_id}", response_model=bool)
async def is_my_profile(
    user_id: int,
    user: User = Depends(current_user),
) -> bool:
    if user and user.id == user_id:
        return True
    else:
        return False