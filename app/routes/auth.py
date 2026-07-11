from fastapi import APIRouter,HTTPException,status,Form,Response,Request
from fastapi.security import OAuth2PasswordBearer
from app.core.dependancies import db_dependancy
from app.core.auth_dependacies import user_dependancy
from app.models.auth_models import User
from app.schemas.auth_schemas import message, user_sign_up,UserProfileResponse,Token
from app.services.auth_services import check_user_exists, create_access_token, create_refresh_token, create_user, verify_password, decode_token, get_user_from_token, get_token_from_request
from app.services.subscription_services import create_default_budget, process_subscriptions
from datetime import timedelta, datetime, timezone
from app.exceptions.auth_exceptions import Inavlid_credentials_exception

auth_router=APIRouter(prefix="/auth",tags=["Auth"])

ACCESS_TOKEN_EXPIRE=timedelta(minutes=15)
REFRESH_TOKEN_EXPIRE=timedelta(days=7)

def set_auth_cookies(response:Response, access_token:str, refresh_token:str):
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=int(ACCESS_TOKEN_EXPIRE.total_seconds()),
        path="/"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=True,
        max_age=int(REFRESH_TOKEN_EXPIRE.total_seconds()),
        path="/"
    )

def clear_auth_cookies(response:Response):
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")

@auth_router.post("/sign_up",status_code=status.HTTP_201_CREATED)
async def sign_up(user:user_sign_up,db:db_dependancy):
    existing_user=check_user_exists(user.email,db)
    if not existing_user:
        create_user(user,db)
        return message(message="User created succesfully")
    else:
        raise HTTPException(status_code=400,detail="User already exists")
    

@auth_router.post("/log_in",status_code=status.HTTP_200_OK)
async def log_in(response:Response, db:db_dependancy, username: str = Form(...), password: str = Form(...)):
    existing_user=check_user_exists(username,db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if not verify_password(password,existing_user.hashed_password):
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password incorrect")
    
    try:
        create_default_budget(db, existing_user)
        process_subscriptions(db, existing_user)
    except Exception as e:
        print("Subscription processing failed")

    access_token=create_access_token(existing_user.id,existing_user.email,expiry=ACCESS_TOKEN_EXPIRE)
    refresh_token=create_refresh_token(existing_user.id,existing_user.email)
    set_auth_cookies(response, access_token, refresh_token)
    return {"message":"Logged in successfully"}
        
@auth_router.post("/refresh")
async def refresh_token(response:Response, request:Request, db:db_dependancy):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="No refresh token")
    try:
        payload=decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise Inavlid_credentials_exception
        user_id=payload.get("id")
        email=payload.get("sub")
        user=db.query(User).filter(User.id==user_id).first()
        if not user:
            raise Inavlid_credentials_exception
        new_access=create_access_token(user.id,user.email,expiry=ACCESS_TOKEN_EXPIRE)
        new_refresh=create_refresh_token(user.id,user.email)
        set_auth_cookies(response, new_access, new_refresh)
        return {"message":"Token refreshed"}
    except Inavlid_credentials_exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid refresh token")

@auth_router.post("/logout")
async def logout(response:Response):
    clear_auth_cookies(response)
    return {"message":"Logged out"}

@auth_router.get("/profile",status_code=status.HTTP_200_OK,response_model=UserProfileResponse)
async def get_profile_details(user:user_dependancy):
    return user
