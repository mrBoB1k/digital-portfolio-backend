from fastapi import APIRouter, Depends
import fastapi_users
from sqlalchemy import func, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from database import get_async_session
from additional_info.models import information
from additional_info.schemas import AddataionalInfo

router = APIRouter(
    prefix="/information",
    tags=["information"]
)


@router.get("/")
async def get_user_additional_info(userid: int, session: AsyncSession = Depends(get_async_session)):
    query = select(information).where(information.c.user_id == userid)
    result = await session.execute(query)
    return result.all()



fastapi_users = fastapi_users.FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()


@router.post("/")
async def add_user_additional_info(addataional_info: AddataionalInfo, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    stmt = insert(information).values(
        user_id=user.id,
        additional_information=addataional_info.additional_information,
        telegram=addataional_info.telegram,
        vkontakte=addataional_info.vkontakte,
        telephone=addataional_info.telephone
    )
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}