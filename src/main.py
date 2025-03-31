from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.auth.backend import auth_backend
from src.auth.manager import fastapi_users, current_active_user
from src.auth.schemas import UserRead, UserCreate, UserUpdate

from src.links.create import router as create_router
from src.links.delete import router as delete_router
from src.links.redirect import router as redirect_router
from src.links.update import router as update_router
from src.links.search import router as search_router
from src.stats.view import router as stats_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth
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

# Links
app.include_router(create_router)
app.include_router(delete_router)
app.include_router(redirect_router)
app.include_router(update_router)
app.include_router(search_router)

# Stats
app.include_router(stats_router)

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Добро пожаловать в API сервиса сокращения ссылок!"}
