from fastapi import FastAPI
from src.links.create import router as create_router
from src.links.redirect import router as redirect_router

app = FastAPI()

app.include_router(create_router)
app.include_router(redirect_router)
