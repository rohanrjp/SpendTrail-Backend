from fastapi import APIRouter,HTTPException,status
from app.core.dependancies import db_dependancy
from app.schemas.auth_schemas import message, user_sign_up
from app.services.auth_services import check_user_exists,create_user

auth_router=APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/sign_up",status_code=status.HTTP_201_CREATED)
async def sign_up(user:user_sign_up,db:db_dependancy):
    existing_user=check_user_exists(user,db)
    if not existing_user:
        create_user(user,db)
        return message(message="User created succesfully")
    else:
        raise HTTPException(status_code=400,detail="User already exists")
        