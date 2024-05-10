from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, models, schemas

from auth.models import User
from auth.utils import get_user_db

from config import SECRET_AUTH


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()


        if user_create.sex != "Мужской" and user_create.sex != "Женский":
            raise exceptions.InvalidPasswordException(
                reason="sex should be at Мужской or Женский"
            )
        
        if len(user_create.password) > 20 or len(user_create.password) < 8 :
            raise exceptions.InvalidPasswordException(
                reason="Password should be at least 8 character and less than 20"
            )

        if len(user_create.first_name) > 12:
            raise exceptions.InvalidPasswordException(
                reason="Password should be at least 8 character and less than 20"
            )
        if len(user_create.last_name) > 20:
            raise exceptions.InvalidPasswordException(
                reason="Password should be at least 8 character and less than 20"
            )

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        birth_date = user_dict.pop("birth_date")
        user_dict['birth_date'] = birth_date.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db = Depends(get_user_db)):
    yield UserManager(user_db)