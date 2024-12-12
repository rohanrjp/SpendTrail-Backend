from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.exceptions.auth_exceptions import Inavlid_credentials_exception
from app.schemas.auth_schemas import user_sign_up
from app.models.auth_models import User
from passlib.context import CryptContext
from app.core.config import Config
import jwt
from app.core.utils import get_ist_datetime
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import PyJWTError
from app.core.dependancies import db_dependancy

SECRET_KEY=Config.SECRET_KEY
ALGORITHM=Config.ALGORITHM

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_scheme=OAuth2PasswordBearer(tokenUrl="auth/log_in")

def hash_pass(password:str)->str:
    return pwd_context.hash(password)

def check_user_exists(email,db:Session):
    user=db.query(User).filter(email==User.email).first()
    return user

def create_user(user:user_sign_up,db:Session):
    hashed_password=hash_pass(user.password)
    ist_datetime=get_ist_datetime()
    new_user=User(name=user.name,email=user.email,hashed_password=hashed_password,avatar=user.avatar,join_date=ist_datetime)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
def verify_password(user_password:str,user_hashed_password:str)->bool:
    return pwd_context.verify(user_password,user_hashed_password)

def create_access_token(id:int,email:str,expiry:timedelta|None=None)->str:
    encodings={'sub':email,'id':id}
    if  expiry:
        encodings.update({'exp':datetime.now(timezone.utc)+expiry}) 
    else:
        encodings.update({'exp':datetime.now(timezone.utc)+timedelta(minutes=15)})   
    return jwt.encode(encodings,SECRET_KEY,ALGORITHM)     


def get_current_user(token:Annotated[str,Depends(auth_scheme)],db:db_dependancy):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id:int=payload.get('id')
        user_email:str=payload.get('sub')
        if user_id is None or user_email is None:
            raise Inavlid_credentials_exception
        user=db.query(User).filter(User.id==user_id).first()
        if not user:
            raise Inavlid_credentials_exception
        return user    
    except PyJWTError:
        raise Inavlid_credentials_exception
    
    
        
            
            
    