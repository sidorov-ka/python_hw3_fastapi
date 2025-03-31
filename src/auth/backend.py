from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication.strategy.db import DatabaseStrategy
from fastapi_users.db import SQLAlchemyUserDatabase

from src.models import User
from src.database import get_db

cookie_transport = CookieTransport(cookie_name="auth", cookie_max_age=3600)

def get_strategy() -> DatabaseStrategy:
    user_db = SQLAlchemyUserDatabase(User, get_db())
    return DatabaseStrategy(user_db, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="cookie",
    transport=cookie_transport,
    get_strategy=get_strategy,
)
