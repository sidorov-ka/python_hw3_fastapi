
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.auth.manager import fastapi_users, current_active_user
from src.auth.backend import auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.models import User

# Импорты всех роутеров
from src.links.create import router as create_router
from src.links.delete import router as delete_router
from src.links.redirect import router as redirect_router
from src.links.update import router as update_router
from src.links.search import router as search_router
from src.stats.view import router as stats_router

app = FastAPI(title="FastAPI HW 3")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# FastAPI Users
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Пример защищённой ручки
@app.get("/whoami", tags=["users"])
async def whoami(user: User = Depends(current_active_user)):
    return {"email": user.email, "id": user.id}

# Подключение всех роутеров
app.include_router(create_router)
app.include_router(delete_router)
app.include_router(redirect_router)
app.include_router(update_router)
app.include_router(search_router)
app.include_router(stats_router)
