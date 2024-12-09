from sqlalchemy.orm import Session
from app.schemas.auth_schemas import user_sign_up
from app.models.auth_models import User
from passlib.context import CryptContext


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