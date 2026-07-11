from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class user_sign_up(BaseModel):
    name:str
    email:str
    password:str
    avatar:str
    currency:str="INR"

class message(BaseModel):
    message:str

class user_log_in(BaseModel):
    email:str
    password:str
    
class Token(BaseModel):
    access_token:str 
    token_type:str        
    
class TokenData(BaseModel):
    email:str
    id:int
    exp:datetime       
    
class UserProfileResponse(BaseModel):
    id: int
    name: str
    email: str
    avatar: Optional[str] = None
    join_date: datetime    
    income_goal:float
    savings_goal:float
    currency:str="INR"