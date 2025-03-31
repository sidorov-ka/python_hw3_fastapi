from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users import FastAPIUsers

from src.models import User
from src.config import SECRET
from src.database import get_db
from src.auth.schemas import UserRead, UserCreate, UserUpdate

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"Пользователь зарегистрирован: {user.id}")

async def get_user_manager(db=Depends(get_db)):
    from src.auth.backend import auth_backend  # Отложенный импорт
    yield UserManager(SQLAlchemyUserDatabase(User, db))

fastapi_users = FastAPIUsers[User, int](
    get_user_manager=get_user_manager,
    auth_backends=[],
)

current_active_user = fastapi_users.current_user(active=True)
