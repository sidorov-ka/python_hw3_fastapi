from fastapi_users import schemas

class UserRead(schemas.BaseUser[int]):
    class Config:
        from_attributes = True

class UserCreate(schemas.BaseUserCreate):
    class Config:
        from_attributes = True

class UserUpdate(schemas.BaseUserUpdate):
    class Config:
        from_attributes = True
