from typing import List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from auth.base_config import current_user
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import User
from database import get_async_session
from subscription.models import UserSubscription
from subscription.schemas import Mas, Sub
from sqlalchemy.orm import selectinload



router = APIRouter(
  tags=["sub"]
)


@router.get("/sub/subscriptions/{user_id}", response_model=List[Sub])
async def search_subscriptions(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(User)
        .filter(User.id == user_id)
        .options(selectinload(User.subscriptions))
    )
    user = result.scalars().first()
    if user:
        subscriptions = user.subscriptions

        if subscriptions:
            subscription_list = []

            for sub in subscriptions:
                result = await session.execute(select(User).filter(User.id == sub.user_id))
                subscription_user = result.scalars().first()
                if subscription_user:
                    subscription_add = Sub(id=subscription_user.id, first_name=subscription_user.first_name, last_name=subscription_user.last_name)
                    subscription_list.append(subscription_add)   
            return subscription_list
        else: 
            raise HTTPException(status_code=404, detail="Subscriptions not found")
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.get("/sub/subscriptions_count/{user_id}", response_model=int)
async def search_subscriptions_count(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(User)
        .filter(User.id == user_id)
        .options(selectinload(User.subscriptions))
    )
    user = result.scalars().first()
    if user:
        subscriptions = user.subscriptions
        return len(subscriptions)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.get("/sub/subscribers/{user_id}", response_model=List[Sub])
async def search_subscribers(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(User)
        .filter(User.id == user_id)
        .options(selectinload(User.subscribers))
    )
    user = result.scalars().first()
    if user:
        subscribers = user.subscribers
        
        if subscribers:
            subscriber_list = []
            for sub in subscribers:
                result = await session.execute(select(User).filter(User.id == sub.subscriber_id))
                subscriber_user = result.scalars().first()
                if subscriber_user:
                    subscriber_add = Sub(id=subscriber_user.id, first_name=subscriber_user.first_name, last_name=subscriber_user.last_name)
                    subscriber_list.append(subscriber_add)   
            return subscriber_list
        else:
            raise HTTPException(status_code=404, detail="Subscribers not found")
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/sub/subscribers_count/{user_id}", response_model=int)
async def search_subscribers_count(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(User)
        .filter(User.id == user_id)
        .options(selectinload(User.subscribers))
    )
    user = result.scalars().first()
    if user:
        subscribers = user.subscribers
        return len(subscribers)
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/sub/i_follow/{user_id}", response_model=bool)
async def i_follow(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    result = await session.execute(
        select(User)
        .filter(User.id == user.id)
        .options(selectinload(User.subscriptions))
    )

    user2 = result.scalars().first()


    subscriptions_list = [sub.user_id for sub in user2.subscriptions]

    return user_id in subscriptions_list

@router.get("/sub/subscribe_unsubscribe/{user_id}", response_model=Mas)
async def subscribe_unsubscribe(
    user_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")

    # Проверяем, существует ли пользователь с указанным user_id
    user_to_subscribe = await session.execute(
        select(User).filter(User.id == user_id)
    )
    user_exists = user_to_subscribe.scalar()

    if not user_exists:
        raise HTTPException(status_code=404, detail="User_id not found.")

    # Проверяем, подписан ли текущий пользователь уже на указанный user_id
    result = await session.execute(
        select(UserSubscription)
        .filter(UserSubscription.user_id == user_id)
        .filter(UserSubscription.subscriber_id == user.id)
    )
    subscription = result.scalars().first()

    if subscription:
        # Если подписка уже существует, удаляем ее из базы данных
        await session.delete(subscription)
        await session.commit()
        return Mas(message ="Подписка отменена успешно.")
    else:
        # Если подписка не существует, создаем новую запись в базе данных
        new_subscription = UserSubscription(user_id=user_id, subscriber_id=user.id)
        session.add(new_subscription)
        await session.commit()
        return Mas(message ="Подписка оформлена успешно.")