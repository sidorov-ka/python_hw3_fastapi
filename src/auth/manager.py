from fastapi import Depends
from fastapi_users import FastAPIUsers, BaseUserManager, IntegerIDMixin
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from src.models import User
from src.config import SECRET
from src.database import get_async_session
from src.auth.backend import auth_backend


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"Пользователь зарегистрирован: {user.id}")


async def get_user_manager(session=Depends(get_async_session)):
    user_db = SQLAlchemyUserDatabase(session, User)
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
