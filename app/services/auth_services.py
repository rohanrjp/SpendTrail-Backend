from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.schemas.auth_schemas import user_log_in, user_sign_up
from app.models.auth_models import User
from passlib.context import CryptContext
from app.core.config import Config
import jwt

SECRET_KEY=Config.SECRET_KEY
ALGORITHM=Config.ALGORITHM

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pass(password:str)->str:
    return pwd_context.hash(password)

def check_user_exists(user,db:Session):
    user=db.query(User).filter(user.email==User.email).first()
    return user

def create_user(user:user_sign_up,db:Session):
    hashed_password=hash_pass(user.password)
    new_user=User(name=user.name,email=user.email,hashed_password=hashed_password,avatar=user.avatar)
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