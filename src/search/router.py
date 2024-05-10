from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from auth.models import User
from additional_info.models import Information
from search.schemas import TechnologyList, UserList
from database import get_async_session

router = APIRouter(
  tags=["search"]
)

@router.post("/search/users", response_model=List[UserList])
async def search_users(
    city: Optional[str] = None,
    technology: Optional[TechnologyList] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).outerjoin(Information).options(selectinload(User.information))

    if city:
        query = query.filter(User.city == city)
    if technology:
        query = query.filter(Information.technology.contains(technology.technology))
    if first_name:
        query = query.filter(User.first_name == first_name)
    if last_name:
        query = query.filter(User.last_name == last_name)

    result = await session.execute(query)
    users = result.scalars().all()

    if users:
        users_list = []
        for user in users:
            user_info = UserList(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                city=user.city,
                technology=user.information.technology if user.information else None
            )
            users_list.append(user_info)
        
        return users_list
    else:
        raise HTTPException(status_code=404, detail="No users found")
