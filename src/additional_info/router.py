from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import User
from database import get_async_session
from additional_info.models import Information
from additional_info.schemas import AddataionalInfoPut, AddataionalInfoRead
from auth.utils import get_user_db
from auth.base_config import current_user

router = APIRouter(
    prefix="/information",
    tags=["information"]
)

# async def get_current_user(user: User = Depends(get_user_db)):
#     if not user:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     return user
# , dependencies=[Depends(get_current_user)]

@router.put("/", response_model=AddataionalInfoRead)
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
        existing_info.additional_information = info_put.additional_information
        existing_info.telegram = info_put.telegram
        existing_info.vkontakte = info_put.vkontakte
        existing_info.education = info_put.education
        existing_info.work = info_put.work
    else:
        # Если информация не найдена, создаем новую запись
        new_info = Information(
            user_id=user.id,
            additional_information=info_put.additional_information,
            telegram=info_put.telegram,
            vkontakte=info_put.vkontakte,
            education=info_put.education,
            work=info_put.work
        )
        session.add(new_info)

    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update information")

    return AddataionalInfoRead(
        user_id=user.id,
        additional_information=info_put.additional_information,
        telegram=info_put.telegram,
        vkontakte=info_put.vkontakte,
        education=info_put.education,
        work=info_put.work
    )
