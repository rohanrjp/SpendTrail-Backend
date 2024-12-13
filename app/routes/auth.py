from fastapi import APIRouter,HTTPException,status,Form
from fastapi.security import OAuth2PasswordBearer
from app.core.dependancies import db_dependancy
from app.core.auth_dependacies import user_dependancy
from app.models.auth_models import User
from app.schemas.auth_schemas import message, user_sign_up,UserProfileResponse,Token
from app.services.auth_services import check_user_exists, create_access_token,create_user, verify_password
from datetime import timedelta

auth_router=APIRouter(prefix="/auth",tags=["auth"])

@auth_router.post("/sign_up",status_code=status.HTTP_201_CREATED)
async def sign_up(user:user_sign_up,db:db_dependancy):
    existing_user=check_user_exists(user.email,db)
    if not existing_user:
        create_user(user,db)
        return message(message="User created succesfully")
    else:
        raise HTTPException(status_code=400,detail="User already exists")
    

@auth_router.post("/log_in",status_code=status.HTTP_200_OK,response_model=Token)
async def log_in(db:db_dependancy,username: str = Form(...), password: str = Form(...)):
    existing_user=check_user_exists(username,db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,message="User not found")
    if not verify_password(password,existing_user.hashed_password):
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,message="Password incorrect")
    access_token=create_access_token(existing_user.id,existing_user.email,expiry=timedelta(minutes=20)) 
    return {"access_token":access_token,"token_type":"bearer"}
        
@auth_router.get("/profile",status_code=status.HTTP_200_OK,response_model=UserProfileResponse)
async def get_profile_details(user:user_dependancy):
    return user